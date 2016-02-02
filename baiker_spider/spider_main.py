#coding:utf-8
from baiker_spider import url_manager, html_parser, html_downloader,\
    html_outputer

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManger()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutPuter()
    def craw(self, root_url): 
        count = 1
        self.urls.add_new_url(root_url)
        while(self.urls.hasUrl()):
            try:
                new_url = self.urls.getUrl()
                print "crow %d : %s" % (count,new_url)
                html_cont = self.downloader.download(new_url)
                new_urls,new_data = self.parser.parse(new_url,html_cont)
                self.urls.addNewUrls(new_urls)
                self.outputer.collect_data(new_data)
                if(count == 1000):
                    break
                count = count + 1
            except  Exception:
#                 raise
                print "craw failed"
        self.outputer.output_html()

if __name__=="__main__":
    root_url="http://baike.baidu.com/item/python"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)