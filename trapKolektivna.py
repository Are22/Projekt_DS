'''
 * Fajl:    trapPtoP.py
 *
 * Svrha:   Paralelna implementacija trapezoidalne formule koristeći
            kolektivnu komunikaciju.
 *
 * Ulaz:   a, b, n
 * Izlaz:  Integral funkcije f(x) na intervalu [a, b] koristeći n te
 *         pritom smanjujući pogrešku.
 *
 * Pokretanje:  mpiexec -n <number of processes> ./mpi_trap
 *
 * Algoritam:
 *    0.  Proces ranga 0 čita ulaz  a, b, i n, i distribuira ih odnosno
 *        prosljeđuje ostalim procesima.
 *    1.  Svaki proces računa "svoj" podinterval, koristeći svoje
 *        lokalne a i b.
 *    2.  Svaki proces primjenjuje trapeznu formulu na svoj podinterval.
 *    3a. Svaki proces čiji je rang raličit od 0 šalje svoj rezultat precesu ranga 0.
 *    3b. Proces ranga 0 sumira rezultate dobivene od ostalih
 *        procesa te ispisuje konačni rezultat.
 *
 * Napomena:  f(x) je unaprijed zadana.
 * Primjer za pokretanje: mpiexec -n 4 python trapPtoP.py 0.0 1.0 10000
 * Dobiveni izlaz: Podjelom intervala na n = 10000 trapezoida, procjenjena vrijednst integrala od 0.0 do 1.0 iznosi 0.3333333350000003
 *
 '''

#importamo potrebne pakete(numpy-rad s poljima, sys-čita podatke, MPI- za komunikaciju među procesima)
import numpy
import sys
from mpi4py import MPI
import time #za mjerenje vremena izvođenja

start = time.time()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

#čita podatke koji su napisani pri pokretanju programa u komandnoj liniji i postavlja ih na  [a,b,n]
a = float(sys.argv[1])
b = float(sys.argv[2])
n = int(sys.argv[3])

#ovdje definiramo funkciju
def f(x):
        return x*x

#ovo je serijski pristup trapezoidalnoj formuli
#paralelizam se događa tako da imamo više procesa pri obradi
def trapezna(a, b, n):
        '''Numerička integracija primjenjujući trapezoidno pravilo na intervalu
        od a do b koristeći n trapezoida.
        '''
        integral = -(f(a) + f(b))/2.0 #ovo je zadana u matematickoj formuli
        #imamo n trapezoida te zbog toga imamo n+1 krajnjih točaka
        for x in numpy.linspace(a,b,n+1): #numpy.linspace kreira polje koje uključuje n+1 pravilno raspoređenih točaka unutar intervala a i b
                        integral = integral + f(x) #integral je jedank integrali i sumi vrijednosti f(x), za svaki prethodno kreirani x u polju
        integral = integral* (b-a)/n #(b-a)/n je ubiti ekvivalentno formuli za deltaX
        return integral #vracamo integral


#h je veličina koraka(za kolio čemo "se pomaknuti" od prve točke do sljedeče i tako redom), n je ukupan broj trapezoida
h = (b-a)/n
#lokalni_n je broj trapezoida koji će svaki pojedini proces izračunati
#potrebno je lokalni_n podijeliti s ukupnim brojem procesa
lokalni_n = n/size

#računamo interval za svaki pojedini proces
#lokalni_a je početna točka a lokalni_b je krajnja točka
lokalni_a = a + rank*lokalni_n*h
lokalni_b = lokalni_a + lokalni_n*h

#inicijaliziramo varijable. mpi4py traži da se prosljede numpy objekti.
integral = numpy.zeros(1)
ukupna_suma = numpy.zeros(1)

#Računanje lokalnog integrala. Svaki proces integrira svoj lokalni interval
integral[0] = trapezna(lokalni_a, lokalni_b, lokalni_n)

# komunikacija

#vrši proces redukcije(u oveme slučaju suma) na danom skupu elemenata koji čini
#po jedna vrijednost sa svakog od procesa i rezultat redukcije sprema u varijablu na korijenskom procesu.

comm.Reduce(integral, ukupna_suma, op=MPI.SUM, root=0)

end = time.time()

# korijenski proces(proces ranga 0) ispisuje konačni rezultat
if comm.rank == 0:
        print ("Podjelom intervala na n =", n, "trapezoida, procjenjena vrijednst integrala od"\
        , a, "do", b, "iznosi", ukupna_suma[0], "\nPritom smo koristili kolektivnu komunikaciju.")

        print("\nVrijeme izvodenja programa ovom obradom iznosi", end-start )
