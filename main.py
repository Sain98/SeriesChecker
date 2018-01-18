#!/usr/bin/python
import configparser
import datetime
from os import system, name, getcwd, path

# Load API handler
from api_handlers.tvMaze_api import tvMaze_API_Handler


# ===========================
# = SeriesChecker functions =
# ===========================
class SeriesChecker:

	def __init__(self, tracking=None):
		if tracking is None:
			tracking = {}
		self.api_handler = tvMaze_API_Handler()

		# { Serie_id(int): "Name", ... } - Read from config
		self.tracking = tracking

		# Result from api request
		# result_b is for requesting next episode or extra info etc.
		# without getting rid off the original result
		self.result = None
		self.result_b = None

	def command_handler(self, cmd):
		print(cmd)
		cmd[0] = cmd[0].lower()

		# Searching
		if cmd[0] == "search":
			# Search Game of thrones
			try:
				self.result = self.api_handler.search(cmd[1])
				self.display_results()
			except IndexError:
				print("Error: You need to supply a name to search\nEx: search game of thrones")
		elif cmd[0] == "ssearch" or cmd[0] == "singlesearch":
			# ssearch Game Of Thrones | singlesearch game of thrones
			try:
				self.result = self.api_handler.search_single(cmd[1])
				self.display_result()
			except IndexError:
				print("Error: You need to supply a name to search\nEx: search game of thrones")

		# Tracking
		elif cmd[0] == "tracking":
			self.tracking_list()
		elif cmd[0] == "tracklist":
			self.tracking_list_small()
		elif cmd[0] == 'add' or cmd[0] == 'track':
			try:
				self.tracking_add(cmd[1])
			except IndexError:
				print("Error: You need to supply a Show ID\nEx: add 82")
		elif cmd[0] == 'remove':
			try:
				self.tracking_remove(cmd[1])
			except IndexError:
				print("Error: You need to supply a Show ID to remove\nEx: remove 82")

		# Next episode
		elif cmd[0] == "next":		# cmd[1] = Serie ID
			try:
				self.result, show_name = self.api_handler.shows_episode_find_next(cmd[1])
				if not self.result:
					self.display_next_episode(self.result.json(), show_name)
			except IndexError:
				print("Error: You need to supply a Show ID\nEx: next 82")

		else:
			print(f"Command: {cmd} | Not found")
		
		return

	def tracking_list(self):
		for show_id, show_name in self.tracking.items():
			self.result = self.api_handler.shows(show_id)

			self.display_result()
		return

	def tracking_list_small(self):
		for k, v in self.tracking.items():
			print(f"ID: {k} | Name: {v}")

	def tracking_add(self, show_id):
		# Add the given id to the tracking list

		# Get the shows name for the config/tracking list
		show_name = self.api_handler.shows(show_id).json()['name']

		# Update tracker
		self.tracking.update({show_id: show_name})

		# Update config
		cfg = ConfigHandler()
		cfg.config_read()
		cfg.config_edit('Tracking', show_id, show_name)

		return

	def tracking_remove(self, show_id):
		self.tracking.pop(show_id)
		cfg = ConfigHandler()
		cfg.config_read()
		cfg.config_remove('Tracking', show_id)

	def display_results(self):
		for result in self.result.json():
			self.display_result(result['show'])

	def display_result(self, data=None):
		if data is None:
			data = self.result.json()

		if type(data) != dict:
			# JSON is normally a type dict
			data = data.json()

		show_name = data['name']

		print("="*50)
		print(f"Name: {show_name}")
		print(f"Status: {data['status']}")
		print(f"Rating: {data['rating']['average']}")
		print(f"ID: {data['id']}")

		if data['schedule']['time'] != '':
			print(f"Schedule: {data['schedule']['time']} | Days: ", end='')
		else:
			print("Days: ", end='')

		for x in range(len(data['schedule']['days'])):
			print(data['schedule']['days'][x], end='')
			if x < len(data['schedule']['days']) - 1:
				print(", ", end='')

		if len(data['genres']) > 0:
			print("\nGenres: ", end='')
		for x in range(len(data['genres'])):
			print(data['genres'][x], end='')
			if x < len(data['genres']) - 1:
				print(", ", end='')

		print()
					
		# Next episode:
		try:
			ep_id = data['_links']['nextepisode']['href'].split('/')[-1]
			episode_data = self.api_handler.shows_episode_next(ep_id)
			if episode_data is not None:
				print("\nNext Episode: ")
				self.display_next_episode(episode_data.json())
		except KeyError:
			if data['status'] != "Ended":
				print("\nNo information found for the next episode.")

		print("\n = External ID's = ")
		if data['externals']['tvrage'] is not None:
			print(f"TVRage: {data['externals']['tvrage']}")

		if data['externals']['thetvdb'] is not None:
			print(f"TheTVdb: {data['externals']['thetvdb']}")

		if data['externals']['imdb'] is not None:
			print(f"IMDB: {data['externals']['imdb']} | URL: http://www.imdb.com/title/{data['externals']['imdb']}/")

	def display_next_episode(self, result, show_name=None):
		# json formatted result
		# print(result)	# DEBUG

		# Next episode info:
		if show_name is not None:
			print(f"Show: {show_name}")
			tab = "" 	# No tab if the user only wants to see the next ep info
		if show_name is None:
			tab = "\t"

		print(f"{tab}Episode Name: {result['name']}")
		print(f"{tab}Season {result['season']} | Episode {result['number']}")
		print(f"{tab}Date: {result['airdate']} @ {result['airtime']} ({self.get_day(result['airdate'])})")

		try:
			print(f"{tab}Summary: {result['summary'][3:-4]}")	 # Get rid off the <p> tags
		except IndexError:
			pass

		return

	@staticmethod
	def get_day(date):
		# Date ex: '2018-01-12'
		date = date.split('-')

		try:
			day = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))  # Year, Month, Day
		except IndexError as ex:
			print(f"Error: {ex}")
			return None

		day = day.weekday()

		weekday = {
					0: "Monday", 
					1: "Tuesday",
					2: "Wednesday", 
					3: "Thursday", 
					4: "Friday", 
					5: "Saturday", 
					6: "Sunday"
				}

		return weekday[day]


