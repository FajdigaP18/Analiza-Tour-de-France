############################################################################
# kakšne etape gorske, hribovske, ravninske, kronometer, ekipni kronometer
############################################################################

import requests
import re
import json

def dobi_info_staga(link):
    '''Vrne tekstovno informacijo strani o stagu.'''
    return requests.get(link).text

def preveri(besedilo):
    '''Preveri ali je ne obstaja stran.'''
    #response = requests.get(link)
    izraz = '<title>Page not found.*</title>'
    return len(re.findall(izraz, besedilo)) > 0


def etapa(podatki):
    '''Funkcija vrne podatke etape ([povprečna_hitrost, pot, profil, vertikalni_metri, start, cilj, kašen_je_bil_zaključek]).'''
    etapa = podatki.split('</tbody></table>')[-1]
    
    hitrost = r'Avg. speed winner:</div> <div>.*'
    pot = r'Distance:\s*</div> <div>.* km'
    profil = r'Parcours type:\s*</div> <div><span class="icon profile p\d"'
    vertikalno = r'Vert. meters:</div> <div>\d*'
    zacetek = r'Departure:</div> <div><a    href="location/.*">.*</a>'
    konec = r'Arrival:</div> <div><a    href="location/.*">.*</a>'
    zmaga_kako = r'Won how: </div> <div>.*'
    
    v = re.findall(hitrost, etapa)[0].split('<div>')
    v = re.sub('<.*?>', "", v[-1])
    #v = re.findall(hitrost, etapa)[0].split('<div>')
    #v = v[-1][:-4].strip()
    s = re.findall(pot, etapa)[0].split('<div>')[-1][:-3].strip()
    pr = re.findall(profil, etapa)[0][-3:-1]
    ver = re.findall(vertikalno, etapa)[0].split('<div>')
    start = re.findall(zacetek, etapa)
    start = re.sub('<.*?>', "", start[0])[10:].strip()
    cilj = re.findall(konec, etapa)
    cilj = re.sub('<.*?>', "", cilj[0])[8:].strip()
    zmaga = re.findall(zmaga_kako, etapa)[0][:-11].split('<div>')[-1]
    zmaga = re.sub('<.*?>', "", zmaga)

    if len(ver[-1]) == 0: ver = '/'
    else: ver = int(ver[-1])
    return [v, s, pr, ver, start, cilj, zmaga]

besedilo = requests.get('https://www.letour.fr/en/history').text

# (\d*) -> oklepaji so za capture group
# Testiranje priporočam na https://www.regextester.com/
izraz = r'data-tabs-ajax="/en/block/history/\d*/.*">(\d*)</button>'

iskanje = re.findall(izraz, besedilo)

    
slovar_tourov = {}
for leto in iskanje:
    try:
        iskanje_po_letu = 'https://www.procyclingstats.com/race/tour-de-france/' + str(leto)
        besedilo = requests.get(iskanje_po_letu).text

        st_stagov = int(
            re.findall(f'<title>Tour de France \d* Stage (\d*)[a,b]?(?: \(ITT\))? results</title>', besedilo)[0])
        print(f'Leto: {leto}, število tekem: {st_stagov}')
        
        slovar_etap = {}
        # Za vsako leto preglej vse stage
        for trenutni_stage in range(1, st_stagov + 1):
            if int(leto) == 1998 and trenutni_stage == 17:
                continue
            stage_link = f'{iskanje_po_letu}/stage-{trenutni_stage}'
            response = dobi_info_staga(stage_link)

#             preveri = re.findall(izraz, response.text)
            if preveri(response):
                stage_a = dobi_info_staga(stage_link + 'a')
                stage_b = dobi_info_staga(stage_link + 'b')
                stage_c = dobi_info_staga(stage_link + 'c')
                if preveri(stage_c):
                    print(f'Stage {trenutni_stage} a in b')
                    slovar_etap[str(trenutni_stage) + 'a'] = etapa(stage_a)
                    slovar_etap[str(trenutni_stage) + 'b'] = etapa(stage_b)
                else:
                    print(f'Stage {trenutni_stage} a, b in c')
                    slovar_etap[str(trenutni_stage) + 'a'] = etapa(stage_a)
                    slovar_etap[str(trenutni_stage) + 'b'] = etapa(stage_b)
                    slovar_etap[str(trenutni_stage) + 'c'] = etapa(stage_c)
            else:
                print(f'Stage {trenutni_stage}')
                slovar_etap[str(trenutni_stage)] = etapa(response)
        slovar_tourov[leto] = slovar_etap
    except:
        print(leto)
with open('opis_etap.json', 'w') as f:
    json.dump(slovar_tourov , f)


