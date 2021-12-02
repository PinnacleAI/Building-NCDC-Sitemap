
import os
import re
import urllib
import bs4
import requests
from bs4 import BeautifulSoup
from xml.etree import ElementTree as ET


class XMLParser:
    """Create and parse the url to xml format

    The class contains all the functionality needed to operate and/or create
    a xml file

    Parameters
    ----------
    homepage: str
        The link leading to the default home page of the website
    filepath: str (default=`sitemap`)
        The name of the file to save the formatted url xml. The extension
        .xml will be appended to the name
    """
    def __init__(self, home_page: str, filepath="sitemap"):
        self.home_page = home_page
        self.__filepath = f"{filepath}.xml"
        self.__root = None
        self.initialize_xml()

    def initialize_xml(self):
        """Initialize the XML ElementTree by creating the 
        root element"""
        self.__root = ET.Element('urlset', xmlns=self.home_page)

    def add_url(self, params, is_valid=True, parent_element=None):
        """
        Adds a url SubElement and it various SubElements 
        to it parent urlset root Element
        """

        # if the website is not accessible, indicated it as invalid
        # in the url attributes
        if not is_valid:
            element = ET.SubElement(self.__root, 'url', name="Invalid Website")
        else:
            element = ET.SubElement(self.__root, 'url')

        # raise a TypeError if url location is not specified
        if not isinstance(params, dict):
            raise TypeError("params must be of type `dict`")

        # create SubElement of the url Element
        for tag in params:
            if tag == 'loc' and params[tag] is None:
                raise ValueError(f"params['{tag}'] must not be None")

            if params[tag] is not None:
                ET.SubElement(element, tag).text = params[tag]
        
    def get_root(self) -> ET.Element:
        """Returns the root of the xml tree"""
        return self.__root

    def close(self) -> ET.ElementTree:
        """Save the xml to the specified file"""
        self.__tree = ET.ElementTree(self.__root)
        self.__tree.write(self.__filepath, xml_declaration=True)
        return self.__tree


class Spider:
    """The bot responsible for crawling through the site and 
    retrieving links for further processing

    Parameters
    ----------
    homepage: str
        The link leading to the default home page of the website
    filepath: str (default=`sitemap`)
        The name of the file to save the formatted url xml. The extension
        .xml will be appended to the name.
    header: dict
        The header details to be used when making requests
    """
    def __init__(self, homepage, filepath, header=None):
        self.homepage = homepage
        self.xml_parser = XMLParser(self.homepage, filepath)

        if header is not None:
            if not isinstance(header, dict):
                raise TypeError(f"header should be of type `dict` "
                                "instead got {type(header)}")
            self.headers = header
        else:
            self.headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
            }                                              
        self.__no_of_links = 0

    def download_page(self, url) -> BeautifulSoup:
        """Downloads the url and converts it to a BeautifulSoup object
        
        Returns
        -------
        A BeautifulSoup object if url is valid else it returns None
        """
        req = requests.get(url, headers=self.headers)
        if req.status_code == 200:
            return BeautifulSoup(req.content, 'html5lib')
        print(req.status_code)

    def extract_links(self, page):
        """Extracts all the links from the page that are either 
        absolute url or relative url of the host websites,
        external links are ignored"""

        if not page:
            return []
        return page.findAll('a', href=re.compile(f"({self.homepage})+|(^/)+"))

    def get_links(self, page_url):
        page = self.download_page(page_url)
        if page is not None:
            links = self.extract_links(page)
            return links
        return []

    def crawl(self):
        """Crawls the throughs the website, using the 
        depth-first approach"""

        from collections import deque
        visited = set()
        queue = deque()
        queue.append(self.homepage)

        while queue:
            url = queue.popleft()

            if url in visited:
                continue
            visited.add(url)

            print(url)
            params = {'loc': url, 'changefreq': 'daily'}

            # refrain from downloading files that are not html
            # eg. [.pdf, .csv, .xlsx, .docx, .doc]

            # comment this code block to reveal more errors
            # in the download links
            ext = os.path.splitext(url)[-1]
            doc_files = {".pdf", ".xlsx", ".csv", ".docx", ".doc"}
            if ext in doc_files:
                params['changefreq'] = "never"
                params['priority'] = "0.8"

                self.xml_parser.add_url(params)
                self.__counter += 1
                continue

            links = self.get_links(url)

            # if there is any error in accessing the link
            if not links:
                params['changefreq'] = "never"
                params['priority'] = "0.0"

                self.xml_parser.add_url(params, False)
                continue

            # access additional link present on this page
            # if there is no error accesing its page
            for link_tag in links:
                link = link_tag.attrs['href']
                
                # if the link is a relative import
                # convert it to a full absolute link
                if link.startswith('/'):
                    link = f"{self.homepage}{link}"
                queue.appendleft(link)

            # add the url to xml
            self.xml_parser.add_url(params)

            self.__no_of_links += 1
        print(f"Finished building sitemap of {self.__no_of_links} links")

    def close(self):
        print("Saving sitemap")
        return self.xml_parser.close()


homepage = "https://ncdc.gov.ng"
spider = Spider(homepage, "sitemap")
spider.crawl()
tree = spider.close()
