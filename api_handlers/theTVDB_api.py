import requests
import json
import urllib

class theTVDB_API_Handler:
	# https://api.thetvdb.com/swagger#/

	def __init__(self):
			self.header = {'content-type': 'application/json'}
			self.auth = None

			self.api_url = "https://api.thetvdb.com"
			self.api_key = "YOUR_API_KEY"

			self.username = "YOUR_USER_NAME"
			self.user_key = "YOUR_USER_KEY"

			self.token = ""		# temporary token received in get_token() - lasts 24 hours

			self.debug_mode = True	# Disable this for less off the technical output


	# if err_code != 200: 
	def response_error_codes(err_code):

		print(f"[!] Response code: {err_code}")

		if err_code == 401:
			print("[!] Invalid credentials and/or API token")
			quit()

		elif err_code == 415:
			print("[!] 415: Unsupported Media Type")
			print("[!] Check or you included headers")
			quit()

		else:
			print("[!] Unknown error code")
			quit()


	def get_token(self):
		url = self.api_url + "/login"

		payload = {	
					"apikey": self.api_key, 
					"username": self.username, 
					"userkey": self.user_key
				}

		print(f"\n[*] Sending request to {url}")

		response = requests.post(
							url, 
							data=json.dumps(payload), 
							headers=self.header
						)

		if response.status_code == 200:
			self.token = response.json()["token"]	# Save the token

			if self.debug_mode:		
				# Only prints this in debug mode
				# the token tends to fill the screen a bit :p
				print(f"[*] Response: {response}")
				print(f"[*] Token: {self.token}")

		else:
			response_error_codes(response.status_code)

		# Update header with token for authentication
		self.header = {'content-type': 'application/json',
		"Authorization": f"Bearer {self.token}"}


	def refresh_token(self):
		url = self.api_url + "/refresh_token"

		r = requests.get(url, headers=self.header)

		if r.status_code == 200:
			self.token = r.json()["token"]			# Save new token

			if self.debug_mode:		
				# Only prints this in debug mode
				# the token tends to fill the screen a bit :p
				print(f"[*] Response: {response}")
				print(f"[*] New Token: {self.token}")

		else:
			response_error_codes(response.status_code)


	"""
		functions related to handling series below
		searching for, getting series id, episodes, detailed info, actors, ...  
	"""
	def search_series(self, name=None, imdbID=None, zap2itId=None):
		# https://api.thetvdb.com/swagger#!/Search/get_search_series
		url = self.api_url + "/search/series?"

		if name != None:
			url = url + "name=" + urllib.parse.quote(name, safe='')
		elif imdbID != None:
			url = url + "imdbId=" + urllib.parse.quote(imdbID, safe='')
		elif zap2itId != None:
			url = url + "zap2itId=" + urllib.parse.quote(zap2itId, safe='')

		r = requests.get(url, headers=self.header)

		if r.status_code == 200:
			if self.debug_mode:
				print(f"[*] Response: {r}\n")

			data = r.json()["data"]

			return data

		return 0


	def series(self, db_id):
		# https://api.thetvdb.com/swagger#!/Series/get_series_id
		url = self.api_url + "/series/" + db_id

		r = requests.get(url, headers=self.header)

		if r.status_code == 200:
			print(f"[*] Response: {r}\n")

			data = r.json()['data']

			try:
				errs = r.json()['errors']
			except KeyError:
				errs = ""

			print(data)
			print()

			if len(errs) > 0:
				print(errs)
		else:
			response_error_codes(r.status_code)

		return 0

	def series_episodes(self, db_id, page=None):
		# https://api.thetvdb.com/swagger#!/Series/get_series_id_episodes
		url = self.api_url + f"/series/{db_id}/episodes"

		if page != None:
			url = url + f"?page={page}"

		r = requests.get(url, headers=self.header)

		if r.status_code == 200:
			data = r.json()
			return data
		else:
			response_error_codes(r.status_code)

		return 0
