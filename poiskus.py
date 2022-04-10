import json

f = open('tour_de_france_podatki.json')
podatki = json.load(f)

gc = open('zmagovalci_podatki.json')
podatki_gc = json.load(gc)

e = open('opis_etap.json')
et = json.load(e)

##########################################
# Poiscimo zmagovalce podamezne etape (prvi trije):
##########################################
letnice = list(podatki_gc.keys())

def kdaj_kronometer(podatki, leto):
    '''Funkcija bo vrnila seznam etap, na katerih je bil kronometer.'''
    seznam = []
    niz = 'Time Trial'
    for etapa in podatki[leto].keys():
        if niz in podatki[leto][etapa]:
            seznam.append(etapa)
    return seznam

def prvo_drugo_mesto(podatki_gc, leto):
    '''Funkcija vrne seznam imen prvo in drugo uvrščenih kolesarjev na Tour de France.'''
#     prvi_in_drugi = []
#     for leto in letnice:
    prvi = podatki_gc[leto][0][1] + podatki_gc[leto][0][3]
    drugi = podatki_gc[leto][1][1] + podatki_gc[leto][1][3]
    #prvi_in_drugi.append((prvi, drugi))
    return prvi, drugi

def cas_popravek(niz):
    '''Funkcija vo spremenila niz casa v niz ura:min:sek'''
    if ',,' in niz:
        a = [2:].split(':')
        ura = 0
        minute = int(a[0])
        sekunde = int(niz[-1])
    niz = niz.split(':')
    elif len(niz[1]) > 2:
        minute = int(niz[0])
        sekunde = int(niz[2][:2])
    elif len(niz[-1]) > 2:
        ind = index('″')
        bonus = int(niz[-1][4:ind])
    else:
        ura = int(niz[0])
        minute = int(niz[1])
        sekunde = int(niz[-1])
    return ura, minute, sekunde
# print(prvo_drugo_mesto(podatki_gc))

def casovne_razlike(podatki, prvi, drugi, leto):
    '''Funkcija vrne casovne razlike med prvo in drugo uvrscenim na touru leta leto.'''
    razlika_casov = []
    for etapa in podatki[leto].keys():
        if etapa in kdaj_kronometer(et, leto): k = -3
        else: k = -2
        cas_1 = podatki[leto][etapa][prvi][-1][k]
        cas_2 = podatki[leto][etapa][drugi][-1][k]
        razlika_casov.append((cas_1, cas_2))
    return razlika_casov

        
# leto = '2020'
# prvi, drugi = prvo_drugo_mesto(podatki_gc, leto)
# razlike = casovne_razlike(podatki, prvi, drugi, leto)
# print(razlike)

#zmagovalci = list(podatki_gc['2021'].keys())


# 
# ne_deluje = []
# ne_deluje_2 = []
# zmagovalci = []
# drugi = []
# 
# for key in podatki.keys():
#     for etapa in podatki[key].keys():
#         kolesarji = list(podatki[key][etapa].keys())
#         if len(kolesarji) == 0:
#             ne_deluje.append((key, etapa))
#             print("Ne deluje {}, {}".format(key, etapa))
#             continue
#         zmagovalec = list(podatki[key][etapa].keys())[0]
#         zmagovalci.append(zmagovalec)
#         drugi.append(kolesarji[1])
#         #print(key, etapa, zmagovalec)
# print(zmagovalci)
# print(ne_deluje)
# print(drugi)



# 
# for i in podatki['2021']['1'].items():
#     print(i)

gc.close()
f.close()
    