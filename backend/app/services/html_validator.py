from bs4 import BeautifulSoup


def sanitize_html(html):

    soup = BeautifulSoup(html, "html.parser")

    return str(soup)
