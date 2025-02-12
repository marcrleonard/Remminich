from immich.models import SearchModel
import requests
import json


class ImmichClient:
	def __init__(self, base_url: str, api_key: str):
		"""
		Initializes the ImmichClient wrapper.

		:param base_url: The base URL of the Immich server.
		:param api_key: The API key for authentication.
		"""
		self.base_url = base_url.rstrip('/')
		self.headers = {
			"x-api-key": f"{api_key}",
			# "Authorization": f"Bearer {api_key}",
			"Content-Type": "application/json",
			'Accept': 'application/json'
		}

	def list_albums(self):
		url = f"{self.base_url}/api/albums"
		response = requests.get(url, headers=self.headers)
		return self._handle_response(response)

	def get_album(self, album_uuid:str):
		url = f"{self.base_url}/api/albums/{album_uuid}"
		response = requests.get(url, headers=self.headers)
		return self._handle_response(response)

	def search_assets(self, search_payload:SearchModel):
		url = f"{self.base_url}/api/search/metadata"
		response = requests.post(url, headers=self.headers, data=json.dumps(search_payload.model_dump_json()))
		return self._handle_response(response)

	def get_album(self, album_uuid:str):
		url = f"{self.base_url}/api/albums/{album_uuid}"
		response = requests.get(url, headers=self.headers)
		return self._handle_response(response)

	def make_thumb_url(self, asset_id:str):
		return f"{self.base_url}/api/assets/{asset_id}/thumbnail"
	def get_thumbnail(self, asset_id:str):
		url = self.make_thumb_url(asset_id)
		response = requests.get(url, headers=self.headers)
		return response

	def _handle_response(self, response, resp_type=None):
		"""Handles HTTP responses and raises exceptions for errors."""
		try:
			response.raise_for_status()
			return response.json()
		except requests.exceptions.HTTPError as err:
			return {"error": str(err), "status_code": response.status_code}
		except ValueError:
			return {"error": "Invalid JSON response", "status_code": response.status_code}


if __name__ == "__main__":
	c = ImmichClient('http://localhost:2283/', "xnFmvnF4E2ijDXZPbCL8LjJm8kbdSwe85EvzD5VZA")
	for a in c.list_albums():
		resp = c.get_thumbnail("8c5569b0-4f14-4ca6-abeb-25fec81e0101")
		print(resp)