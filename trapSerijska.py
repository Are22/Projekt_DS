'''
 * Fajl:  trapSerijska.py
 * Svrha: Serijska implementacija trapezoidalne formule
 *
 * Ulaz:   a, b, n
 * Izlaz:  Integral funkcije f(x) na intervalu [a, b].

 Primjer za pokretanje: python trapSerijska.py 0.0 1.0 10000
 Dobiveni izlaz: Podjelom intervala na n = 10000 trapezoida, procjenjena vrijednost integralaod 0.0 do 1.0 iznosi 0.3333333349999983
'''

import numpy
import sys
import time #za mjerenje vremena

#Pokrenemo brojač vremena.
start = time.time()

#Čita podatke koji su napisani pri pokretanju programa u komandnoj liniji i postavlja ih na  [a,b,n]-
a = float(sys.argv[1])
b = float(sys.argv[2])
n = int(sys.argv[3])

#Ovdje definiramo funkciju.
def f(x):
        return x*x

def trapezna(a, b, n):
        '''Numerička integracija primjenjujući trapezoidno pravilo na intervalu
        od a do b koristeći n trapezoida.
        '''
        #Ovo je zadana u matematickoj formuli.
        integral = -(f(a) + f(b))/2.0
        #Imamo n trapezoida te zbog toga imamo n+1 krajnjih točaka.
        # numpy.linspace kreira polje koje uključuje n+1 pravilno raspoređenih točaka unutar intervala a i b.
        for x in numpy.linspace(a,b,n+1):
                integral = integral + f(x) #Integral je jedank integralu i sumi vrijednosti f(x), za svaki prethodno kreirani x u polju.
        integral = integral* (b-a)/n #(b-a)/n je ubiti ekvivalentno formuli za deltaX.
        return integral #Vracamo integral.

integral = trapezna(a, b, n) #Pozivanje funkcije.

#Zaustavimo brojač vremena.
end = time.time()

#Ispis.
print("Podjelom intervala na n =", n, "trapezoida, procjenjena vrijednost integrala\
od", a, "do", b, "iznosi", integral, "\nPritom smo koristili serijsku obradu")
print("\nVrijeme izvodenja programa ovom obradom iznosi", end-start )

