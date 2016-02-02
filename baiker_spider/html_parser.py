#coding:utf-8
import re
import urlparse
from bs4 import BeautifulSoup


class HtmlParser(object):
    def __get_new_urls(self,page_url, soup):
        new_urls = set()
        #view/123.htm
        links = soup.find_all("a",href=re.compile(r"/view/\d+\.htm"))
        for link in links:
            url = link["href"]
            full_url = urlparse.urljoin(page_url, url)
            new_urls.add(full_url)
        return new_urls
    
    
    def __get_new_data(self,page_url, soup):
        rs_data={}
        rs_data["url"]=page_url
        #<dd class="lemmaWgt-lemmaTitle-title"> <h1>Python</h1>
        title_node = soup.find("dd",class_="lemmaWgt-lemmaTitle-title").find("h1")
        rs_data["title"] = title_node.getText()
        #<div class="lemma-summary" label-module="lemmaSummary">
        summary_node = soup.find("div",class_="lemma-summary")
        rs_data["summary"] = summary_node.getText()
        
        return rs_data
    
    def parse(self,page_url,html_cont):
        if page_url is None or html_cont is None:
            return None
        soup = BeautifulSoup(html_cont,"html.parser",from_encoding="utf-8")
        new_urls = self.__get_new_urls(page_url,soup)
        new_data = self.__get_new_data(page_url,soup)
        return new_urls,new_data
    
    
    
    



