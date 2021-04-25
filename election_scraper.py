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

# Funkce ziska kod obce, nazev obce a odkaz na stranku s vysledky voleb pro kazdou obec
# Vystupem je list tuplu (kod, nazev, odkaz)
def get_all_locations(html):
    soup = bs(html, 'html.parser')
    divs = soup.find_all('div', class_='t3')
    tables = [table for table in divs]
    all_locations = []
    for i, table in enumerate(tables, start=1):
        locations = []
        headers1 = f't{i}sa1 t{i}sb1'
        # headers2 = f't{i}sa1 t{i}sb2'
        tds1 = table.find_all('td', class_="cislo", headers=headers1)
        # tds2 = table.find_all('td', headers=headers2)
        for td in tds1:
            location_code = td.string
            location_name = td.next_sibling.next_sibling.text
            link = URL_START + td.find('a').get('href')
            locations.append((location_code, location_name, link))
        all_locations.extend(locations)
    return all_locations


# Vystupem je list tuplu, obsahujici pary cisel - poradkove cislo strany a pocet platnych hlasu
def get_parties_votes(url):
    r = requests.get(URL)
    soup = bs(r.text, 'html.parser')

    divs = soup.find_all('div', class_='t2_470')
    # Vytvorime prazdnyj list pro poradkova cisla a pocet hlasu vsech stran, kandidujicich v obci
    parties_all = []
    for i, div in enumerate(divs, start=1):
        headers_nums = f't{i}sa1 t{i}sb1'
        headers_votes = f't{i}sa2 t{i}sb3'
        parties_nums = div.find_all('td', class_='cislo', headers=headers_nums)
        parties_votes = div.find_all('td', class_='cislo', headers=headers_votes)
        parties_div = []
        for n in range(len(parties_nums)):
            parties_div.append((parties_nums[n].text, parties_votes[n].text))
        parties_all.extend(parties_div)

    return parties_all





def main():
    html = get_html(URL)
    all_locations = get_all_locations(html)
    from pprint import pprint as pp
    print(len(all_locations))
    pp(all_locations)



main()

