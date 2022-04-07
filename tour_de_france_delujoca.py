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


izraz = '<title>Page not found.*</title>'

link = 'https://www.procyclingstats.com/race/tour-de-france/1939/stage-2'
response = requests.get(link)
preveri = re.findall(izraz, response.text)
if len(preveri) > 0:
    stage_a = dobi_info_staga(link + 'a')
    stage_b = dobi_info_staga(link + 'b')

for leto in iskanje:

    try:
        iskanje_po_letu = 'https://www.procyclingstats.com/race/tour-de-france/' + str(leto)
        besedilo = requests.get(iskanje_po_letu).text

        st_stagov = int(
            re.findall(f'<title>Tour de France \d* Stage (\d*)[a,b]?(?: \(ITT\))? results</title>', besedilo)[0])
        print(f'Leto: {leto}, število tekem: {st_stagov}')

        # Za vsako leto preglej vse stage
        for trenutni_stage in range(1, st_stagov + 1):
            stage_link = f'{iskanje_po_letu}/stage-{trenutni_stage}'
            response = requests.get(stage_link)

            preveri = re.findall(izraz, response.text)
            if len(preveri) > 0:
                stage_a = dobi_info_staga(link + 'a')
                stage_b = dobi_info_staga(link + 'b')
                print(f'Stage {trenutni_stage} a in b')
            else:
                print(f'Stage {trenutni_stage}')

    except:
        print(leto)