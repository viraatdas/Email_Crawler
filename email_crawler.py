from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import requests.exceptions
import pickle

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

term_key = ['ncrna', 'mrna']
#term_key = ['lncrna']
email = pickle.load(open("curr_email3.pkl",'rb'))
url = "https://www.ncbi.nlm.nih.gov/pubmed/"
sleep_constant = 0.7

initial_start_page = 500
# Config for web driver
options = Options()
options.headless = True
file1 = open("page_indicator.txt","a") 
def add_email(new_url):
    try:
        response = requests.get(new_url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        # ignore pages with errors
        return

    # extract all email addresses and add them into the resulting set
    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
    email.update(new_emails)

# Returns name page as well as adds email to the set
slice_len = len("/pubmed/")
def get_page(soup):
    for link in soup.findAll('a', attrs={'href': re.compile("/pubmed/")}):
        key = link.get('href')[slice_len:]
        try:
            key = int(key)
        except:
            continue

        new_url = url + str(key)
        add_email(new_url)

for term in term_key:
    term_url = url + "?term=" + term
    html_page = urlopen(term_url)

    soup = BeautifulSoup(html_page)

    # get num_page
    for foo in soup.find_all('h3', attrs={'class': 'page'}):
        bar = foo.find(attrs={'class': 'num'})
        num_page = int(bar["last"])

    get_page(soup)

    # Navigating to next pages
    browser = webdriver.Chrome("/Users/owner/Documents/chromedriver", options=options)

    browser.get(term_url)
    # Wait until page is loaded
    time.sleep(sleep_constant)

    next_button_id = "EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_Pager.Page"
    for page in range(initial_start_page, num_page+1):
	
        if page % 10 == 0:
            pickle.dump(email, open("curr_email3.pkl",'wb'))

        browser.find_element_by_id('pageno').clear()
        input_el = browser.find_element_by_id("pageno")
        input_el.send_keys(str(page))
        input_el.send_keys(Keys.ENTER)
        time.sleep(sleep_constant)

        content = browser.page_source.encode('ascii', 'ignore').decode("utf-8")
        get_page(BeautifulSoup(content))
        file1.write(f'{term} {page}\n')

# CSV writer
import csv

with open('email2.csv', 'w') as email_file:
    email_writer = csv.writer(email_file, delimiter=',')

    for el in email:
        email_writer.writerow([el])

