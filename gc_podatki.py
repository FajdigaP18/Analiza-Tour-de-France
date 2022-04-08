import requests
import re
import json


###################################
# zanima me kje je bila dirka odločena in na podlagi tega lahhko računalnik s strojnim učenjem predvideva, kdo bo zmagovalec v prihajajočem touru
###################################

def dobi_info_staga(link):
    '''Vrne tekstovno informacijo strani o stagu.'''
    return requests.get(link).text

def razpolovi(niz):
    '''Funkcija razpolovi dani niz in vrne prvo polovico niza.'''
    dolzina = len(niz) // 2
    return niz[:dolzina]

def luscenje(tabela):
    '''Funkcija bo vrnila novo tabelo z 1., 3., 5., 6. 7. in 9. elementom iz tabele tabela.'''
    return [tabela[0]]  + tabela[5:8] + [tabela[-3]]
#    return [tabela[0]] + [tabela[2]] + tabela[4:7] + [tabela[-3]]

def tabela_kolesarjev(besedilo):
    '''Funkcija vrne tabelo podatkov kolesarjev za etapo.'''
#     podatki = besedilo.split('</tbody></table>')[0]
    niz = r'<td>.*</a><span class="showIfMobile riderteam">.*</td>'
    isci = re.findall(niz, besedilo)
    tabela = []
    for niz in isci:
        niz = niz.split('</td>')
        kolesar = []
        for podniz in niz:
            zamenjava = re.sub('<.*?>', "", podniz).strip()
            kolesar.append(zamenjava)
        #print(kolesar)
        if len(kolesar[0]) > 3:
            continue
        else:
            kolesar = luscenje(kolesar)
            kolesar[1] = re.sub(kolesar[3], "", kolesar[1])
            tabela.append(kolesar)
    return tabela



besedilo = requests.get('https://www.letour.fr/en/history').text

# (\d*) -> oklepaji so za capture group
# Testiranje priporočam na https://www.regextester.com/
izraz = r'data-tabs-ajax="/en/block/history/\d*/.*">(\d*)</button>'

iskanje = re.findall(izraz, besedilo)

slovar_zmagovalcev = {}
for leto in iskanje:

    try:
        link = f'https://www.procyclingstats.com/race/tour-de-france/{str(leto)}/gc'
        gc = dobi_info_staga(link)
        podatki = gc.split('</tbody></table>')
        if leto == '1987':
            gc = podatki[2]
        else:
            gc = podatki[1]
        slovar = tabela_kolesarjev(gc)
        
        slovar_zmagovalcev[leto] = slovar
        print(slovar)
        print(f'{leto} Deluje.')
        
    except:
        print(leto)


print(slovar_zmagovalcev['1987'])
# 
# with open('zmagovalci_podatki.json', 'w') as f:
#      json.dump(slovar, f)        
        