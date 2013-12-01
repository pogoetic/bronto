class Scraper:

	def __init__ (self):

		gox = None

	def Scrape_gox_trades(self):

		from MtgoxClass import Mtgox
		import json, time, decimal as D, sqlite3 as sdb, requests

		gox = Mtgox() #create instance of mtgox obj

		#PUll in trade history of a currency pair
		#Will only pull 1000 rows at a time

		path = 'db/test.db'
		stmnt = 'select max(date) from mtgoxUSD'
		conn = sdb.connect(path)
		with conn:
			cur = conn.cursor()    
			cur.execute(stmnt)
			maxdate = cur.fetchone()

		time_since = maxdate[0]   #time_now - 30 #time in seconds
		#gox format is microtime which they call a TID, must be an int for the URLENCODE to work properly
		time_since_gox = int(time_since * 1000000) 
		#print 'time since: ', str(time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(time_since)))

		j = None
		i = 0
		while j == None: #Keep retrying until server responds...
			
			r = gox.auth('BTCUSD/money/trades/fetch',{'since':str(time_since_gox)})
				#TEST BAD REQUEST: r = requests.get('http://httpbin.org/status/404')
				#print json.dumps(r.json(), sort_keys = True, indent=4, separators=(',', ': '))			
			if r.status_code == requests.codes.ok:
				j = r.json()
				i = 0
			elif i > 10:
				r.raise_for_status()
			else:
				time.sleep(10) #sleep 10 seconds between retries
				i = i + 1

		stmnt = 'insert into mtgoxUSD values(?,?,?,?,?,?,?,?,?,?,?)'
		x=0
		for item in j['data']:
			#print item['date'],item['price'],item['amount'],item['price_int'],item['amount_int'],item['tid'],item['price_currency'],item['item'],item['trade_type'],item['primary'],item['properties']
			data = [item['date'],item['price'],item['amount'],item['price_int'],item['amount_int'],item['tid'],item['price_currency'],item['item'],item['trade_type'],item['primary'],item['properties']]
			with conn:
				cur = conn.cursor()    
				cur.execute(stmnt,data)
			x+=1	
			print 'data inserted! row: ',x

		return x

