import urllib2
from bs4 import BeautifulSoup

# Use BeautifulSoup to parse the questions html to create a questions list.
def get_questions(soup, html_class, get_descriptions):
    print 'Parsing questions...'
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

def convert_html_to_soup(html):
    return BeautifulSoup(html, 'html.parser')
