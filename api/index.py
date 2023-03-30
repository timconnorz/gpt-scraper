from flask import Flask, request
from src.main import scrape_url

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

# scrape route that calls the src/scrape.py script with a url string parameter
@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.form.get('url')

    # get the scraped & cleaned result
    cleaned_content = scrape_url(url)

    # with open('/Users/timco/Documents/VS Code/Personal/gpt-scraper/files/cleaned_content.md', 'w+') as f:
    #     f.write(cleaned_content)
    #     f.flush()
    #     print("Cleaned content written to file.")

    return cleaned_content
