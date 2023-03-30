# GPT-Scraper

Takes in a url, scrapes it with Beautiful Soup, cleans the output with GPT-4

Instead of passing in the entire scraped page, it asks GPT-4 to produce re.sub()
function calls that will clean the scraped content. 

We then run the suggested re.sub() calls against the scraped_content to get
the cleaned_content. Both can be printed to markdown files so you can see the
difference (uncomment the "with open()..." lines)

Organized as a flask app so you can deploy it for your own purposes. 
vercel.json is also included so you can deploy to vercel.

Archive.py contains some other functions that may be useful for folks looking
to expand upon this functionality.

### Required Env Variables:
- OPENAI_API_KEY: the api key from openai
- OPENAI_ORG: your assigned org id


### To Run

To run locally, type:
`flask --app api.index run`

To deploy to vercel type
`vercel dev`
to get started

To call the scrape function 
GET: "<host>/scrape" with a 'url' form parameter


### The Prompt

Here's what I used as the chat prompt to GPT-4
```python
{
    "role": "system",
    "content": """
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
}
```