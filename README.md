# YahooAnswersScraper
A Python scraper for Yahoo Answers using Selenium, BeautifulSoup, and SQLite.
As of now, only gets questions from an entered URL, with the option to get all the questions' descriptions.

Clone this repo or download the files to use, then follow the usage section.

## Usage
`python ya_scraper.py --url <URL> --get_descriptions`

The URL is the Yahoo Answers category page, such as Sports.
The `get_descriptions` flag is optional, passing it will enable getting each question's description.
