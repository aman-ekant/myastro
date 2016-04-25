#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
import lxml
import sqlite3

conn = sqlite3.connect('scrap.db')
c = conn.cursor()
c.execute('''CREATE TABLE scrap
             (UserID text, Name text, Company test, Email text, Phone text, Mobile text, Profession text, Keywords text, Address text, City text, State text, Country text, ZipCode text )''')

login_page = "https://www.bniconnectglobal.com/web/open/login/web/j_spring_security_check"
sess = requests.session()
resp = sess.post(login_page, {"j_username": "savar", "j_password": "Savar42*"})

i=0

def main():
    for i in xrange(1,1038355):
        
        res = sess.get('https://www.bniconnectglobal.com/web/secure/networkProfile?userId={}'.format(i))
        soup = BeautifulSoup(res.content, "lxml")

        try:
            email = soup.find_all("a", {"class": "profileurl"})
            emailv = email[0].text
        except:
            pass

    
        name = soup.find_all("h1")
        namev = name[0].text
        
        phonea =soup.find('span', attrs={'class': 'clearboth'})
        try:
            for phone in soup.find_all("label", {"for": "memberPhoneNumber"}):
                phonea = phone.find('span', attrs={'class': 'fieldtext'})
            phoneb = phonea.text
        except:
            phoneb=""

        companya =soup.find('span', attrs={'class': 'clearboth'})
        try:
            for company in soup.find_all("label", {"for": "memberCompanyName"}):
                companya = company.find('span', attrs={'class': 'fieldtext'})
            companyb = companya.text
        except:
            professionb=""

        mphonea =soup.find('span', attrs={'class': 'clearboth'})
        try:
            for mphone in soup.find_all("label", {"for": "memberMobileNumber"}):
                mphonea = mphone.find('span', attrs={'class': 'fieldtext'})
            mphoneb = mphonea.text
        except:
            mphoneb=""

        professiona =soup.find('span', attrs={'class': 'clearboth'})
        try:
            for profession in soup.find_all("label", {"for": "memberPrimaryCategory"}):
                professiona = profession.find('span', attrs={'class': 'fieldtext'})
            professionb = professiona.text
        except:
            professionb=""

        keywordsa = soup.find('span', attrs={'class': 'clearboth'})
        try:
            for keywords in soup.find_all("label", {"for": "memberKeywords"}):
                keywordsa = keywords.find('span', attrs={'class': 'fieldtext'})
            keywordsb = keywordsa.text
        except:
            keywordsb=""

        addressa = soup.find('span', attrs={'class': 'clearboth'})
        try:
            for address in soup.find_all("label", {"for": "memberAddressLine1"}):
                addressa = address.find('span', attrs={'class': 'fieldtext'})
            addressb = addressa.text
        except:
            addressb=""

        citya = soup.find('span', attrs={'class': 'clearboth'})
        try:
            for city in soup.find_all("label", {"for": "memberCity"}):
                citya = city.find('span', attrs={'class': 'fieldtext'})
            cityb = citya.text
        except:
            cityb=""

        statea = soup.find('span', attrs={'class': 'clearboth'})
        try:
            for state in soup.find_all("label", {"for": "memberState"}):
                statea = state.find('span', attrs={'class': 'fieldtext'})
            stateb = statea.text
        except:
            stateb=""

        countrya = soup.find('span', attrs={'class': 'clearboth'})
        try:
            for country in soup.find_all("label", {"for": "memberCountry"}):
                countrya = country.find('span', attrs={'class': 'fieldtext'})
            countryb = countrya.text
        except:
            countryb=""

        zipa = soup.find('span', attrs={'class': 'clearboth'})
        try:
            for zipcode in soup.find_all("label", {"for": "memberZipCode"}):
                zipa = zipcode.find('span', attrs={'class': 'fieldtext'})
            zipb = zipa.text
        except:
            zipb=""
   

        c.execute("INSERT INTO scrap (UserID, Name, Company, Email, Phone, Mobile, Profession, Keywords, Address, City, State, Country, ZipCode) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",(i, namev, companyb, emailv, phoneb, mphoneb, professionb, keywordsb, addressb, cityb, stateb, countryb, zipb))

        conn.commit()
        
    conn.close()

if __name__ == '__main__':
    main()