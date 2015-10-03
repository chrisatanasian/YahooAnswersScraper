#!/usr/bin/python

import sys, time, os.path
import urllib2
import selenium.webdriver
from bs4 import BeautifulSoup

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
            print link.text.encode('utf-8')
            if get_descriptions:
                url = urllib2.urlopen('https://answers.yahoo.com' + link.get('href'))
                get_description(BeautifulSoup(url, 'html.parser'))
            print 'https://answers.yahoo.com' + link.get('href')

# Use BeautifulSoup to parse the question page to select its description.
def get_description(soup):
    description = soup.find_all('span', { 'class': 'ya-q-text' })[0].text
    if description:
        print description.encode('utf-8')

url = sys.argv[1]
fname = 'questions.html'
one_day_ago = time.time() - 60 * 60 * 24;
html_class = 'Fz-14 Fw-b Clr-b Wow-bw title'

soup = get_questions_page(url, fname, 100, 0.5, one_day_ago)
get_questions(soup, html_class, False)
