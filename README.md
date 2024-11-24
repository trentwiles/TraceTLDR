# Trace TL;DR
Don't have time to search through Trace? Get a quick of any Northeastern professor.
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
# cookies - the cookies list for trace, see "How to Get Trace Cookies"
# mongo - MongoDB connection string
# gemini- Your Google Gemini API Key

# Scrape the data and upload to mongo, takes a few hours
screen python3 run.py

# Run the web server in dev mode
python3 server.py
```