from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import re

# # a queue of urls to be crawled
#
# new_urls = deque(['https://www.ncbi.nlm.nih.gov/pubmed/?term=lncrna'])
#
# # a set of urls that we have already crawled
# processed_urls = set()
#
# # a set of crawled emails
# emails = set()
#
# # process urls one by one until we exhaust the queue
# while len(new_urls):
#
#     # move next url from the queue to the set of processed urls
#     url = new_urls.popleft()
#     processed_urls.add(url)
#
#     # extract base url to resolve relative links
#     parts = urlsplit(url)
#     base_url = url
#     path = url[:url.rfind('/') + 1] if '/' in parts.path else url
#
#     # get url's content
#     print("Processing %s" % url)
#     try:
#         response = requests.get(url)
#     except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
#         # ignore pages with errors
#         continue
#
#     # extract all email addresses and add them into the resulting set
#     new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
#     emails.update(new_emails)
#
#     # create a beutiful soup for the html document
#     soup = BeautifulSoup(response.text, features="lxml")
#
#     # find and process all the anchors in the document
#     for anchor in soup.find_all("a"):
#         # extract link url from the anchor
#         link = anchor.attrs["href"] if "href" in anchor.attrs else ''
#         # resolve relative links
#         if link.startswith('/'):
#             link = base_url + link
#         elif not link.startswith('http'):
#             link = path + link
#         # add the new url to the queue if it was not enqueued nor processed yet
#         if not link in new_urls and not link in processed_urls:
#             new_urls.append(link)


from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


term_key = ['lncrna', 'lincrna', 'ncrna', 'mrna']

email = set()
journ_key = set()
url = "https://www.ncbi.nlm.nih.gov/pubmed/"
html_page = urlopen(url + "?term=lncrna")

soup = BeautifulSoup(html_page)
slice_len = len("/pubmed/")

for link in soup.findAll('a', attrs={'href': re.compile("/pubmed/")}):
    key = link.get('href')[slice_len:]
    try:
        key = int(key)
    except:
        continue

    new_url = url + str(key)
    try:
        response = requests.get(new_url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        # ignore pages with errors
        continue

    # extract all email addresses and add them into the resulting set
    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
    email.update(new_emails)

# CSV writer
import csv

with open('email.csv', 'w') as email_file:
    email_writer = csv.writer(email_file, delimiter=',')

    for el in email:
        email_writer.writerow([el])

