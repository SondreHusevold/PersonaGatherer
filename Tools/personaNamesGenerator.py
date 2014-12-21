import sys
from urllib2 import urlopen, URLError
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from lxml import etree

def main():
    url = 'http://apps.evilrobotstuff.com/persona4/fusion.php'

    # Make soup
    try:
        resp = urlopen(url)
    except URLError as e:
        print 'An error occured fetching %s \n %s' % (url, e.reason)   
        return 1
    soup = BeautifulSoup(resp.read())

    # Get persona names
    for link in soup.find_all('option'):
    	print link.string

if __name__ == '__main__':
    status = main()
    sys.exit(status)