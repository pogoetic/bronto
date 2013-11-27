from MtgoxClass import Mtgox
import json, time, decimal as D, sqlite3 as sdb
from pprint import pprint

gox = Mtgox() #create instance of mtgox obj
start = time.time()
end = time.time()

'''
while ((end-start)/60) < 5: #run for 5 minutes

	end = time.time()

	#Ticker
	r = gox.auth('BTCUSD/money/ticker',{})
	#print json.dumps(r.json(), sort_keys = True, indent=4, separators=(',', ': '))
	j = r.json()
	#print j['data'].keys() #get members of dict branch

	tick_date = str(time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(D.Decimal(j['data']['now'])/1000000)))
	tick_avg = j['data']['avg']['value']
	tick_buy = j['data']['buy']['value']
	tick_sell = j['data']['sell']['value']
	tick_high = j['data']['high']['value']
	tick_low = j['data']['low']['value']
	tick_vol = j['data']['vol']['value']
	tick_vwap = j['data']['vwap']['value']

	
	#print tick_date
	#print 'avg:  %s', tick_avg 
	#print 'buy:  %s', tick_buy
	#print 'sell: %s', tick_sell
	#print 'high: %s', tick_high
	#print 'low:  %s', tick_low
	#print 'vol:  %s', tick_vol
	#print 'vwap: %s', tick_vwap
	#print ''
	

	#SQLITE
	path = 'db/test.db'
	#stmnt = 'select * from gox_ticker'
	stmnt = 'insert into gox_ticker values(?,?,?,?,?,?,?,?,?)'
	data = [None,tick_date,tick_avg,tick_buy,tick_sell,tick_high,tick_low,tick_vol,tick_vwap]


	conn = sdb.connect(path)
	with conn:
		cur = conn.cursor()    
		cur.execute(stmnt,data)
		#cur.execute(stmnt)
		#rows = cur.fetchall()

	cur.execute('Select max(rowid) from gox_ticker')	
	maxrow = cur.fetchone()
	print "row inserted", maxrow
	#for row in rows:
	#	pprint(row)

	j=None
	r=None

	time.sleep(15) #give us a gap between API calls

	#if time.time() > 1385471461.15: #approx 8 hours from 1385442661.15   (28,800 seconds more)
	#	break
'''

#PUll in trade history of a currency pair


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
#print time_now
#print time_since
#print time_since_gox
#print 'time now: ', str(time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(time_now)))
print 'time since: ', str(time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(time_since)))

r = gox.auth('BTCUSD/money/trades/fetch',{'since':str(time_since_gox)})
#print json.dumps(r.json(), sort_keys = True, indent=4, separators=(',', ': '))
j = r.json()

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
'''

#Account / Wallet Info
time.sleep(10)
r = gox.auth('BTCUSD/money/info',{})
#print json.dumps(r.json(), sort_keys = True, indent=4, separators=(',', ': '))
j = r.json()
#print j['data'].keys()
btc_bal = D.Decimal(j['data']['Wallets']['BTC']['Balance']['value_int'])/100000000
usd_bal = D.Decimal(j['data']['Wallets']['USD']['Balance']['value_int'])/100000
print 'BTC Balance: ', btc_bal
print 'USD Balance: ', usd_bal
print ''

'''

'''

#Get a spot quote to BUY BTC with USD
time.sleep(10)
btc_to_buy = input('How many BTC to Buy?')
r = gox.auth('BTCUSD/money/order/quote',{'type':'bid','amount':btc_to_buy*100000000})
#print json.dumps(r.json(), sort_keys = True, indent=4, separators=(',', ': '))
j = r.json()
print 'USD Cost: $' + str(D.Decimal(j['data']['amount'])/100000)
print '' 

'''
'''

#Get a spot quote to SELL BTC for USD
time.sleep(10)
btc_to_sell = input('How many BTC to Sell?')
r = gox.auth('BTCUSD/money/order/quote',{'type':'ask','amount':btc_to_sell*100000000})
#print json.dumps(r.json(), sort_keys = True, indent=4, separators=(',', ': '))
j = r.json()
print 'USD Income: $' + str(D.Decimal(j['data']['amount'])/100000)
print ''

'''
'''

#Pull in Trade History
#time.sleep(10)
r = gox.auth('BTCUSD/money/wallet/history',{'currency':'USD'})
print json.dumps(r.json(), sort_keys = True, indent=4, separators=(',', ': '))
j = r.json()

print 'Total Records: ', j['data']['records']

records = j['data']['result']
x = 0
for record in records:
	
	pprint(j['data']['result'][x]['Info'])
	print'TID:   ', j['data']['result'][x]['Trade']['tid']
	print'UUID:  ', j['data']['result'][x]['Link'][0]
	print'Type:  ', j['data']['result'][x]['Type']
	print'Value: ', j['data']['result'][x]['Value']['value']
	print'Currency Out: ', j['data']['result'][x]['Trade']['Amount']['currency']
	print'Amount Out: ', j['data']['result'][x]['Trade']['Amount']['value']
	print'Price :', round(D.Decimal(j['data']['result'][x]['Value']['value'])/D.Decimal(j['data']['result'][x]['Trade']['Amount']['value']),5)

	x = x + 1
	print ''

'''

'''
time.sleep(10)
r = gox.auth('BTCUSD/money/depth/fetch',{})	

#print json.dumps(r.json(), sort_keys = True, indent=4, separators=(',', ': '))
j = r.json()

print ['stamp','price','amount']
x = 0
for item in j['data']['asks']:
	print [time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(D.Decimal(j['data']['asks'][x]['stamp'])/1000000)),j['data']['asks'][x]['price'],j['data']['asks'][x]['amount']]
	x+=1
x = 0
for item in j['data']['bids']:
	print [time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(D.Decimal(j['data']['bids'][x]['stamp'])/1000000)),j['data']['bids'][x]['price'],j['data']['bids'][x]['amount']]
	x+=1

print 'Max Price: ' + j['data']['filter_max_price']['value'] #in USD
print 'Min Price: ' + j['data']['filter_min_price']['value'] #in USD
'''



