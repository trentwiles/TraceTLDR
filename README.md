# Trace TL;DR
Don't have time to search through Trace? Get a quick of any Northeastern professor.

Try it out: [trace.trentwiles.com](https://trace.trentwiles.com/?utm_source=github)

# How it Works

* First, all Khoury classes are scraped from Trace
* Second, all comments made on each class are scraped, along with the name of the professor
* Third, all comments placed under their respective professor
* Fourth, Google Gemini summarizes the positive comments and the critical comments into five words

# Installation

```shell
# Download dependencies
pip3 install -r requirements.txt

# Copy the Template .env
cp .env.example .env

# Add all required variables to .env
# cookies - the cookies list for trace, see "How to Get Your Trace Cookies"
# mongo - MongoDB connection string
# gemini- Your Google Gemini API Key

# Scrape the data and upload to mongo, takes a few hours
screen python3 run.py

# Run the web server in production mode on port 8000
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

## How to Get Your Trace Cookies

1. [Log into Trace](https://www.applyweb.com/eval/shibboleth/neu/36892)
2. Open dev tools/inspect element, and access the "Network" tab
3. Reload
4. Click the first request
5. Copy the value of "Cookie" under request headers, and paste that into the `.env`, under `cookies`

![](https://trentwil.es/a/u9nZeo7qF5.png)