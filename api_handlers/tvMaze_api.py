import requests
import json


class tvMaze_API_Handler:
	# https://www.tvmaze.com/api

	def __init__(self):
		self.url = "http://api.tvmaze.com"
		self.header = {'content-type': 'application/json'}

	def search(self, name):
		url = self.url + f"/search/shows?q={name}"

		r = requests.get(url, headers=self.header)

		return r

	def search_single(self, name):
		# Unlike regular search this only returns the first result
		url = self.url + f"/singlesearch/shows?q={name}"

		r = requests.get(url)

		return r

	def search_people(self, name):
		url = self.url + f"/search/people?q={name}"

		r = requests.get(url, headers=self.header)

		return r

	def lookup(self, tvrage=None, thetvdb=None, imdb=None):
		# Same as the search function more or less
		# This one searches based on a given ID (tvrage, theTVdb or imdb id's)
		url = self.url + "/lookup/shows?"

		if tvrage != None:
			url = url + f"tvrage={tvrage}"
		elif thetvdb != None:
			url = url + f"thetvdb={thetvdb}"
		elif imdb != None:
			url = url + f"imdb={imdb}"
		else:
			raise Exception("No values given for: 'tvrage', 'thetvdb' or 'imdb'\
			\nPlease provide at least one off these with a value")

		r = requests.get(url, headers=self.header)

		return r

	def shows(self, show_id):
		url = self.url + f"/shows/{show_id}"

		r = requests.get(url, headers=self.header)

		return r

	def shows_episodes(self, show_id):
		url = self.url + f"/shows/{show_id}/episodes"

		r = requests.get(url, headers=self.header)

		return r

	def shows_season(self, show_id):
		url = self.url + f"/shows/{show_id}/seasons"

		r = requests.get(url, headers=self.header)

		return r

	def shows_episode_number(self, show_id, season, episode):
		url = self.url + f"/shows/{show_id}/episodebynumber?season={season}&number={episode}"

		r = requests.get(url, headers=self.header)

		return r

	def shows_episode_next(self, episode_nr):
		url = self.url + f"/episodes/{episode_nr}"

		r = requests.get(url, headers=self.header)

		return r

	def shows_episode_find_next(self, show_id):
		data = self.shows(show_id).json()

		try:
			ep_id = data['_links']['nextepisode']['href'].split('/')[-1]
			return self.shows_episode_next(ep_id), data['name']
		except KeyError:
			print("[!] Error - Unable to find next episode info")
			return False, False
