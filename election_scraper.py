import requests
from bs4 import BeautifulSoup as bs
#import urllib3


# https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2109
# <td class="cislo" headers="t1sa1 t1sb1"><a href="ps311?xjazyk=CZ&amp;xkraj=2&amp;xobec=538043&amp;xvyber=2109">538043</a></td>
# URL = 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2109'
URL = 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4207'  # Usti nad Labem:
RESULT_OUT = 'vysledky_Praha-vychod.csv'
# URL_START = 'https://volby.cz/pls/ps2017nss/'
URL_START = 'https://volby.cz/pls/ps2017nss/'  # Usti nad Labem:


def get_html(url):
    r = requests.get(url)
    return r.text

def get_all_links(html):
    soup = bs(html, 'html.parser')
    divs = soup.find_all('div', class_='t3')
    tables = [table for table in divs]
    links_all = []
    for i, table in enumerate(tables, start=1):
        links_tab = []
        headers = f't{i}sa1 t{i}sb1'
        tds = table.find_all('td', class_="cislo", headers=headers)
        for td in tds:
            link = URL_START + td.find('a').get('href')
            links_tab.append(link)
        links_all.extend(links_tab)
    return links_all

def main():
    html = get_html(URL)
    links_obce = get_all_links(html)
    from pprint import pprint as pp
    print(len(links_obce))
    pp(links_obce)



main()

