import re


tlds = []

with open("data/TLDs.dat") as f:
    for tld in f:
        tlds.append(tld.replace("\n", ""))


def find_domain(link):

    # Replace common url parts
    link = re.sub("|".join(['www.', 'https://', 'http://', '\n']), "", link)
    domain = re.search('[^/]*', link).group(0)

    return domain

def clear_duplicates(urls):

    global tlds
    no_duplicates = []  # Contains links with unique domains
    # Contains domains of links, that are already included in no_duplicates
    # list
    seen_domains = []

    for url in urls:
        domain_parts = find_domain(url).split(".")
        domain_parts = set(domain_parts) - set(tlds)
        for domain in domain_parts:
            if domain not in seen_domains:
                no_duplicates.append(url)
                seen_domains.append(domain)
    return no_duplicates

def clear_non_links(urls):

    links = []  

    
    for url in urls:
        if not (re.search('javascript:', url) or re.search('mailto', url) or re.search('\(', url) or re.search('<', url) or re.search('sms:', url)) and url.count('http') == 1:
            links.append(url)
    return links

def clear_cdn_and_multimedia_links(urls):

    links = []  

    for url in urls:
        if not (  re.search('cdn', url) or re.search('.pdf', url) or re.search('.png', url) 
               or re.search('.gif', url) or re.search('.jpg', url) or re.search('.jpeg', url) 
            ):
            links.append(url)
    return links

def clear_utm_source_parts(urls):

    links = []
    for url in urls:
        if re.search('utm_source\%5F', url) or re.search('utm_', url):
            if re.search("\%3F", url):
                links.append(url.split('%3F',1)[0])
            else:
                links.append(url.split('?',1)[0])
        else:
            links.append(url)
    
    return links

def clear_gr_links(urls):
    links = []
    for url in urls:
        if not re.search('\.gr/', url):
            links.append(url)
    return links

links = []
with open("data/non_phishing_urls.dat") as c:
    for url in c:
        if re.search('http://', url) or re.search('https://', url):
            if len(url) > 6:
                links.append(url)


links = clear_duplicates(links)
links = clear_non_links(links) 
links = clear_cdn_and_multimedia_links(links) 
links = clear_utm_source_parts(links) 
links = clear_gr_links(links) 

with open("data/non_phishing_urls.dat", "w") as f:
    f.write('')

with open("data/non_phishing_urls.dat", "a") as f:
    for url in links:
        f.write(url)

print(len(links))
