import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from markdownify import MarkdownConverter
import re
import os
from dotenv import load_dotenv
import openai
import ast


load_dotenv()

links_to_scrape: list = []

# Gets markdown-formatted text from a given url
def scrape_url(url):
    
    """ Scrape a url and return the scraped content
        Args:
            url (str): The url to scrape
            domain (str): The root domain of the url
        Returns:
            dict: A dictionary containing the url and scraped content
    """
    # follow redirect, if there is one
    url = requests.get(url).url

    print(f"Scraping {url}...")
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    # get the page title
    title = soup.find('title').text
    content = html_to_md(soup, url)

    # print the content
    # with open('/Users/timco/Documents/VS Code/Personal/gpt-scraper/files/scraped_content.md', 'w+') as f:
    #     f.write(content)
    #     f.flush()
    #     print("Scraped content written to file.")

    # cut the content to 25,000 chars
    content = content[:25000]

    # clean the content
    try:
        cleaned_content = clean_data(content)
    except:
        cleaned_content = content

    return f"# {title}\n\nPage URL: {url}\n\n#scraped\n\n{cleaned_content}"

# Make sure the link doesn't 404
def validate_link(link):
    """Follow redirects if applicable and check that it fits the root domain"""
    response = requests.get(link)

    # follow redirect if applicable
    link = response.url

    # confirm that its not a 404 error
    if response.status_code == 404:
        return None
    
    return link

# Convert relative image paths to absolute paths
def convert_relative_image_paths(text, root_domain):
    """ Given the markdown, convert image path to absolute path """

    # Find all text that matches the pattern: ![alt text](../path/to/image.png)
    pattern = r'\!\[(.*?)\]\((.*?)\)'
    matches = re.findall(pattern, text)

    for match in matches:
        alt_text, image_path = match
        if not image_path.startswith('http'):
            # remove ../ if applicable
            image_path = image_path.replace('../', '')
            new_path = root_domain + '/' + image_path
            text = text.replace(image_path, new_path)

    return text

# Create shorthand method for conversion
def md(soup, **options):
    return MarkdownConverter(**options).convert_soup(soup)

# Convert html to markdown
def html_to_md(soup: BeautifulSoup, url: str):

    # Remove some tags
    for tag in soup.find_all(['style', 'script', 'nav', 'footer', 'head', 'title']):
        tag.decompose()
    
    # Remove header links
    tags_to_remove = soup.find_all(class_="headerlink")
    for tag in tags_to_remove:
        tag.decompose()


    # convert to md using Markdownify
    text = md(soup, escape_underscores=False, code_language='python')

    # compress newlines in output
    pattern = r"\n{3,}"
    replacement = "\n\n"
    text = re.sub(pattern, replacement, text)

    # Remove anything between brackets that's longer than 20 chars
    pattern = r"[\[\<\>\(\)](.{20,}?)[\[\<\>\(\)]"
    replacement = ""
    text = re.sub(pattern, replacement, text)

    # take out #.
    pattern = r"#."
    replacement = ""
    text = re.sub(pattern, replacement, text)

    # Convert image paths
    try:
        # Get root domain of a url with regex
        pattern = r"(https?:\/\/)?(www\.)?([\w-]+\.)*([\w-]+)(\/[\w-]+)*\/?"
        root_domain = re.search(pattern, root_domain).group(0)
        text = convert_relative_image_paths(text, root_domain)
    except:
        pass

    return text

# Ask GPT-4 to clean the markdown
def clean_data(scraped_data):
    """ Ask GPT-4 to clean the markdown """
    openai.organization = os.getenv("OPENAI_ORG")
    openai.api_key = os.getenv("OPENAI_API_KEY")

    print("Cleaning scraped content with GPT-4...")

    # use the openai python package to generate a chat completion
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": f"""
                    You are a data parser that helps people convert messy data into clean readable markdown.

                    Your users will employ a series of re.sub() function calls in python to clean the data. 

                    Please return a list of tuples [(a1,b1),(a2,b2)...] such that users can call re.sub() on each tuple like this: 

                    re.sub(a1, b1, scraped_data)
                    re.sub(a2, b2, scraped_data)
                    ... and so on

                    Make sure your response is a valid python list

                    Example response:
                    [(r'(?<!\n)\n(?!\n)', r' '),(r'\n{2,}', r'\n\n')]
                """
            },
            {
                "role": "user", 
                "content": f"""
                    {scraped_data}
                """
            },

        ]
    )

    replacements = completion.choices[0].message.content
    replacements = ast.literal_eval(replacements)

    print(replacements)

    for pattern, replacement in replacements:
        try:
            scraped_data = re.sub(pattern, replacement, scraped_data)
        except:
            pass

    return scraped_data
