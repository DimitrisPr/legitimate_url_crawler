from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import requests
import re
import random
import pandas as pd
import time
import string
import random

random_query_words = "enter random words here"

visited_domains = ["wiki", "mailto", "stack", ".mp4", ".mp3" , "google", "reddit", "youtube", "twitter", "png", "jpg", "jpeg", "gif", "linkedin", "facebook", "instagram", "pinterest", "gr"]
written = 0

# Recursive function
def main(query):
    global written, visited_domains, random 
    
    # retrieve the number of legitmate links already crawled
    written = file_len("data/non_phishing_urls.dat")
    print("Collected {} links".format(written))

    # make a random query at google
    links = getWebpageLinks("https://www.google.com/search?q={}".format(query))
    
    # for every crawled link
    for url in links:
        try:
            # if link is not in a common or a visited domain such as google, youtube etc (and if link extension is not jpg, mp4, mp3 etc)
            if not any(r_word in url for r_word in visited_domains): 

                # save link domain to visited domains
                last = find_domain(url)
                visited_domains.append(last)
                
                # crawl all the links or the webpage and clear the duplicates 
                links += getWebpageLinks(url)
                links = clear_duplicates(links)        

                if written > 35000:
                    break
        except:
            pass
    
    # append crawled links to file
    with open("data/non_phishing_urls.dat", "a") as crawled:
        for url in links:
            print(url)
            crawled.write(url + "\n")

    # generate random google query
    query = random.choice(random_query_words.split()) + " " + random.choice(random_query_words.split()) + " " + random.choice(random_query_words.split())

    # recursive function repeat/termination condition
    if written < 35000:
        main(query)
    else:
        exit()

def find_domain(link):

    # Replace common url parts
    link = re.sub("|".join(['www.', 'https://', 'http://', '\n']), "", link)
    domain = re.search('[^/]*', link).group(0)

    return domain

def clear_duplicates(urls):

    no_duplicates = []  # Contains links with unique domains
    # Contains domains of links, that are already included in no_duplicates
    # list
    seen_domains = []
    for URL in urls:
        domain = find_domain(URL)
        if domain not in seen_domains:
            no_duplicates.append(URL)
            seen_domains.append(domain)

    return no_duplicates

# crawls website, and collects all the links contained in <a href="..."> tags
def getWebpageLinks(url):
    print('trying {}'.format(url))
    global visited_domains 

    links = []
    try:
        response = requests.get(url, timeout = 2)
        http_encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
        html_encoding = EncodingDetector.find_declared_encoding(response.content, is_html=True)
        encoding = html_encoding or http_encoding
        soup = BeautifulSoup(response.content, from_encoding=encoding, features="html.parser")
        for link in soup.find_all('a', href=True):
            if not any(r_word in link for r_word in visited_domains): #if url has none of the restrixted extensions/domains
                links.append(link['href'].replace('/url?q=', '').split("&sa", 1)[0])
        links = clear_duplicates(links)
        links = keep_valid(links)
    except:
        pass
    return links

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

# function to filter only links (href could also contain 'mailto:' or local URI's etc)
def keep_valid(links):
    valid_urls = []
    for url in links:
        if re.search('http://', url) or re.search('https://', url):
            valid_urls.append(url)

    return valid_urls

def file_len(fname):
    import subprocess
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE, 
                                            stderr=subprocess.PIPE)
    p = subprocess.Popen(['python3', 'scripts/legitmate_url_preprocessing.py'], stdout=subprocess.PIPE, 
                                            stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])

main("")
