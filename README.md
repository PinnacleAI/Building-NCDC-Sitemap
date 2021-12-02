# Building Sitemap for NCDC Website

***Having a sitemap for your website is a MUST! - SEO Experts***.  Not only does it makes it easier for search engines to find and crawl your website efficiently, it makes it useful for people searching for a specific page on your website. Sitemap also helps in structuring your websites.

During my visit to the Nigeria Center for Disease Control (NCDC), I discovered that the website doesn't have a sitemap, and in my attempt build one I made some important discoveries.

1) The website was superbly structured and,
2) They were over 10 invalid website or download links (most of the errors was discovered in download links)

The code for the sitemap is divided into two part: 

* The XMLParser: This part handles everything from creating Element and SubElement, to saving the ElementTree to a file (it saves the file in xml file format).
* The Spider: It contains the crawler that will move through the website and retrieving the internal links. The links are of two form (absolute and relative link)
