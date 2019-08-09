from sites import CuteEmbroidery, AdorableApplique, CuteAlphabets
from os.path import join
import datetime
import logging
import json
import os
import sys


logging.basicConfig(
	filename='logging.log',
	level=logging.INFO,
	format='%(asctime)s %(message)s')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

config_file_path = join(os.path.dirname(os.path.realpath(__file__)), "config.json")

with open(config_file_path) as file_content: 
	config = json.load(file_content)

timestamp = datetime.datetime.now()
extension = config['extension']
destination_folder = config['destination_folder']

sites = [
	CuteEmbroidery(config['cute_embroidery']['username'], config['cute_embroidery']['password']), 
	AdorableApplique(config['adorable_applique']['username'], config['adorable_applique']['password']), 
	CuteAlphabets(config['cute_alphabets']['username'], config['cute_alphabets']['password'])
]

for site in sites:
	try:
		destination_file_name = "{0}-{1}.{2}".format(site.__class__.__name__, timestamp.strftime("%Y-%m-%d[%H-%M-%S]"), extension)
		destination = join(destination_folder, destination_file_name)

		site.login()
		response_content = site.download(extension)

		logging.info("Writing content to file: '%s'", destination)
		with open(destination, 'wb') as f:
			f.write(response_content)
		logging.info("Done!")
	except Exception as e:
	 	logging.error("Unexpected exception: '%s'", e)
