from lxml import html
import requests
import urllib2
import fileinput
import urllib2
from urlparse import urlparse
from bs4 import BeautifulSoup
import unicodedata


def fetch_css( url ):

	try:
		response = urllib2.urlopen(url)
		html_data = response.read()
		response.close()

		soup = BeautifulSoup(''.join(html_data), "lxml")

		# Find all external style sheet references
		ext_styles = soup.findAll('link', rel="stylesheet")
		print ext_styles

		# Find all internal styles
		int_styles = soup.findAll('style', type="text/css")

		# TODO: Find styles defined inline?
		# Might not be useful... which <p style> is which?

		# Loop through all the found int styles, extract style text, store in text
		# first, check to see if there are any results within int_styles.
		int_css_data = ''
		int_found = 1
		if len(int_styles) != 0:
			for i in int_styles:
				print "Found an internal stylesheet"
				int_css_data += i.find(text=True)
		else:
			int_found = 0
			print "No internal stylesheets found"

		# Loop through all the found ext stylesheet, extract the relative URL,
		# append the base URL, and fetch all content in that URL
		# first, check to see if there are any results within ext_styles.
		ext_css_data = ''
		ext_found = 1
		if len(ext_styles) != 0:
			for i in ext_styles:
				# Check to see if the href to css style is absolute or relative
				o = urlparse(i['href'])
				print o
				if o.scheme == "":
					css_url = url + '/' + i['href']  # added "/" just in case
					print "Found external stylesheet: " + css_url
				else:
					css_url = i['href']
					print "Found external stylesheet: " + css_url

				response = urllib2.urlopen(css_url)
				ext_css_data += response.read()
				response.close()
		else:
			ext_found = 0
			print "No external stylesheets found"

		# Combine all internal and external styles into one stylesheet (must convert
		# string to unicode and ignore errors!
		# FIXME: Having problems picking up JP characters:
		# I already tried ext_css_data.encode('utf-8'), but this didn't work
		all_css_data = int_css_data + unicode(ext_css_data, errors='ignore')
		return all_css_data
	except:
		return ""


def main():
	website7 = 'http://www.shirleys-wellness-cafe.com'
	website6 = 'http://www.buienradar.nl' #GOOD
	website5 = 'http://maningray.com' #GOOD!
	website = 'http://www.getcrafty.com' #VERY GOOD!
	website3 = 'http://www.peacemagazine.org' #GOOD! 
	website2 = 'http://www.oed.com'
	website1 = 'http://python.org'
	#Open a url and read the HTML data
	response = urllib2.urlopen(website)
	data = response.read()
	head_index = data.find('<head>') + len('<head>')
	
	#Get CSS
	css_try = fetch_css(website)
	nkfd_form = unicodedata.normalize('NFKD', css_try)
	css = nkfd_form.encode('ASCII', 'ignore')
	print css

	#Insert CSS after head_index + len('<head>')
	complete_data = data[:head_index] + '<style type="text/css">'  + css  + '</style>' + data[head_index:]

	#Save HTML source to a txt file
	html_file = open("file.txt","wb") #open file in binary mode
	html_file.writelines(complete_data)
	html_file.close()


if __name__ == '__main__':
	main()