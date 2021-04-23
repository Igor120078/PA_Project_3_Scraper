import requests
from bs4 import BeautifulSoup as bs
#import urllib3


# https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2109
# <td class="cislo" headers="t1sa1 t1sb1"><a href="ps311?xjazyk=CZ&amp;xkraj=2&amp;xobec=538043&amp;xvyber=2109">538043</a></td>
URL = 'https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xnumnuts=2109'
RESULT_OUT = 'vysledky_Praha-vychod.csv'



def get_html(url):
    r = requests.get(URL)
    return r.text

def get_data(html):
    soup = bs(html, 'html.parser')
    tag1 = soup.find('div', class_='topline')
    return tag1.contents
