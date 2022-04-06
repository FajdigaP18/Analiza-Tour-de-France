## program ne dela

import requests
import re
import json

slovar_izjem = {'1934': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, '21a', '21b', 22, 23],
                '1935': [1, 2, 3, 4, '5a', '5b', 6, 7, 8, 9, 10, 11, 12, '13a', '13b', '14a', '14b', 15, 16, 17, '18a', '18b', '19a', '19b', '20a', '20b', 21],
                '1936': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, '13a', '13b', '14a', '14b', 15, 16, 17, '18a', '18b', '19a','19b','19c', '20a', '20b', 21],
                '1937': [1, 2, 3, 4, '5a', '5b', '5c', 6, 7, 8, 9, 10, '11a', '11b', '12a', '12b', '13a', '13b', '14a', '14b', '14c', 15, 16, '17a', '17b', '17c', '18a', '18b', '19a', '19b', 20],
                '1938': [1, 2, 3, '4a', '4b', 5, '6a', '6b', 7, 8, 9, '10a', '10b', '10c', 11, 12, 13, 14, 15, 16, '17a', '17b', 18, 19, '20a', '20b', '20c', 21],
                '1939': [1, '2a', '2b', 3, 4, 5, '6a', '6b', 7, '8a', '8b', 9, '10a', '10b', 11, '12a', '12b', 13, 14, 15, '16a', '16b', '17a', '17b', '18a', '18b', 19, 20, 21, 22, 23],
                '1954': [1, 2, 3, '4a', '4b', 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, '21a', '21b', 22],
                '1955': ['1a', '1b', 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
                '1956': [1, 2, 3, '4a', '4b', 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
                '1957': [1, 2, '3a', '3b', 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, '15a', '15b', 16, 17, 18, 19, 20, 21, 22],
                '1960': ['1a', '1b', 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
                '1961': ['1a', '1b', 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
                '1962': [1, '2a', '2b', 3, 4, 5, 6, 7, '8a', '8b', 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
                '1963': [1, '2a', '2b', 3, 4, 5, '6a', '6b', 7 , 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
                '1964': [1, 2, '3a', '3b', 4, 5, 6, 7, 8, 9, '10a', '10b', 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, '22a', '22b'],
                '1965': ['1a', '1b', 2, 3, 4, '5a', '5b', 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
                '1966': [1, 2, '3a', '3b', 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, '14a', '14b', 15, 16, 17, 18, 19, 20, 21, '22a', '22b'],
                '1967': [1, 2, 3, 4, '5a', '5b', 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, '22a', '22b'],
                '1968': [1, 2, '3a', '3b', 4, '5a', '5b', 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, '22a', '22b'],
                '1969': ['1a', '1b', 2, 3, 4, 5, 6, 7, '8a', '8b', 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, '22a', '22b'],
                '1970': [1, 2, '3a', '3b', 4, '5a', '5b', 6, '7a', '7b', 8, 9, 10, '11a', '11b', 12, 13, 14, 15, 16, 17, 18, 19, '20a', '20b', 21, 22, 23],
                '1971': ['1a', '1b', '1c', 2, 3, 4, 5, '6a', '6b', 7, 8, 9, 10, 11, 12, 13, 14, 15, '16a', '16b', 17, 18, 19, 20],
                '1972': [1, 2, '3a', '3b', 4, '5a', '5b', 6, 7, 8, 9, 10, 11, 12, 13, '14a', '14b', 15, 16, 17, 18, 19, '20a', '20b'],
                '1973': ['1a', '1b', '2a', '2b', 3, 4, 5, 6, '7a', '7b', 8, 9, 10, 11, '12a', '12b', 13, 14, 15, '16a', '16b', 17, 18, 19, '20a', '20b'],
                '1974': [1, 2, 3, 4, 5, '6a', '6b', 7, '8a', '8b', 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, '19a', '19b', 20, '21a', '21b', 22],
                '1975': ['1a', '1b', 2, 3, 4, 5, 6, 7, 8, '9a', '9b', 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
                '1976': [1, 2, 3, 4, '5a', '5b', 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, '18a', '18b', 19, 20, 21, '22a', '22b'],
                '1977': [1, 2, 3, 4, '5a', '5b', 6, '7a', '7b', 6, 7, 8, 9, 10, 11, 12, '13a', '13b', 14, '15a', '15b', 16, 17, 18, 19, 20, 21, '22a', '22b'],
                '1978': ['1a', '1b', 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, '12a', '12b', 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
                '1980': ['1a', '1b', 2, 3, 4, 5, 6, '7a', '7b', 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
                '1981': ['1a', '1b', 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, '12a', '12b', 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
                '1982': [1, 2, 3, 4, 5, 6, 7, 8, '9a', '9b', 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
                '1985': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, '18a', '18b', 19, 20, 21, 22]}

def rezultati_posamezne_dirke(leto):
    '''Funkcija izpiše slovar podatkov posamezne dirke na turu, ki je bil leta ´letno´.'''
    iskanje = 'https://www.procyclingstats.com/race/tour-de-france/' + str(leto)
    besedilo = requests.get(iskanje).text
    if str(leto) in slovar_izjem.keys():
        seznam_etap = slovar_izjem[str(leto)]
    else:
        st_stagov = int(re.findall(r'<title>Tour de France \d* Stage \d*.*results</title>', besedilo)[0].split()[5])
        seznam_etap = range(1, st_stagov + 1)
    #print(st_stagov)
    slovar_stagov = {}
    for stage in range(1, st_stagov + 1):
        #print(stage)
        link = iskanje + '/stage-' + str(stage)
        stage_besedilo = requests.get(link).text
        stage_besedilo = stage_besedilo.split('</tbody></table>') # ločimo različne tabele podatkov
        if leto == '1988' and stage == 2: # poglej se za ostale ekipne kronometre
            danasnji = stage_besedilo[1]
        else:
            danasnji = stage_besedilo[0]
        niz = r'<td>.*</a><span class="showIfMobile riderteam">.*</td>'
        isci = re.findall(niz, danasnji)
        tabela_kolesarjev = []
        for kolesar in isci:
            kolesar = kolesar.split('</td>')
            tabela_kolesar = []
            for podniz in kolesar:
                zamenjava = re.sub('<.*?>', "", podniz).strip()
                if len(zamenjava) == 0:
                    zamenjava = None
                tabela_kolesar.append(zamenjava)
            if tabela_kolesar[7] is None:
                tabela_kolesarjev.append(tabela_kolesar)
                continue
            else:
                tabela_kolesar[5] = re.sub(tabela_kolesar[7], "", tabela_kolesar[5])
            tabela_kolesarjev.append(tabela_kolesar)#[:-1])
        slovar_stagov[stage] = tabela_kolesarjev
    return slovar_stagov

# LETNICE POSAMEZNIH DIRK
besedilo = requests.get('https://www.letour.fr/en/history').text
# 
izraz = r'data-tabs-ajax="/en/block/history/\d*/.*">\d*</button>'
iskanje = re.findall(izraz, besedilo)
#print(iskanje)
# 
# DOBIVANJE PODATKOV IZ POSAMEZNIH DIRK
#letnica = []
slovar_dirk = {}
for tour in iskanje:
    #print(tour)
    tour = tour.split('/')
    leto = tour[-2][:-1].split('">')[1]
    #letnica.append(int(leto))
    slovar_dirk[leto] = rezultati_posamezne_dirke(leto)
    print(leto)

with open('tour_de_france_podatki.json', 'w') as f:
     json.dump(slovar_dirk , f)

# podatki = rezultati_posamezne_dirke('1989')
# print(len(podatki['3']))#['2'])poglej drugi stage kr nejkej n stima
# print(len(podatki['2']))
