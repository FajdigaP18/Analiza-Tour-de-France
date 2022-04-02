## program ne dela

import requests
import re
import json

def rezultati_posamezne_dirke(leto):
    '''Funkcija izpiše slovar podatkov posamezne dirke na turu, ki je bil leta ´letno´.'''
    iskanje = 'https://www.procyclingstats.com/race/tour-de-france/' + str(leto)
    besedilo = requests.get(iskanje).text
    if leto == '1939':
        st_stagov = 26
        seznam_a_dirk = {2:2, 7:6, 10:8, 13:10, 16:12, 21:16, 23:17, 25:18}
        seznam_b_dirk = {3:2, 8:6, 11:8, 14:10, 17:12, 22:16, 24:17, 26:18}
    else:
        st_stagov = int(re.findall(r'<title>Tour de France \d* Stage \d* results</title>', besedilo)[0].split()[5])
    #print(st_stagov)
    slovar_stagov = {}
    for stage in range(1, st_stagov + 1):
        #print(stage)
        link = iskanje + '/stage-'
        if leto == 1939:
            if stage in seznam_a_dirk:
                stage =  str(seznam_a_dirk[stage]) + 'a'
                link += stage
            elif stage in seznam_b_dirk:
                stage = str(seznam_b_dirk[stage]) + 'b'
                link += stage
            else:
                link += str(stage)
        else:
            link += str(stage)
        stage_besedilo = requests.get(link).text
        stage_besedilo = stage_besedilo.split('</tbody></table>') # ločimo različne tabele podatkov
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


with open('tour_de_france_podatki.json', 'w') as f:
     json.dump(slovar_dirk , f)

# podatki = rezultati_posamezne_dirke(2000)
# print(podatki.keys)

