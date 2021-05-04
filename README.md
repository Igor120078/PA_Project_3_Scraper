# PA_Project_3_Scraper
Třetí project v ramci Python Academii od společnosti [Engeto](https://engeto.cz).
## Popis projektu
Tento project slouží k extrahování výsledků parlamentnich voleb v roce 2017.
Odkaz k prohlednuti naleznete [zde](https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2109).
## Instalace knihoven
Knihovny, které jsou použity v kódu najdete v soubouru ```requirements.txt```.
Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:
```
pip3 --version                      # overim verzi manazeru
pip3 install -r requirements.txt    # nainstalujeme knihovny
```
## Spuštění projektu
Spuštění souboru ```election_scraper.py``` pomoci příkazového řádku požaduje dva povinné argumenty.
```
python election_scraper <odkaz-uzemmiho-celku> <vysledny-soubor>
```
Následně vysledek bude uložen do ```.csv``` souboru
## Ukázka projektu
Výsledky hlasování pro okres Praha-Vychod:
1. argument: ```https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2109```
2. argument: ```Vysledky_Praha-Vychod.csv```

Spuštění programu:
```
python election_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2109" "Vysledky_Praha-Vychod.csv"
```
Průběh stahování:
![Průběh stahování](PA_Project_3_prubeh.jpg)
![Ukončení programu](PA_Project_3_finish.jpg)

Částečný výstup:
```
Kod obce,Název obce,Voliči v seznamu,Vydané obálky,Platné hlasy,Občanská demokratická strana, ...
538043,Babice,732,533,531,79,0,1,17, ,0,56,6,5,1, ,20,0,0,80, ,0, ,2,48,128,0,0,24,0,12,0,0,51,1, 
538051,Bašť,1409,966,961,212,4,0,39, ,3,61,40,17,4, ,22,0,1,139, ,0, ,2,84,239,1,2,16,1,5,0,2,66,1, 
534684,Borek,242,170,170,27,1,0,11, ,0,15,5,1,0, ,2,0,1,24, ,0, ,0,15,64,1,0,0,0,2,0,0,1,0, 
...
```