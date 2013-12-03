from ScraperClass import Scraper
import time

'''
Pull in trade history of a currency pair, BTCUSD in this case
-Will only pull 1000 rows at a time because that is the MTGOX API limit, may need to loop through several times
'''

start = time.mktime(time.gmtime())  #MTGOX server is on UTC
end = start

scrape = Scraper() #initiate scraper object

#loop through updates every 15 sec for 5 hours
#while ((end-start)/60/60) < 5: #run for 5 hours

#end = time.mktime(time.gmtime())

#in case we received more than 1000 trades, loop through
rows_added = 1000
while rows_added >= 1000:
	#scrape the trades from MtGox and return the number of trades inserted
	rows_added = scrape.Scrape_gox_trades() 
	time.sleep(15) #give us a gap between API calls

#time.sleep(200)
#Force stop the script after so many hours
#if end > 1385572448: #approx 5.5 hours from 1385531332 (20,000 seconds more)
#	break