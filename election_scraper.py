import requests
from bs4 import BeautifulSoup as bs
import csv
#import urllib3

URL_CR = 'https://volby.cz/pls/ps2017nss/ps2?xjazyk=CZ&xkraj=0'
# URL = 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2109'
URL = 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4207'  # Usti nad Labem
FILE_OUT = 'Vysledky_Praha-Vychod.csv'
# URL_START = 'https://volby.cz/pls/ps2017nss/'
URL_START = 'https://volby.cz/pls/ps2017nss/'  # Usti nad Labem:


# Funkce ziska seznam vsech stran kandidujicich v CR
# Jako vstup potrebuje odkaz na vysledky voleb cele CR
def get_all_parties_cr(url_cr):
    r = requests.get(url_cr)
    soup = bs(r.text, 'html.parser')
    divs = soup.find_all('div', class_='t2_430')
    parties_all_cr = []
    for i, div in enumerate(divs, start=1):
        headers = f't{i}sa1 t{i}sb2'
        names = div.find_all('td', headers=headers)
        parties_div = []
        for name in names:
            if name.text.strip() != '-':
                parties_div.append(name.text)
        parties_all_cr.extend(parties_div)

    return parties_all_cr


# Fukce vytvori hlavicku vysledne tabulky
def create_table_head(parties_all):
    table_head = ['Kod obce',
                  'Název obce',
                  'Voliči v seznamu',
                  'Vydané obálky',
                  'Platné hlasy']
    return table_head + parties_all



def get_html(url):
    r = requests.get(url)
    return r.text


# Funkce ziska kod obce, nazev obce a odkaz na stranku s vysledky voleb pro kazdou obec
# Vystupem je list tuplu (kod, nazev, odkaz)
# [('567931',
#   'Dolní Zálezly',
#   'https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=6&xobec=567931&xvyber=4207'), ...]
def get_all_locations(html):    # - testovano, v poradku
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


# Vstupem funkce je odkaz na stranku s vysledky konkretni obce z fukce get_all_locations
# Vystupem je list tuplu, obsahujici pary cisel - poradkove cislo strany a pocet platnych hlasu
def get_parties_votes(html):
    soup = bs(html, 'html.parser')

    divs = soup.find_all('div', class_='t2_470')
    # Vytvorime prazdnyj list pro poradkova cisla a pocet hlasu vsech stran, kandidujicich v obci
    parties_votes_all = []
    for i, div in enumerate(divs, start=1):
        headers_nums = f't{i}sa1 t{i}sb1'
        headers_votes = f't{i}sa2 t{i}sb3'
        parties_nums = div.find_all('td', class_='cislo', headers=headers_nums)
        parties_votes = div.find_all('td', class_='cislo', headers=headers_votes)
        parties_div = []
        for n in range(len(parties_nums)):
            parties_div.append((parties_nums[n].text, parties_votes[n].text.replace('\\xa0', '')))
        parties_votes_all.extend(parties_div)

    return parties_votes_all

# Funkce vytori list s platnymi hlasy pro kazdou stranu v dane obci
# a prida i strany, ktere v obci ne kandidovali s prazdnym stringem pro pocet hlasu.
# Data zformovana podle celorepublikoveho seznamu a poradi politickych stran,
# a tim jsou pripravena pro zapis do vysledneho souboru
def get_corrected_parties_votes(parties_votes, parties_all_cr):
    parties_votes_region = []
    for num in range(1, len(parties_all_cr) + 1):
        try:
            if int(parties_votes[0][0]) == num:
                parties_votes_region.append(parties_votes[0][1])
                del parties_votes[0]
            else:
                parties_votes_region.append(' ')
        except:
            parties_votes_region.append(' ')
    return parties_votes_region


def write_csv(file, head, table):
    with open(file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(head)
        writer.writerows(table)
    print(f'File {FILE_OUT} created')



def main():
    parties_all_cr = get_all_parties_cr(URL_CR)
    table_head = create_table_head(parties_all_cr)
    print(table_head)
    html1 = get_html(URL)
    all_locations = get_all_locations(html1)
    result_table = []
    for elem in all_locations:
        code, name, link = elem
        html2 = get_html(link)
        soup = bs(html2, 'html.parser')
        registered_ = soup.find('td', class_='cislo', headers='sa2').text.strip()
        registered = registered_.replace('\\xa0', '')
        print(registered)
        envelops_ = soup.find('td', class_='cislo', headers='sa3').text.strip()
        envelops = envelops_.replace('\\xa0', '')
        valid_ = soup.find('td', class_='cislo', headers='sa6').text.strip()
        valid = valid_.replace('\\xa0', '')

        parties_votes = get_parties_votes(html2)
        parties_votes_region = get_corrected_parties_votes(parties_votes, parties_all_cr)
        print(parties_votes_region)
        row_to_table = [code, name, registered, envelops, valid] + parties_votes_region
        result_table.append(row_to_table)
        print('Data for', code, name, 'parsed')

    write_csv(FILE_OUT, table_head, result_table)

    from pprint import pprint as pp
    pp(result_table)


if __name__ == '__main__':
    main()

