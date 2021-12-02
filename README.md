# Building Sitemap for NCDC Website

***Having a sitemap for your website is a MUST! - SEO Experts***.  Not only does it makes it easier for search engines to find and crawl your website efficiently, it makes it useful for people searching for a specific page on your website. Sitemaps also help in structuring your websites.

During my visit to the Nigeria Center for Disease Control (NCDC), I discovered that the website doesn't have a sitemap, and in my attempt to build one I made some important discoveries.

1) The website was superbly structured and,
2) They were over 10 invalid website or download links (most of the errors was discovered in download links)

The code for the sitemap is divided into two parts: 

* The XMLParser: This part handles everything from creating Element and SubElement, to saving the ElementTree to a file (it saves the file in xml file format).
* The Spider: It contains the crawler that will move through the website and retrieve the internal links. The links are of two forms namely absolute and relative link, it converts every relative link to an absolute link before passing it to the parser instance for recording.

The Scraper does the following when scraping the websites

1. Creates a sitemap.xml file containing all the links in the website.

2. Detects and count the number of invalid links present in the site.

   ​	if an invalid link is detected, it does the following:

|      | Valid links                                                  | Invalid links                                                |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 1    | Add the link to the sitemap.xml.                                 | Add the link to the sitemap.xml.                                 |
| 2    | If the link is a downloadable link set the <priority> tag to "0.8" else it will leave it at the default "0.5". | Set the link <priority> tag to "0.0" regardless of whether it is a downloadable link or not. |
| 3    | Set the <changefreq>  tag of the URL at "daily"              | set the <changefreq> tag of the URL at "never"               |
| 4    | Do not save link to a separate file                          | Save link to a separate file for easy retrieval              |
| 5    | Do not set any name attribute value of the <url> tag         | Set the name attribute value of the <url> tag to "Invalid link" |



3. Counts the number of downloadable links on the website
