from MtgoxClass import Mtgox
import json, time, decimal as D
from pprint import pprint

gox = Mtgox() #create instance of mtgox obj



#Ticker
r = gox.auth('BTCUSD/money/ticker',{})
#print json.dumps(r.json(), sort_keys = True, indent=4, separators=(',', ': '))
j = r.json()
#print j['data'].keys() #get members of dict branch
print time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(D.Decimal(j['data']['now'])/1000000)) 
print 'avg: ' + j['data']['avg']['value']
print 'buy: ' + j['data']['buy']['value']
print 'sell: ' + j['data']['sell']['value']
print 'high: ' + j['data']['high']['value']
print 'low: ' + j['data']['low']['value']
print 'vol: ' + j['data']['vol']['value']
print 'vwap: ' + j['data']['vwap']['value']
print ''
print 'End of Test'
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



