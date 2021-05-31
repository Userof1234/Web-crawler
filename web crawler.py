import requests
from urllib.parse import urlparse, urljoin 
from bs4 import BeautifulSoup
import colorama
import argparse

#using argparse library to parse argument in command line 

parser = argparse.ArgumentParser()
parser.add_argument("url")
args = parser.parse_args()

#using colorama library for using different colors when printing, to distinguish between internal and external links

# init the colorama module
colorama.init()
GREEN = colorama.Fore.GREEN
magenta = colorama.Fore.MAGENTA
RESET = colorama.Fore.RESET


# initializing the set of unique links

internal_urls = set() #For Urls that links to other pages of the same website
external_urls = set() #For Urls that leads us to other websites

#defining a method to check whether url is valid or not

def is_valid(url):
    
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

# Defining a method to find all links in a single webpage 

def get_all_website_links(url):
   
    urls = set()

    # domain name of the URL without the protocol
    
    domain_name = urlparse(url).netloc
    html_content =  requests.get(url).content
    soup = BeautifulSoup(html_content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # joining the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print(f"{magenta}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls        

# number of urls visited so far will be stored here
total_urls_visited = 0

def crawl(url, max_urls=80):
    """
    Crawls a web page and extracts all links.
    
    """
    global total_urls_visited
    total_urls_visited += 1
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)

crawl(args.url)