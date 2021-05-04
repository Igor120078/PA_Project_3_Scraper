import requests
from bs4 import BeautifulSoup as bs
import sys
import csv


URL_CR = 'https://volby.cz/pls/ps2017nss/ps2?xjazyk=CZ&xkraj=0'
URL_START = 'https://volby.cz/pls/ps2017nss/'
# URL = 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2109'
# URL = 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4207'  # Usti nad Labem
# FILE_OUT = 'Vysledky_Praha-Vychod.csv'



def get_all_parties_cr(url_cr):
    """
    Funkce ziska seznam vsech stran kandidujicich v CR.
    :param url_cr: odkaz na vysledky voleb cele CR
    :return: list s nazvy vsech politickych stran CR
    """
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


def create_table_head(parties_all):
    """
    Fukce vytvori hlavicku vysledne tabulky.
    :param parties_all: seznam vsech stran CR
    :return: list s nazvy sloupcu vysledne tabulky
    """
    table_head = ['Kod obce',
                  'Název obce',
                  'Voliči v seznamu',
                  'Vydané obálky',
                  'Platné hlasy']
    return table_head + parties_all


def get_html(url):
    """
    Funkce ziska html kod web stranky s vysledky voleb a zkontruluje odezvu webu na dotaz.
    :param url: odkaz na web stranku
    :return: html kod stranky
    """
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    else:
        sys.exit("Web response Error")


def get_all_locations(html):
    """
    Funkce ziska kod obce, nazev obce a odkaz na stranku s vysledky voleb pro kazdou obec.
    Vystupem je list tuplu (kod, nazev, odkaz)
[('567931',
  'Dolní Zálezly',
  'https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=6&xobec=567931&xvyber=4207'), ...]
    :param html: html kod stranky
    :return: list of tuples (code, name, link)
    """
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


def get_parties_votes(html):
    """
    Funkce ziska vysledky hlasovani pro danou obec podle politickych stran.
    Vstupem funkce je odkaz na stranku s vysledky voleb pro konkretni obce z fukce get_all_locations.
    Vystupem je list tuplu, obsahujici pary cisel - poradkove cislo strany a pocet platnych hlasu
    :param html: odkaz na stranku s vysledky voleb
    :return: list of tuples (party #, votes)
    """
    soup = bs(html, 'html.parser')

    divs = soup.find_all('div', class_='t2_470')
    parties_votes_all = []
    for i, div in enumerate(divs, start=1):
        headers_nums = f't{i}sa1 t{i}sb1'
        headers_votes = f't{i}sa2 t{i}sb3'
        parties_nums = div.find_all('td', class_='cislo', headers=headers_nums)
        parties_votes = div.find_all('td', class_='cislo', headers=headers_votes)
        parties_div = []
        for n in range(len(parties_nums)):
            parties_div.append((parties_nums[n].text, parties_votes[n].text.replace('\xa0', '')))
        parties_votes_all.extend(parties_div)

    return parties_votes_all


def get_corrected_parties_votes(parties_votes, parties_all_cr):
    """
    Funkce vytori list s platnymi hlasy pro kazdou stranu v dane obci
a prida i strany, ktere v obci ne kandidovali s prazdnym stringem pro pocet hlasu.
Ve vysledku data jsou zformovana podle celorepublikoveho seznamu a poradi politickych stran,
a tim jsou pripravena pro zapis do vysledneho souboru.
    :param parties_votes: seznam politickych stran a jejich hlasu pro konkretni obec
    :param parties_all_cr: seznam vsech politickych stran CR a jejich poradkova cisla
    :return: list platnych hlasu vsech politickych stran CR pro danou obec
    """
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


def get_result_table(all_locations, parties_all_cr):
    """
    Funkce pouzije jako  prvni parametr list tuplu (kod, nazev, odkaz) z funkce get_all_locations
    a z kazdeho odkazu na vysledky voleb pro konkretni obec ziska vsechny dalsi data
    pro vytvoreni vysledne tabulky (registrovane volici, vydane obalky, platne hlasy, kandidujici strany
    a pocet jimi ziskanych hlasu).
    Druhy parametr je seznam vsech politickych stran CR pro vytvoreni stejneho vystupu po kazde obci.
    :param parties_all_cr: seznam vsech politickych stran CR
    :param all_locations: list tuplu (kod obce, nazev obce, odkaz na vysledky voleb v teto obci)
    :return result_table: vysledna tabulka (list listu) pro zapis do souboru
    """
    result_table = []
    for elem in all_locations:
        code, name, link = elem
        html = get_html(link)
        soup = bs(html, 'html.parser')
        registered_ = soup.find('td', class_='cislo', headers='sa2').text.strip()
        registered = registered_.replace('\xa0', '')
        envelops_ = soup.find('td', class_='cislo', headers='sa3').text.strip()
        envelops = envelops_.replace('\xa0', '')
        valid_ = soup.find('td', class_='cislo', headers='sa6').text.strip()
        valid = valid_.replace('\xa0', '')

        parties_votes = get_parties_votes(html)
        parties_votes_region = get_corrected_parties_votes(parties_votes, parties_all_cr)
        row_to_table = [code, name, registered, envelops, valid] + parties_votes_region
        result_table.append(row_to_table)
        print('Data for', code, name, 'parsed')
    return result_table


def write_csv(file, head, table):
    """
    Funkce zapise ziskana data do vysledneho souboru.
    :param file: nazev souboru
    :param head: hlavicka tabulky
    :param table: tabulka s vysledky scrapingu
    :return: soubur s vysledky scrapingu
    """
    with open(file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(head)
        writer.writerows(table)


def main():
    if len(sys.argv) < 3:
        sys.exit("The script needs two arguments to work correctly, {} was given".format(len(sys.argv)-1))
    elif not sys.argv[1].startswith('https://volby.cz/pls/ps2017nss/'):
        sys.exit("Sorry, but the first argument isn't a link to a web page with the election results")
    else:
        URL = sys.argv[1]
        FILE_OUT = sys.argv[2]
    parties_all_cr = get_all_parties_cr(URL_CR)
    table_head = create_table_head(parties_all_cr)
    print(f"STAHUJI DATA Z VYBRANEHO URL: {URL}")
    html = get_html(URL)
    all_locations = get_all_locations(html)
    result_table = get_result_table(all_locations, parties_all_cr)

    print(f"UKLADAM DATA DO SOUBORU: {FILE_OUT}")
    write_csv(FILE_OUT, table_head, result_table)
    print(f'File {FILE_OUT} created')

if __name__ == '__main__':
    main()
