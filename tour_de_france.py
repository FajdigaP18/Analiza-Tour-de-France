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

def razpolovi(niz):
    '''Funkcija razpolovi dani niz in vrne prvo polovico niza.'''
    dolzina = len(niz) // 2
    return niz[:dolzina]

def luscenje(tabela):
    '''Funkcija vrne urejeno tabelo. (uvrstitev, ime_in_priimek, ekipa, starost, cas/zaostanek)'''
    return [tabela[0]] + tabela[5:8] + [tabela[-4:]]
#tabela[0]] + [tabela[2]] + tabela[4:7] + [tabela[-3]]  1., 3., 5., 6. 7. in 9.

def slovar_kolesarjev(besedilo):
    '''Funkcija vrne tabelo podatkov kolesarjev za etapo.'''
    podatki = besedilo.split('</tbody></table>')[0]
    niz = r'<td>.*</a><span class="showIfMobile riderteam">.*</td>'
    isci = re.findall(niz, podatki)
    slovar = {}
    for niz in isci:
        niz = niz.split('</td>')
        kolesar = []
        for podniz in niz:
            zamenjava = re.sub('<.*?>', "", podniz).strip()
            kolesar.append(zamenjava)
        #print(kolesar)
        kolesar = luscenje(kolesar)
        
        slovar[kolesar[1]] = kolesar
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





