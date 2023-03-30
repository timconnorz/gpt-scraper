
#####

# # Grab all links on a page
# def get_links(page_url, root_domain):
#     page_url = validate_link(page_url, root_domain)
#     if page_url == None: return []

#     response = requests.get(page_url)
#     soup = BeautifulSoup(response.content, 'html.parser')
    

#     # find all anchor tags on the page
#     links = soup.find_all('a')

#     # extract the href attribute from each anchor tag
#     hrefs = [link.get('href') for link in links]
#     # filter out None and empty hrefs
#     hrefs = [href for href in hrefs if href is not None and href != '']
#     # convert relative URLs to absolute URLs
#     hrefs = [urljoin(page_url, href) for href in hrefs]
#     # chop off the anchor portion of the URL
#     hrefs = [href.split('#')[0] for href in hrefs]
#     # filter out URLs that do not include the root domain
#     hrefs = [href for href in hrefs if root_domain in href]
#     # remove duplicate URLs
#     hrefs = list(set(hrefs))
#     # remove urls that are already in links_to_scrape
#     hrefs = [href for href in hrefs if href not in links_to_scrape]

#     # print the list of href strings:
#     for href in hrefs:
#         print(f"found: {href}")
    
#     return hrefs


# grab the data
# def scrape_domain(root: str, site_id: str) -> list:
#     """Scrape a domain and return the scraped content
#         Args:
#             root (str): The root domain to scrape
#         Returns:
#             list: A list of dictionaries containing the url and scraped content
#     """
#     global links_to_scrape

#     scraped_content = []

#     # add root domain, follow redirect if applicable 
#     links_to_scrape.append(root)

#     # Get Sitemap
#     sitemap_url = f"{root}/sitemap.xml"

#     # Add sitemap links to links_to_scrape
#     links_to_scrape.extend(get_links(sitemap_url, root))

#     # Grab as many unique links as possible
#     for url in links_to_scrape:
#         links_to_scrape.extend(get_links(url, root))
       
#     # scrape each link
#     count = 0
#     for url in links_to_scrape:

#         # scrape the page
#         scraped_page = scrape_url(url, root)


#     return count
