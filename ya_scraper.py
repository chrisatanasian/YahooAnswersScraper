#!/usr/bin/python

import sys, time, os.path
import selenium_methods, soup_methods, db_methods

def main():
    db_name     = 'ya.db'
    fname       = 'questions.html'
    html        = ''
    html_class  = 'Fz-14 Fw-b Clr-b Wow-bw title'
    one_day_ago = time.time() - 60 * 60 * 24;
    url         = sys.argv[1]

    if not os.path.isfile(fname) or os.path.getctime(fname) < one_day_ago:
        html = selenium_methods.get_questions_html(url, 50, 0.75)
        f = open('questions.html', 'w')
        f.write(html.encode('utf-8'))
        f.close()
    else:
        f = open('questions.html', 'r')
        html = str(f.readlines())
        f.close()

    soup = soup_methods.convert_html_to_soup(html)
    questions = soup_methods.get_questions(soup, html_class, False)

    db_methods.insert_into_db(db_name, questions)

if __name__ == "__main__":
    main()
