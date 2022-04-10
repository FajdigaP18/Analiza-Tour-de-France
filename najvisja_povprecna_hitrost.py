import matplotlib
import matplotlib.pyplot as plt
import json

e = open('opis_etap.json')
podatki = json.load(e)

slovar_najvisjih_povp_hitrosti = {'1903': [], '1904': [], '1905': [], '1906': [], '1907': [], '1908': [], '1909': [], '1910': [],'1911': [], '1912': [], '1913': [], '1914': [],'1919': [], '1920': [], '1921': [], '1922': [],
                     '1923': [], '1924': [], '1925': [], '1926': [],'1927': [], '1928': [], '1929': [], '1930': [],'1931': [], '1932': [], '1933': [], '1934': [],'1935': [], '1936': [], '1937': [], '1938': [],'1939': [], '1947': [], '1948': [], '1949': [],'1950': [], '1951': [], '1952': [], '1953': [],
                     '1954': [], '1955': [], '1956': [], '1957': [],'1958': [], '1959': [], '1960': [], '1961': [],'1962': [], '1963': [], '1964': [], '1965': [],'1966': [], '1967': [], '1968': [], '1969': [],'1970': [], '1971': [], '1972': [], '1973': [],'1974': [], '1975': [], '1976': [], '1977': [],
                     '1978': [], '1979': [], '1980': [], '1981': [],'1982': [], '1983': [], '1984': [], '1985': [],'1986': [], '1987': [], '1988': [], '1989': [],'1990': [], '1991': [], '1992': [], '1993': [],'1994': [], '1995': [], '1996': [], '1997': [],'1998': [], '1999': [], '2000': [], '2001': [],
                     '2002': [], '2003': [], '2004': [], '2005': [],'2006': [], '2007': [], '2008': [], '2009': [],'2010': [], '2011': [], '2012': [], '2013': [],'2014': [], '2015': [], '2016': [], '2017': [],'2018': [], '2019': [], '2020': [], '2021': [],
}

for kljuc in podatki:
    for podkljuc in podatki[kljuc]:
        slovar_najvisjih_povp_hitrosti[kljuc].append(podatki[kljuc][podkljuc][0])
        
print(slovar_najvisjih_povp_hitrosti)

for kljuc in podatki:
    for podkljuc in podatki[kljuc]:
        slovar_najvisjih_povp_hitrosti[kljuc].append(podatki[kljuc][podkljuc][0])
        
print(slovar_najvisjih_povp_hitrosti)


leto_1 = '1999'
hitrosti_1 = []
for v in slovar_najvisjih_povp_hitrosti[leto_1]:
    v = float(v[:-4])
    hitrosti_1.append(v)

st_etap_1 = []
for i in range(len(hitrosti_1)):
    st_etap_1.append(i)

leto_2 = '2021'
hitrosti_2 = []
for v in slovar_najvisjih_povp_hitrosti[leto_2]:
    v = float(v[:-4])
    hitrosti_2.append(v)

st_etap_2 = []
for i in range(len(hitrosti_2)):
    st_etap_2.append(i)

plt.plot(st_etap_1, hitrosti_1, label = leto_1)
plt.plot(st_etap_2, hitrosti_2, label = leto_2)
plt.xlabel('Etape')
plt.ylabel('Povprecne hitrosti')
plt.title(f'Primerjava povprecnih hitrosti leta {leto_1} in {leto_2}')
plt.legend()
plt.show()
plt.savefig("primerjava_povprečnih_hitrosti.pdf")#, bbox_inches = 'tight')
plt.close()

e.close()
