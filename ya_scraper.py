#!/usr/bin/python

import sys, time, os.path
import urllib2
import selenium.webdriver
import sqlite3
from bs4 import BeautifulSoup

# Use Selenium driver to get questions html page from url.
def get_questions_html(url, times_to_scroll, sleep_time):
    driver = selenium.webdriver.Chrome()
    driver.get(url)

    for i in range(1, times_to_scroll):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(sleep_time)

    return driver.page_source

# Use BeautifulSoup to parse the questions html to create a questions list.
def get_questions(soup, html_class, get_descriptions):
    questions = []
    for link in soup.find_all('a', class_=html_class):
        if link.get('href').find('question') != -1:
            question = [link.text.encode('utf-8')]
            url = 'https://answers.yahoo.com' + link.get('href')

            if get_descriptions:
                try:
                    html = urllib2.urlopen(url)
                    question.append(get_description(BeautifulSoup(html, 'html.parser')))
                except urllib2.HTTPError, e:
                    continue
            else:
                question.append('')

            question.append(url)
            questions.append(tuple(question))
    return questions

# Use BeautifulSoup to parse the question page to select its description.
def get_description(soup):
    spans = soup.find_all('span')
    if spans:
        return soup.find_all('span', { 'class': 'ya-q-text' })[0].text
    return ''


conn = sqlite3.connect('ya.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS questions
             (text text, description text, link text,
              UNIQUE(text))''')

url = sys.argv[1]
fname = 'questions.html'
one_day_ago = time.time() - 60 * 60 * 24;
html_class = 'Fz-14 Fw-b Clr-b Wow-bw title'
html = ''

if not os.path.isfile(fname) or os.path.getctime(fname) < one_day_ago:
    html = get_questions_html(url, 50, 0.75)
    f = open('questions.html', 'w')
    f.write(html.encode('utf-8'))
    f.close()
else:
    f = open('questions.html', 'r')
    html = str(f.readlines())
    f.close()

soup = BeautifulSoup(html, 'html.parser')
questions = get_questions(soup, html_class, True)

c.executemany('INSERT OR IGNORE INTO questions VALUES (?, ?, ?)', questions)

conn.commit()
conn.close()
