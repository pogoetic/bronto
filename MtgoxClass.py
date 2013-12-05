#IMPORTANT NOTES:
#All API methods are cached for 10 seconds. Do not request results more often than that, you might be blocked by the anti-DDoS filters. 
class Mtgox:

	def __init__ (self):

		#load our API Keys
		fobj = open("key.txt")
		key = fobj.readlines()
		fobj.close()

		key = map(lambda s: s.strip(), key) #strip the \n from the key

		self.key = key[0]
		self.sec = key[1]

	def __sign(self, path, data):
		import hmac, base64, hashlib
		
		mac = hmac.new(base64.b64decode(self.sec), path+chr(0)+data, hashlib.sha512)
		return base64.b64encode(str(mac.digest()))

	def auth(self, path, inp={}, get=False):
		import time, requests, json, urllib, urllib2

		base = 'https://data.mtgox.com/api/2/'
		
		if get:
			#GET
			get_data = urllib.urlencode(inp) 
			r = requests.get(base+path,data=get_data)
			#data_string = json.dumps(r.json(), indent=2)
		else:
			inp['tonce'] = str(int(time.time()*1e6)) #fill inp dict with tonce value
			data = urllib.urlencode(inp) #URL Encode the tonce value
			restsign = self.__sign(path, data)

			#POST
			headers = {'Rest-Key':  self.key,
			           'Rest-Sign': restsign,
			           'Content-Type': 'application/x-www-form-urlencoded'}
			r = requests.post(base+path, data=inp, headers=headers)
			#print r.request.headers
			
			if r.status_code != requests.codes.ok:
				print r.status_code
				print r.headers
				#r.raise_for_status()  #Will throw a python error if POST fails

		return r
	

#!! REMEMBER !!
#Bid refers to buying BTC using the auxiliary currency (e.g. USD)
#Ask refers to selling BTC for the auxiliary currency
#The minimum trade size to buy OR sell is 0.01 BTC





#Will throw a python error if POST fails
#r.raise_for_status()

#GET example 
#path = 'BTCUSD/money/ticker_fast'
#r = auth(path, {}, True)
#print json.dumps(json.loads(r.text), sort_keys = True, indent = 2)


#Encoding to JSON
#data = [ { 'a':'A', 'b':(2, 4), 'c':3.0 } ]
#print 'ORIGINAL Data' , data
#data_string = json.dumps(data)
#print 'ENCODED:', data_string

#Decoding from JSON
#decoded = json.loads(data_string)
#print 'DECODED:', decoded
#print 'ORIGINAL:', type(data[0]['b'])
#print 'DECODED :', type(decoded[0]['b'])

