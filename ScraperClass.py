class Scraper:

	def __init__ (self):

		gox = None

	def Scrape_gox_trades(self):
		#PUll in trade history of a currency pair
		#Will only pull 1000 rows at a time
		from MtgoxClass import Mtgox
		import json, time, MySQLdb, requests, boto.ses, socket
		import ConfigParser

		config = ConfigParser.ConfigParser()
		config.read('config.cfg')

		gox = Mtgox() #create instance of mtgox obj

		#load our SES API public/private Key
		key = [config.get('ses','key'),config.get('ses','secretkey')]

		#load mysql db credentials
		hostname = socket.gethostname()
		if hostname.find(config.get('mysql','remotehostname'))>=0:   #IF we are on the server, use localhost. 
			host = 'localhost'
		else:
			host = config.get('mysql','host') #If we are remote use the server name
		dbuser = config.get('mysql','dbuser')
		dbpwd = config.get('mysql','dbpwd')
		dbname = config.get('mysql','dbname')
		db=MySQLdb.connect(host=host,user=dbuser,passwd=dbpwd,db=dbname)

		stmnt = 'select max(tid) from mtgoxUSD'
		with db:
				c = db.cursor()	
				c.execute(stmnt)
				maxtid = c.fetchone()

		time_since = maxtid[0]   #time_now - 30 #time in seconds
		#gox format is microtime which they call a TID, must be an int for the URLENCODE to work properly
		time_since_gox = int(time_since) 
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
				conn = boto.ses.connect_to_region('us-east-1',aws_access_key_id=key[0],aws_secret_access_key=key[1])
				message = 'Server status code - %s\nServer Response Content - %s' % (r.status_code(),r.text)
				sender = config.get('ses','sender')
				recip = config.get('ses','recipient')
				subj = 'MtGox Scraper ERROR'
				conn.send_email(sender,subj,message,[recip])  
				print 'sent error email to %s' % (recip)  
				r.raise_for_status()
			else:
				time.sleep(10) #sleep 10 seconds between retries
				i = i + 1

		x=0
		for item in j['data']:
				#print item['date'],item['price'],item['amount'],item['price_int'],item['amount_int'],item['tid'],item['price_currency'],item['item'],item['trade_type'],item['primary'],item['properties']
			data = [item['date'],item['price'],item['amount'],item['price_int'],item['amount_int'],item['tid'],item['price_currency'],item['item'],item['trade_type'],item['primary'],item['properties']]

			if data[5] <= time_since:
				#prevent insertion of duplicates just in case Mtgox starts processing trades with duplicate TID's
				print 'Duplicate TID Found - insert aborted ', data[5]
			else:	
				with db:
					c = db.cursor()	
					c.execute('insert into mtgoxUSD values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,''NULL'')',data)
						#c.execute("""SELECT * FROM mtgoxUSD order by date desc LIMIT %s""",(limit,))

				x+=1	
				print 'data inserted! row: %s  TID: %s' % (x,data[5])

		return x

