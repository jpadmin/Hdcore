import json, time, hashlib, urllib2, random
class Client:
	def __init__(self, privateKey, publicKey):
		self.__endpoint = 'https://api.hostdime.com/v1/'
		self.__privateKey = privateKey
		self.__publicKey = publicKey

	def __generateHex(self, max, min=0, orKey=0):
		return hex(random.randint(min, max)|orKey).split('x')[1].zfill(4)

	def __generateUUID(self):
		return self.__generateHex(max=65535)+self.__generateHex(max=65535)+'-'+self.__generateHex(max=65535)+'-'+self.__generateHex(max=4095, orKey=16384)+'-'+self.__generateHex(max=16383, orKey=32768)+'-'+self.__generateHex(max=65535)+self.__generateHex(max=65535)+self.__generateHex(max=65535)

	def __generateHash(self):
		hashelements = ':'.join([self.__timestamp, str(self.__unique), self.__privateKey, self.__action, json.dumps(self.__parameters)])
		hashCode = hashlib.sha256(hashelements.encode('utf-8')).hexdigest()
		return hashCode

	def __buildJson(self):
		self.__payLoad = self.__parameters
		authenticationData = {
			'api_key' : str(self.__publicKey),
			'api_timestamp' : str(self.__timestamp),
			'api_unique' : str(self.__unique),
			'api_hash' : str(self.__hash)
		}
		self.__payLoad.update(authenticationData)

		#self.__payLoad = json.dumps(self.__payLoad)

	def __getResponse(self):
		return urllib2.urlopen(urllib2.Request(self.__endpoint+'/'.join(self.__action.split('.'))+'.json', data=json.dumps(self.__payLoad), headers = {'content-type': 'application/json'})	).read()

	def call(self, action, parameters = None):
		if parameters is None:
			self.__parameters = {}
		else:
			self.__parameters = parameters

		self.__action = action

		#generate api_timestamp current UTC timestamp
		self.__timestamp = str(int(time.time()))

		#generate uuid for api_unique as per the standards in https://docs.python.org/2/library/uuid.html
		self.__unique = self.__generateUUID()

		#generate hash for api_hash as per the method in https://api.hostdime.com/docs/request.html
		self.__hash = self.__generateHash()

		#build the Json request for the coreAPI server
		self.__buildJson()

		print "Request \n"+json.dumps(self.__payLoad, indent=2)

		#get response from the coreApi server
		responseData = self.__getResponse()
		print responseData

		#print "payLoad -> " + str(self.__payLoad)

