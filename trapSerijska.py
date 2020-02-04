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

start = time.time()

#čita podatke koji su napisani pri pokretanju programa u komandnoj liniji i postavlja ih na  [a,b,n]
a = float(sys.argv[1])
b = float(sys.argv[2])
n = int(sys.argv[3])

#ovdje definiramo funkciju
def f(x):
        return x*x

def trapezna(a, b, n):
        '''Numerička integracija primjenjujući trapezoidno pravilo na intervalu
        od a do b koristeći n trapezoida.
        '''
        integral = -(f(a) + f(b))/2.0 #ovo je zadana u matematickoj formuli
        #imamo n trapezoida te zbog toga imamo n+1 krajnjih točaka
        for x in numpy.linspace(a,b,n+1): #numpy.linspace kreira polje koje uključuje n+1 pravilno raspoređenih točaka unutar intervala a i b
                integral = integral + f(x) #integral je jedank integrali i sumi vrijednosti f(x), za svaki prethodno kreirani x u polju
        integral = integral* (b-a)/n #(b-a)/n je ubiti ekvivalentno formuli za deltaX
        return integral  #vracamo integral

integral = trapezna(a, b, n) #pozivanje funkcije

end = time.time()

#ispis
print("Podjelom intervala na n =", n, "trapezoida, procjenjena vrijednost integrala\
od", a, "do", b, "iznosi", integral, "\nPritom smo koristili serijsku obradu")
print("\nVrijeme izvodenja programa ovom obradom iznosi", end-start )

