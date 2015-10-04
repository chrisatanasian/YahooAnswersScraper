#!/usr/bin/python

import sys, time, os.path
import urllib2
import selenium.webdriver
import sqlite3
from bs4 import BeautifulSoup

conn = sqlite3.connect('ya.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS questions
             (text text, description text, link text,
              UNIQUE(text))''')

# Use Selenium driver to get all questions from url.
def get_questions_page(url, fname, times_to_scroll, sleep_time, days_ago):
    if not os.path.isfile(fname) or os.path.getctime(fname) < days_ago:
        driver = selenium.webdriver.Chrome()
        driver.get(url) 

        for i in range(1, times_to_scroll):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(sleep_time)

        f = open('questions.html', 'w')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        f.write(str(soup))
        f.close()
    else:
        f = open('questions.html', 'r')
        soup = BeautifulSoup(str(f.readlines()), 'html.parser')
        f.close()

    return soup

# Use BeautifulSoup to parse the questions listing to select all question texts.
def get_questions(soup, html_class, get_descriptions):
    for link in soup.find_all('a', class_=html_class):
        if link.get('href').find('question') != -1:
            row = []
            row.append(link.text.encode('utf-8'))
            if get_descriptions:
                try:
                    url = urllib2.urlopen('https://answers.yahoo.com' + link.get('href'))
                    row.append(get_description(BeautifulSoup(url, 'html.parser')))
                except urllib2.HTTPError, e:
                    continue
            else:
                row.append('')
            row.append('https://answers.yahoo.com' + link.get('href'))
            c.execute('INSERT OR IGNORE INTO questions VALUES (?, ?, ?)', row) 

# Use BeautifulSoup to parse the question page to select its description.
def get_description(soup):
    return soup.find_all('span', { 'class': 'ya-q-text' })[0].text

url = sys.argv[1]
fname = 'questions.html'
one_day_ago = time.time() - 60 * 60 * 24;
html_class = 'Fz-14 Fw-b Clr-b Wow-bw title'

soup = get_questions_page(url, fname, 100, 0.5, one_day_ago)
get_questions(soup, html_class, True)
conn.commit()
