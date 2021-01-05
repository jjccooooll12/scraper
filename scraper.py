from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import requests
import argparse
import re

class Scraper():
    
    def get_all_urls(self, url):
        """
        check for all the internal links of an url
        """
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        a_tags = soup.findAll("a", href=True)
        if not url.endswith("/"):
            url += "/"
        links = [url[:-1]+tag['href'] if not tag['href'].startswith("http") else tag["href"] for tag in a_tags]
        links.append(url)
        return set(links)
    
    
    def scrape_url(self, url):
        """
        Returns all texts from div sections from input url
        """
        divs_text = []
        try:
            print(f"Scraping {url}")
            page = requests.get(url)
            # we neeed to set the right encoder otherwise special characters are lost
            html_encoding = EncodingDetector.find_declared_encoding(page.content, is_html=True)
            encoding = page.encoding if 'charset' in page.headers.get('content-type', '').lower() else html_encoding
            soup = BeautifulSoup(page.content, 'html.parser', from_encoding=encoding)
            divs = soup.find_all('div')
            for div in divs:
                divs_text.append(div.get_text())
        except:
            print(f"Can't connect to {url}")
            pass
        
        return divs_text
    
    
    
    def scrape_urls(self, urls):
        urls_text = []
        for url in urls:
            scraped_url = self.scrape_url(url)
            if scraped_url:
                urls_text.append(scraped_url)
        flat_urls_text = set([flat_list for sub_list in urls_text for flat_list in sub_list])
        return flat_urls_text
    
        
    
    def main(self, url, output_filepath):
        """
        given an url it scrapes all the connected links and return an output text file with the scraped content
        """
        request = requests.get(url)
        if request.status_code == 200:
        
            all_urls = self.get_all_urls(url)
            urls_text = self.scrape_urls(all_urls)

            # writing text to a file
            for line in urls_text:
                if line != "":
                    with open(output_filepath, 'a') as f:
                        f.write(line.strip() + "\n")
        else:
            raise Exception (f"{url} is not a valid url") 

            
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
       description="A tool to scrape websites")
    parser.add_argument("-u", "--url", help="A website to scrape")
    parser.add_argument("-o", "--output", help="Name of the output file", default="output.txt")
    args = parser.parse_args()
    url = args.url
    if not url:
        raise Exception ("Please provide a valid url") 
    output = args.output
    print("Loading a scraper...")
    scraper = Scraper()
    print("Loaded scraper...")
    scraper.main(url, output)
    
