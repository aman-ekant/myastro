import mechanize
import requests
from bs4 import BeautifulSoup
import urllib2 
import cookielib

cj = cookielib.CookieJar()
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.set_cookiejar(cj)

br.open("https://www.bniconnectglobal.com/web/open/login")

br.select_form(nr=0)
br.form['j_username'] = 'savar'
br.form['j_password'] = 'Savar42*'
br.submit()

print br.response().read()