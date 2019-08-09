from urllib.parse import urljoin
from requests_html import HTMLSession
import logging

class Site:

	def __init__(self, base_url, username, password):
		self.session = HTMLSession()
		self.base_url = base_url
		self.username = username
		self.password = password

	def login(self):
		pass

	def download(self, extension):
		pass


class CuteEmbroidery(Site):

	def __init__(self, username, password):
		super().__init__("http://cuteembroidery.com", username, password)

	def login(self):
		login_url = urljoin(self.base_url, "/?com=signin")
		logging.info("Logging in to url '%s' with username '%s' and password '%s' ", login_url, self.username, self.password)		
		self.session.post(
			login_url, 
			data={
				'loginemail': self.username,
				'pass': self.password,
				'remember': 'on',
				'com': 'signin',
				'gocom': '',
				'govl': '',
				'formkey': '7302872765820497'
			}
		)

	def _find_download_link(self, extension):
		logging.info("Finding download link for extension '%s'...", extension)
		response = self.session.get(urljoin(self.base_url, "/freedesigneveryday.html"))
		download_link = response.html.find('a', containing=extension)[0].attrs['href']
		logging.info("Download link: '%s'", download_link)
		return download_link

	def download(self, extension):
		download_link = self._find_download_link(extension)
		logging.info("Downloading from url: '%s'...", download_link)
		content = self.session.get(download_link).content
		logging.info("Done!")
		return content


class AdorableApplique(Site):

	def __init__(self, username, password):
		super().__init__("http://www.adorableapplique.com", username, password)

	def login(self):
		login_url = urljoin(self.base_url, "/index.php")
		data= {
			'email': self.username,
			'pass': self.password,
			'remember': 'on',
			'com': 'signin',
			'gocom': '',
			'govl': '',
			'formkey': 'c7gHjdh'
		}
		logging.info("Logging in to url '%s' with username '%s' and password '%s' and data '%s'", login_url, self.username, self.password, data)
		response = self.session.post(login_url, data=data)

	def _find_extension_id(self, response, extension):
		logging.info("Finding id for extension '%s'...", extension)
		id = response.html.find("option", containing=extension.upper())[0].attrs['value']
		logging.info("Found id '%s'", id)
		return id;

	def _find_design_id(self, response):
		logging.info("Finding id for design...")
		id = response.html.find("input[name='vl']")[0].attrs['value']
		logging.info("Found id '%s'", id)
		return id;

	def download(self, extension):
		response = self.session.get(urljoin(self.base_url, "/free-embroidery-design.html"))
		design_id = self._find_design_id(response)
		extension_id = self._find_extension_id(response, extension)
		download_post_data = {
			'file': extension_id,
			'cm': 'download',
			'type': 'free',
			'vl': design_id,
			'x': 77,
			'y': 15,
		}
		logging.info("Downloading from url: '%s' with data: '%s'...", self.base_url, download_post_data)
		response = self.session.post(self.base_url, data=download_post_data, allow_redirects=True)
		logging.info("Done!")
		return response.content

class CuteAlphabets(Site):

	def __init__(self, username, password):
		super().__init__("http://cutealphabets.com/", username, password),

	def login(self):
		login_url = urljoin(self.base_url, "/index.php")
		data = {
			'loginemail': self.username,
			'pass': self.password,
			'remember': 'on',
			'com': 'signin',
			'gocom': '',
			'govl': '',
			'form_key': 'c7gHjdh'
		}
		logging.info("Logging in to url '%s' with username '%s' and password '%s' and data '%s'", login_url, self.username, self.password, data)		 
		self.session.post(login_url, data=data)

	def _find_download_page(self):
		logging.info("Finding download page...")
		response = self.session.get(self.base_url)
		download_page = response.html.find(".box_freebies")[0].find('a')[-1].attrs['href']
		logging.info("Found page '%s'", download_page)
		return download_page

	def download(self, extension):
		download_page = self._find_download_page()
		response = self.session.get(download_page);
		download_link = response.html.find('a', containing=extension)[0].attrs['href']
		logging.info("Downloading from url: '%s'...", download_link)
		content = self.session.get(download_link).content
		logging.info("Done!")
		return content
