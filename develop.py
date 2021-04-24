import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint as pp

# Vystupem je list tuplu, obsahujici pary cisel - poradkove cislo strany a pocet platnych hlasu
URL = 'https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=538043&xvyber=2109'

r = requests.get(URL)
soup = bs(r.text, 'html.parser')

divs = soup.find_all('div', class_='t2_470')
# Vytvorime prazdnyj list pro poradkova cisla vsech stran, kandidujicich v obci
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

for n, party in enumerate(parties_all, start=1):
    print(n, party)

# try:
#     registered = soup.find('td', class_='cislo', headers='sa2').text.strip()
# except:
#     registered = ''
#
# try:
#     envelops = soup.find('td', class_='cislo', headers='sa3')
# except:
#     envelops = ''
#
# try:
#     valid = soup.find('td', class_='cislo', headers='sa6')
# except:
#     valid = ''
#
#
#
#
# print(volici)