# ====================
# = Config functions =
# ====================
#
# Handles anything related to the config
# 
class ConfigHandler:
	def __init__(self):
		self.config_loc = f"{getcwd()}/config.conf"
		self.config_pars = configparser.ConfigParser()

	def config_exists(self):
		# Check if config exists
		return path.isfile(self.config_loc) 	# Returns True if cfg exists else -> False

	def config_read(self):
		# Read stored info from config
		tracking = {}

		self.config_pars.read(self.config_loc)

		uname = self.config_pars['Data']['Name']
		for key in self.config_pars['Tracking']:
			tracking.update({key: self.config_pars['Tracking'][key]})

		return tracking, uname

	def config_make(self, uname):
		# Makes default config if there is no existing config
		self.config_pars.add_section('Data')
		self.config_pars.set('Data', 'Name', uname)
		self.config_pars.add_section('Tracking')

		with open(self.config_loc, 'w') as conf_file:
			self.config_pars.write(conf_file)
		return

	def config_edit(self, section, var_name, new_val, auto_write=True):
		try:
			self.config_pars.set(section, var_name, new_val)

			if auto_write:
				with open(self.config_loc, 'w') as cfg_file:
					self.config_pars.write(cfg_file)

		except configparser.NoSectionError:
			print(f"Error section: [ {section} ] not found!")
			print("Availabe sections are: ")
			print(self.config_pars.sections())

	def config_remove(self, section, var_name, auto_write=True):

		if self.config_pars.has_option(section, var_name):
			self.config_pars.remove_option(section, var_name)

			if auto_write:
				with open(self.config_loc, 'w') as c:
					self.config_pars.write(c)
		else:
			print(f"ID: {var_name} | Not found in the tracking list")


# ============
# = Commands =
# ============


def display_commands():
	print("Available commands:")
	print()
	print("q, quit, exit - Exit the program")
	print("cls, clear - Clear the screen")
	print("help, commands - Displays this screen")
	print()
	print("Config commands: ")
	print("set {section} {variable name} {new value}")
	print("\tExample to change your username:")
	print("\tset data name your name")
	print()
	print("TV Show commands: ")
	print("searching:")
	print("search - Search for a given name (returns multiple results if multiple are found")
	print("\tEx: search Game of Thrones")
	print("ssearch, singlesearch - Search for a given name only returns the first result")
	print("\tEx: ssearch Game of Thrones | singlesearch Game of Thrones")
	print()
	print("tracking:")
	print("tracking - returns info on all the shows you are currently tracking")
	print("add, track - Adds a given show id (which can be found using the search commands)")
	print("\tto the tracking list Ex: add 82 | track 82")
	print()
	print("Next episode:")
	print("next - Returns info on the next episode (Episode name, summary, date)")
	print("\tEx: next 82")

	return

# ========
# = Main =
# ========


def main():

	# Check if config exists	
	cfg = ConfigHandler()
	cfg_exists = cfg.config_exists()

	# Make it if it does not exist
	if not cfg_exists:		# cfg_exists == False:
		track = {}
		uname = "Guest"		# Can be changed later
		cfg.config_make(uname)

	# Read config for tracked series, settings, etc..
	else:
		track, uname = cfg.config_read()

	print(f"Username: {uname}\n")

	# Show tracked shows
	print("Tracking: ")
	for k, v in track.items():
		print(f"\tID: {k} | Name: {v}")
	print()

	# Load SeriesChecker() with any custom settings if loaded
	sc = SeriesChecker(track)

	# while True loop for the user to enter his commands
	while True:
		print()
		print(f"{uname} :>> ", end='')

		cmd = input()

		if len(cmd) > 0:
			cmd = cmd.split(maxsplit=1)

			cmd[0] = cmd[0].lower()

			if cmd[0] == 'q' or cmd[0] == 'quit' or cmd[0] == 'exit':
				quit(0)

			elif cmd[0] == 'set':
				cmd = cmd[1].split(maxsplit=2)
				cmd[0] = cmd[0][0].upper() + cmd[0][1:]		# First letter uppercase
				if len(cmd) == 3:
					cfg.config_edit(cmd[0], cmd[1], cmd[2])
				else:
					print("Usage: set {section} {variable name} {new value}")
					print("Ex: set Data name Sain")

			elif cmd[0] == 'help' or cmd[0] == 'commands':
				display_commands()

			elif cmd[0] == 'cls' or cmd[0] == 'clear':
				if name == 'nt':		# os.name
					# Windows
					system('cls')
				if name == 'posix':		# os.name
					# Linux
					system('clear')

			else:
				sc.command_handler(cmd)
		else:
			print("You need to provide a command")


if __name__ == '__main__':
	main()