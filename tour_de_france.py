import requests
import re
import json

besedilo = requests.get('https://www.letour.fr/en/history').text

# (\d*) -> oklepaji so za capture group
# Testiranje priporočam na https://www.regextester.com/
izraz = r'data-tabs-ajax="/en/block/history/\d*/.*">(\d*)</button>'

iskanje = re.findall(izraz, besedilo)

def dobi_info_staga(link):
    '''Vrne tekstovno informacijo strani o stagu.'''
    return requests.get(link).text

def preveri(besedilo):
    '''Preveri ali je ne obstaja stran.'''
    #response = requests.get(link)
    izraz = '<title>Page not found.*</title>'
    return len(re.findall(izraz, besedilo)) > 0

def slovar_kolesarjev(podatki):
    '''Funkcija bo za vsako etapo/stage naredila slovar posameznih kolesarjev na etapi,
    kateri ekipi pripadajo in kakšen je bil njihov zaostanek.'''
    podatki = podatki.split('</tbody></table>') # ločimo različne tabele podatkov
    danasnji = podatki[0]
    niz = r'<td>.*</a><span class="showIfMobile riderteam">.*</td>'
    isci = re.findall(niz, danasnji)
    slovar = {}
    for kolesar in isci:
        kolesar = kolesar.split('</td>')
        tabela_kolesar = []
        for podniz in kolesar:
            zamenjava = re.sub('<.*?>', "", podniz).strip()
            if len(zamenjava) == 0:
                zamenjava = None
                tabela_kolesar.append(None)
                continue
                zamenjava = None
            tabela_kolesar.append(zamenjava)
        #if tabela_kolesar[6] is None:
        if tabela_kolesar[7] == None:
            #tabela_kolesarjev.append(tabela_kolesar)
            continue
        else:
            tabela_kolesar[5] = re.sub(tabela_kolesar[7], "", tabela_kolesar[5])
        ime_kolesarja = tabela_kolesar.pop(5)
        slovar[ime_kolesarja] = tabela_kolesar
    return slovar

    
    
slovar_tourov = {}
for leto in iskanje:
    
    iskanje_po_letu = 'https://www.procyclingstats.com/race/tour-de-france/' + str(leto)
    besedilo = requests.get(iskanje_po_letu).text

    st_stagov = int(
        re.findall(f'<title>Tour de France \d* Stage (\d*)[a,b]?(?: \(ITT\))? results</title>', besedilo)[0])
    print(f'Leto: {leto}, število tekem: {st_stagov}')
        
    slovar_etap = {}
    # Za vsako leto preglej vse stage
    for trenutni_stage in range(1, st_stagov + 1):
        stage_link = f'{iskanje_po_letu}/stage-{trenutni_stage}'
        response = dobi_info_staga(stage_link)

#             preveri = re.findall(izraz, response.text)
        if preveri(response):
            stage_a = dobi_info_staga(stage_link + 'a')
            stage_b = dobi_info_staga(stage_link + 'b')
            stage_c = dobi_info_staga(stage_link + 'c')
            if preveri(stage_c):
                print(f'Stage {trenutni_stage} a in b')
#                     slovar_etap[str(trenutni_stage) + 'a'] = slovar_kolesarjev(stage_a)
#                     slovar_etap[str(trenutni_stage) + 'b'] = slovar_kolesarjev(stage_b)
            else:
                print(f'Stage {trenutni_stage} a, b in c')
                slovar_etap[str(trenutni_stage) + 'c'] = slovar_kolesarjev(stage_c)
            slovar_etap[str(trenutni_stage) + 'a'] = slovar_kolesarjev(stage_a)
            slovar_etap[str(trenutni_stage) + 'b'] = slovar_kolesarjev(stage_b)
        else:
            print(f'Stage {trenutni_stage}')
            slovar_etap[trenutni_stage] = slovar_kolesarjev(response)
    slovar_tourov[leto] = slovar_etap
    
#print(slovar_tourov)


with open('tour_de_france_podatki.json', 'w') as f:
     json.dump(slovar_tourov , f)





