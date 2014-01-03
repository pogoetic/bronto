from ScraperClass import Scraper
import time, argparse, sys

'''
Pull in trade history of a currency pair, BTCUSD in this case
-Will only pull 1000 rows at a time because that is the MTGOX API limit, may need to loop through several times
'''

parser = argparse.ArgumentParser(description='Input an override mtgox TID for the scraper to begin at, use unix microtimestamps only')
parser.add_argument('--tid', type=int, nargs='+',
                   help='a starting TID from which to scrape mtgox trades in UNIX Microtime')
args = parser.parse_args()

start = time.mktime(time.gmtime())  #MTGOX server is on UTC
end = start

scrape = Scraper() #initiate scraper object

i=0
#loop through updates every 15 sec for 5 hours
while ((end-start)/60/60) < 5: #run for 5 hours

	#end = time.mktime(time.gmtime())
	end = start #this will force run indefinitely
	#in case we received more than 1000 trades, loop through
	rows_added = 1000
	while rows_added >= 1000:
		i+=1 #count number of loops
		#scrape the trades from MtGox and return the number of trades inserted
		if args.tid and i=1:
			if len(str(args.tid[0]))!=16:
				print "Incorrect TID length - must be a UNIX Microtime of length 16"
				sys.exit()
			rows_added = scrape.Scrape_gox_trades(tidoverride=args.tid[0])  #tidoverride=1369326824470988		
		elif args.tid and i>1:
			print 'I have already run 1 tidoverride iteration'
			#user max rowid to get "last row inserted" and go from there
		else: 
			rows_added = scrape.Scrape_gox_trades()
		time.sleep(15) #give us a gap between API calls

	#time.sleep(200)
	#Force stop the script after so many hours
	#if end > 1385572448: #approx 5.5 hours from 1385531332 (20,000 seconds more)
	#	break