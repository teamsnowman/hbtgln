import urllib
import json

class FanGraphs:
	def __init__(self, apiKey):
		self.apiKey = apiKey
		self.ROOT_URL = "http://www.kimonolabs.com/api/b54z7vvq"

	def getData(self, date, team, season):
		encodedData = urllib.urlencode({
			'apikey': self.apiKey,
			'team': team,
			'date': date,
			'season': str(season),
			'dh': '0',
			})
		results = json.load(urllib.urlopen("%s?%s" % (self.ROOT_URL, encodedData)))
		return results


