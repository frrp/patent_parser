#!/usr/bin/python

import urllib2

o = urllib2.build_opener( urllib2.HTTPCookieProcessor() )

remoteFileUrl = 'http://storage.googleapis.com/patents/grant_full_text/2014/ipg140107.zip'

## lets create a variables for year and week (in this case it is 2014 and 140107)

#def getUrl(year, week):
#	url = 'http://storage.googleapis.com/patents/grant_full_text/ %year/ipg %week.zip'
#	return url

def downld(remoteFileUrl):
	f = o.open(remoteFileUrl)
	localFile = open('localFile', "wb")

	while 1:
	   packet = f.read()
	   if not packet:
	      break
	   localFile.write(packet)
	f.close()


def main():
#	yrange = 
#	wrange = 
#	for year in yrange:
#		for week in wrange:
#			remoteFileUrl = getUrl(year, week)
			downld(remoteFileUrl)


main()
