from class_Cas import Cas
import json
import matplotlib.pyplot as plt

f = open('tour_de_france_podatki.json')
podatki = json.load(f)

gc = open('zmagovalci_podatki.json')
podatki_gc = json.load(gc)

e = open('opis_etap.json')
et = json.load(e)

##########################################
# Poiscimo zmagovalce podamezne etape (prvi trije):
##########################################

def kdaj_kronometer(podatki, leto):
    '''Funkcija bo vrnila seznam etap, na katerih je bil kronometer.'''
    seznam = []
    niz = 'Time Trial'
    for etapa in podatki[leto].keys():
        if niz in podatki[leto][etapa]:
            seznam.append(etapa)
    return seznam

def preveri_kljuc(podatki, kolesar, leto, etapa):
    '''Funkcija preveri ali je ključ pravilen.'''
    return kolesar in podatki[leto][etapa].keys()

def prvo_drugo_mesto(podatki_gc, leto):
    '''Funkcija vrne seznam imen prvo in drugo uvrščenih kolesarjev na Tour de France.'''
    prvi = podatki_gc[leto][0][1]
    drugi = podatki_gc[leto][1][1]
    return prvi, drugi

def razpolovi(niz):
    '''Funkcija razpolovi dani niz in vrne prvo polovico niza.'''
    dolzina = len(niz) // 2
    return niz[:dolzina]

def cas_popravek(niz):
    '''Funkcija vo spremenila niz casa v niz ura:min:sek'''
    bonus = None
    if ',,' in niz:
        niz = niz[2:]
    if len(niz.split(':')[-1]) > 2:
        ind = niz.split(':')[-1].index('″')
        bonus = int(niz.split(':')[-1][3:ind])
        niz = niz[:niz.index('+')]
    if len(niz.split(':')) == 3:
        if len(niz.split(':')[1]) > 2:
            niz = razpolovi(niz)
        else:
            niz = niz.split(':')
            return Cas(int(niz[0]), int(niz[1]), int(niz[-1]))
    niz = niz.split(':')
    return Cas(0, int(niz[0]), int(niz[1]))

def razlika_casov(prvi, drugi,  zmaga_kateri = None):
    '''Funkcija vrne razliko casov v sekundah. In sicer - bo pred casom '''
    razlika = 0
    tabela_razlik = []
    if zmaga_kateri is None:
        if prvi > drugi: # razlika se zmanjša
            cas = prvi - drugi
            d  = cas.minute * 60 + cas.sekunde
            return -d
        else:
            cas = drugi - prvi
            d = cas.minute * 60 + cas.sekunde
            return d
    else:
        if zmaga_kateri == 0:
            d = drugi.minute * 60 + drugi.sekunde
            return d
        if zmaga_kateri == 1:
            d = prvi.minute * 60 + prvi.sekunde
            return -d

def casovne_razlike(podatki, podatki_gc, prvi, drugi, leto):
    '''Funkcija vrne casovne razlike med prvo in drugo uvrscenim na touru leta leto.'''
    razlika = []
    prvi_1 = prvi + podatki_gc[leto][0][3]
    drugi_1 = drugi + podatki_gc[leto][1][3]
    sekunde = []
    zmage = []
    for etapa in podatki[leto].keys():
        if etapa in kdaj_kronometer(et, leto): k = -3
        else: k = -2
        if not preveri_kljuc(podatki, prvi, leto, etapa):
            prvi = prvi_1
        if not preveri_kljuc(podatki, drugi, leto, etapa):
            drugi = drugi_1
        try:
            zmaga = None
            mesto_1 = podatki[leto][etapa][prvi][0]
            mesto_2 = podatki[leto][etapa][drugi][0]
            if len(mesto_1) == 1:
                if int(mesto_1) == 1:
                    zmaga = 0
            if len(mesto_2) == 1:
                if int(mesto_2) == 1:
                    zmaga = 1
            zmage.append(zmaga)

            cas_1 = cas_popravek(podatki[leto][etapa][prvi][-1][k])
            cas_2 = cas_popravek(podatki[leto][etapa][drugi][-1][k])
            d = razlika_casov(cas_1, cas_2,  zmaga)
            sekunde.append(d)
            
            razlika.append((cas_1, cas_2))
        except:
            
            cas = Cas(0,0,0)
            razlika.append((cas, cas))
            zmage.append(None)
            sekunde.append(0)
    
    return sekunde

    
###################################################################################
###################################################################################


profili_etap = {'p0':'Ni podano', 'p1':'ravninska', 'p2':'hribovska', 'p3':'hribovska - gorska', 'p4':'gorska 2.-kategorije', 'p5':'gorska 1.kategorije'}

print('{:>10} | {:>10} | {:>26} | {:>26} | {:>15} | {:>20} | {:>20} | {:>20} | {:>22} | {}'.format('Leto', 'Št. etap', 'Zmagovalec', 'Drugo uvrščeni', 'Končni zaostanek', 'Ključna etapa', 'Največja razlika','Dolžina [m]', 'Profil etape', 'Kaksna zmaga' ))

kaksen_profil = {}
zaostanki = []
l = -22
tabela_letnic = list(et.keys())
for leto in tabela_letnic[l:]:
    st_etap = list(et[leto].keys())[-1]
    prvi, drugi = prvo_drugo_mesto(podatki_gc, leto)
    tabela = casovne_razlike(podatki, podatki_gc, prvi, drugi, leto)
    najvecji = max(tabela)
    koncni_zaostanek = razpolovi(podatki_gc[leto][1][-1])
    #koncni_zaostanek = '{}:{}'.format(koncni_zaostanek.minute, kon)
    
    indeks = tabela.index(najvecji)
    tabela_etap = list(et[leto].keys())
    etapa_najvecji = tabela_etap[indeks]
    kaksna_etapa = et[leto][etapa_najvecji]
    profil = et[leto][etapa_najvecji][2]
    dolzina = et[leto][etapa_najvecji][1]
    
    kako_zmaga = et[leto][etapa_najvecji][-1]
    
    if profil in kaksen_profil.keys():
        kaksen_profil[profil] += 1
    else:
        kaksen_profil[profil] = 0
    
    zaostanek = cas_popravek(koncni_zaostanek)
    zaostanki.append(zaostanek.ure * 60*60 + zaostanek.minute * 60 + zaostanek.sekunde)
    
    print('{:>10} | {:>10} | {:>26} | {:>26} | {:>15} | {:>20} | {:>20} | {:>20} | {:>23} | {}'.format(leto, st_etap, prvi, drugi, koncni_zaostanek, etapa_najvecji, najvecji, dolzina , profili_etap[profil], kako_zmaga))

 
print(zaostanki)

plt.plot(tabela_letnic[l:], zaostanki)
plt.title('Končni zaostanek drugouvrščenega na Tour de France po letih')
plt.xlabel('Leto')
plt.ylabel('Zaostanek drugouvrsčenega')
plt.show()

profili_x = []
st_y = []
for pf in list(kaksen_profil.keys()):
    profili_x.append(profili_etap[pf])
    st_y.append(kaksen_profil[pf])
print(profili_x)
print(st_y)

plt.bar(profili_x, st_y)
plt.title('Št. ključni profilov na dirkah Tour de France')
plt.xlabel('Profili')
plt.ylabel('število')
plt.show()


gc.close()
f.close()
    