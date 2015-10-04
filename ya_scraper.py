#!/usr/bin/python

import sys, time, os.path
import selenium_methods, soup_methods, db_methods
import argparse

DB_NAME     = 'ya.db'
FILE_NAME   = 'questions.html'
HTML_CLASS  = 'Fz-14 Fw-b Clr-b Wow-bw title'
ONE_DAY_AGO = time.time() - 60 * 60 * 24;

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', required=True,
                        help='questions category URL')
    parser.add_argument('-d', '--get_descriptions', action='store_true',
                        help='get descriptions of questions')
    args = parser.parse_args()

    url = vars(args)['url']
    get_descriptions = vars(args)['get_descriptions']

    if not os.path.isfile(FILE_NAME) or os.path.getctime(FILE_NAME) < ONE_DAY_AGO:
        html = selenium_methods.get_questions_html(url, 50, 0.75)
        f = open(FILE_NAME, 'w')
        f.write(html.encode('utf-8'))
        f.close()
    else:
        f = open(FILE_NAME, 'r')
        html = str(f.readlines())
        f.close()

    soup = soup_methods.convert_html_to_soup(html)
    questions = soup_methods.get_questions(soup, HTML_CLASS, get_descriptions)

    db_methods.insert_into_db(DB_NAME, questions)

if __name__ == "__main__":
    main()
