#!/usr/bin/env python3
import argparse
import sys
import os
import tempfile
import subprocess
import string
import timeit
import textwrap

__version__ = '0.2'


class Kolory:
	rozowy = "\033[1m\033[95m"
	niebieski = "\033[1m\033[94m"
	zielony = "\033[1m\033[92m"
	zolty = "\033[1m\033[93m"
	czerwony = "\033[1m\033[91m"
	reset = "\033[1m\033[0m"
	
	poprawny = zielony
	niepoprawny = czerwony
	skonczony = zolty
	bledny = czerwony
	
	wlaczone = 0
	
	def wymus_wlaczenie():
		Kolory.wlaczone = 1
	
	def wylacz():
		if Kolory.wlaczone != 1:
			Kolory.rozowy = ""
			Kolory.niebieski = ""
			Kolory.zielony = ""
			Kolory.zolty = ""
			Kolory.czerwony = ""
			Kolory.reset = ""
			
			Kolory.poprawny = ""
			Kolory.niepoprawny = ""
			Kolory.skonczony = ""
			Kolory.bledny = ""	

class Opcje:
	# Sciezka do programu wykonywalnego
	program = ''
	
	# Sciezka do folderu z testami
	testy = ''
	
	# Czy testowac na kilku konkretnych testach
	tryb_testu = 0
	
	# Lista testow w trybie testu
	lista_testow = []
	
	# Czy wyswietlac czas dzialania programu
	pokaz_czas = 1
	
	# Czy w przypadku bledu wyswietlac wyjscia: programu i poprawnego
	pokaz_porownanie = 1
	
	# Czy pokazywac podsumowanie na samym koncu
	pokaz_podsumowanie = 1
	
	# Czy pokazywac, ze wystapila odpowiedz poprawna
	pokaz_testy_poprawne = 1
	
	# Czy pokazywac, ze wystapila odpowiedz niepoprawna
	pokaz_testy_niepoprawne = 1
	
	# Czy pokazywac, ze wystapila odpowiedz skonczona
	pokaz_testy_skonczone = 1
	
	# Czy pokazywac, ze wystapila odpowiedz skonczona
	pokaz_testy_bledne = 1
	
class Wyniki:
	def __init__(self):
		self.poprawne = 0 #program dal odpowiedz i jest ona poprawna
		self.niepoprawne = 0 #program dal odpowiedz i nie jest ona poprawna
		self.skonczone = 0 #program dal odpowiedz i nie wiadomo jaka jest prawidlowa
		self.bledne = 0 #program rzucil blad podczas uruchomienia
	
	def dodaj_poprawne(self):
		self.poprawne += 1
	
	def dodaj_niepoprawne(self):
		self.niepoprawne += 1
	
	def dodaj_skonczone(self):
		self.skonczone += 1
	
	def dodaj_bledne(self):
		self.bledne += 1
	
	def wez_poprawne(self):
		return self.poprawne
	
	def wez_niepoprawne(self):
		return self.niepoprawne
			
	def wez_skonczone(self):
		return self.skonczone
	
	def wez_bledne(self):
		return self.bledne

# Zrodlo: http://stackoverflow.com/a/32974697
class MultilineFormatter(argparse.HelpFormatter):
	def _fill_text(self, text, width, indent):
		text = self._whitespace_matcher.sub(' ', text).strip()
		paragraphs = text.split('|n ')
		multiline_text = ''
		for paragraph in paragraphs:
			formatted_paragraph = textwrap.fill(paragraph, width, initial_indent=indent, subsequent_indent=indent) + '\n'
			multiline_text = multiline_text + formatted_paragraph
		return multiline_text


def sprawdz_terminal():
	if sys.stdout.isatty() == False:
		Kolory.wylacz()

def wczytaj():
	parser = argparse.ArgumentParser(__file__, formatter_class=MultilineFormatter, 
	description="Tester programow. Skrypt uruchamia program na serii testow, przekierowuje wejscie programu i sprawdza czy wyjscie programu jest takie samo jak wyjscie testu. Mozliwe odpowiedzi to: OK, SKONCZONE, ZLE, BLAD WYKONANIA.|n |n OK - program zakonczyl sie i odpowiedz sie zgadza |n SKONCZONE - program zakonczyl sie, ale nie ma z czym porownac odpowiedzi |n ZLE - program zakonczyl sie, ale dal inna odpowiedz |n BLAD WYKONANIA - program zwrocil kod wyjscia rozny od zera")
	
	parser.add_argument("PROGRAM", type=str, help="sciezka do programu wykonywalnego")
	
	parser.add_argument("TESTY", type=str, help="sciezka do folderu z testami (zawiera pliki *.in oraz *.out)")
	
	parser.add_argument("--test", type=str, action='append', help="nazwa testu bez sufiksu .in; program jest testowany na konkretnym tescie; parametr moze wystapic wiecej niz raz")
	
	parser.add_argument("--portable", action="store_true", help="alias dla -TC")
	
	parser.add_argument("--quiet", action="store_true", help="alias dla -O")
		
	parser.add_argument("-T", "--no-time", action="store_true", help="nie wyswietlaj czasu dzialania programu")
	
	parser.add_argument("-C", "--no-compare", action="store_true", help="nie wyswietlaj porownania odpowiedzi blednej i poprawnej")
	
	parser.add_argument("-O", "--no-ok", action="store_true", help="nie wyswietlaj testow, ktore program przeszedl poprawnie")
	
	parser.add_argument("-E", "--no-error", action="store_true", help="nie wyswietlaj testow, ktorych program nie przeszedl poprawnie")
	
	color = parser.add_mutually_exclusive_group()
	
	color.add_argument("--color", action="store_true", help="wymus wlaczenie kolorow")
	
	color.add_argument("--no-color", action="store_true", help="wymus wylaczenie kolorow")
	
	parser.add_argument("--no-summary", action="store_true", help="nie wyswietlaj podsumowania")
	
	parser.add_argument("-V", "--version", action="version", version=__version__)
	
	return parser.parse_args()

def inicjuj_zmienne(arg):
	
	Opcje.program = os.path.abspath(arg.PROGRAM)
	
	Opcje.testy = os.path.abspath(arg.TESTY)
	
	if arg.test:
		Opcje.tryb_testu = 1
		for test in arg.test:
			Opcje.lista_testow.append(test)
	
	if arg.portable:
		Opcje.pokaz_czas = 0
		Opcje.pokaz_porownanie = 0
	
	if arg.quiet:
		Opcje.pokaz_testy_poprawne = 0
		Opcje.pokaz_testy_skonczone = 0
	
	if arg.no_time:
		Opcje.pokaz_czas = 0
	
	if arg.no_compare:
		Opcje.pokaz_porownanie = 0
	
	if arg.no_ok:
		Opcje.pokaz_testy_poprawne = 0
		Opcje.pokaz_testy_skonczone = 0
	
	if arg.no_error:
		Opcje.pokaz_testy_bledne = 0
		Opcje.pokaz_testy_niepoprawne = 0
	
	if arg.color:
		Kolory.wymus_wlaczenie()
	
	if arg.no_color:
		Kolory.wylacz()
	
	if arg.no_summary:
		Opcje.pokaz_podsumowanie = 0
	
def sprawdz_pliki():
	if not os.path.exists(Opcje.testy):
		print("Folder z testami nie istnieje:\n"+Opcje.testy)
		#~ raise FileNotFoundError
		raise SystemExit
	
	if not os.path.isfile(Opcje.program):
		print("Plik wykonywalny nie istnieje:\n"+Opcje.program)
		#~ raise FileNotFoundError
		raise SystemExit

def pokaz_podsumowanie(wyniki):
	print("\n\n-----")
	print("Poprawne: "+Kolory.poprawny+str(wyniki.wez_poprawne())+Kolory.reset)
	if wyniki.wez_skonczone() > 0:
		print("Skonczone: "+Kolory.skonczony+str(wyniki.wez_skonczone())+Kolory.reset)
	print("Niepoprawne: "+Kolory.niepoprawny+str(wyniki.wez_niepoprawne())+Kolory.reset)
	print("Bledy wykonania: "+Kolory.bledny+str(wyniki.wez_bledne())+Kolory.reset)

def wypisz_czas(czas):
	if Opcje.pokaz_czas:
		print("czas: {:.2f}".format(czas))
		print()

def wypisz(nazwa_testu, status, czas=-1, porownanie=''):
	odstep = ":\t"
	if status == 0: #poprawne
		if Opcje.pokaz_testy_poprawne:
			print("Test "+nazwa_testu+odstep+Kolory.poprawny+"OK"+Kolory.reset)
			wypisz_czas(czas)
	elif status == 1: #niepoprawne
		if Opcje.pokaz_testy_niepoprawne:
			print("Test "+nazwa_testu+odstep+Kolory.niepoprawny+"ZLE"+Kolory.reset)
			if Opcje.pokaz_porownanie:
				print(porownanie)
				print("(wynik programu | prawidlowy wynik)")
			wypisz_czas(czas)
	elif status == 2: #skonczone
		if Opcje.pokaz_testy_skonczone:
			print("Test "+nazwa_testu+odstep+Kolory.skonczony+"SKONCZONY"+Kolory.reset)
			wypisz_czas(czas)
	elif status == 3: #bledy wykonania
		if Opcje.pokaz_testy_bledne:
			print("Test "+nazwa_testu+odstep+Kolory.bledny+"BLAD WYKONANIA"+Kolory.reset)
			wypisz_czas(czas)
	else:
		pass #nic nie rob

def prefix(tekst, n):
	lista = tekst.split('\n',1)
	tekst = lista[0]
	if len(tekst) <= n:
		if len(lista) > 1:
			if len(tekst) <= n-3:
				return "%s..."%(tekst[:n])
			else:
				return "%s..."%(tekst[:n-3])
		else:
			return tekst
	else:
		return "%s..."%(tekst[:n-3])

def testuj(nazwa_testu, test_in, test_out, wyniki):
	with open(test_in, 'rt') as f_in, tempfile.SpooledTemporaryFile(mode='r+t') as f_out, tempfile.SpooledTemporaryFile(mode='r+t') as f_returncode:
		proces = subprocess.Popen(Opcje.program, stdin=f_in, stdout=f_out, stderr=subprocess.DEVNULL, shell=False)
		proces.wait()
		
		# TODO - poprawic aby nie uruchamiac drugi raz programu #
		# Moze pomoze:
		# subprocess.run() -> https://docs.python.org/3/library/subprocess.html#subprocess.run
		if Opcje.pokaz_czas:
			try:
				start = timeit.default_timer()
				czas = timeit.timeit(stmt ="subprocess.check_call(PROGRAM, stdin=f_in, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False)", setup="import subprocess; import os; PROGRAM='"+Opcje.program+"'; f_in = open( '"+test_in+"' , 'r');", number=1)
			except:
				czas = timeit.default_timer() - start
		else:
			czas = 0
		# ##### #
		
		if proces.returncode != 0:
			wyniki.dodaj_bledne()
			wypisz(nazwa_testu, 3, czas)
		else:
			try:
				with open(test_out , 'rt') as f_answer:
					f_out.seek(0)
					if f_answer.read().strip() == f_out.read().strip():
						wyniki.dodaj_poprawne()
						wypisz(nazwa_testu, 0, czas)
					else:
						wyniki.dodaj_niepoprawne()
						f_answer.seek(0)
						f_out.seek(0)
						# Wpisane na stale do kodu liczby 100 i 25. Hmm...
						answer = f_answer.read(100).strip()
						out = f_out.read(100).strip()
						porownanie = prefix(out.strip(),25)+"  |  "+prefix(answer.strip(),25)
						wypisz(nazwa_testu, 1, czas, porownanie)
			except OSError:
				wyniki.dodaj_skonczone()
				wypisz(nazwa_testu, 2, czas)

def potestuj():
	wyniki = Wyniki()
	# Tworze liste testow na slowniku. Troche na okolo, ale w ten sposob
	# niezaleznie od wielkosci liter dobrze sparuje pliki *.in + *.out
	testy = {}
	
	if Opcje.tryb_testu:
		for nazwa in Opcje.lista_testow:
			for plik in os.listdir(Opcje.testy):
				if plik.lower().endswith('.in') and nazwa == os.path.splitext(plik)[0]:
					plik = os.path.join(Opcje.testy, plik)
					testy[nazwa] = (plik, '')
			
			for plik in os.listdir(Opcje.testy):
				if plik.lower().endswith('.out') and nazwa == os.path.splitext(plik)[0]:
					if nazwa in testy:
						test = testy[nazwa]
						plik = os.path.join(Opcje.testy, plik)
						testy[nazwa] = (test[0], plik)
	else:
		for plik in os.listdir(Opcje.testy):
			if plik.lower().endswith('.in'):
				nazwa = os.path.splitext(plik)[0]
				plik = os.path.join(Opcje.testy, plik)
				testy[nazwa] = (plik, '')
		
		for plik in os.listdir(Opcje.testy):
			if plik.lower().endswith('.out'):
				nazwa = os.path.splitext(plik)[0]
				if nazwa in testy:
					test = testy[nazwa]
					plik = os.path.join(Opcje.testy, plik)
					testy[nazwa] = (test[0], plik)
	
	for nazwa_testu,test in sorted(testy.items()):
		testuj(nazwa_testu, test[0], test[1], wyniki)
	
	if Opcje.pokaz_podsumowanie:
		pokaz_podsumowanie(wyniki)

def main():
	argumenty = wczytaj()
	inicjuj_zmienne(argumenty)
	sprawdz_terminal()
	sprawdz_pliki()
	potestuj()
	
	raise SystemExit

if __name__=="__main__":
	# minimalna wersja pythona:
	# 3.0
	# 3.2 - PEP 389, stworzono modul argparse
	# 3.3 - PEP 3151, wyjatki OSError oraz IOError znacza to samo
	# 3.3 - subprocess wprowadzona nowa stala DEVNULL
	min_version = (3,3)
	if sys.version_info >= min_version:
		main()
	else:
		print("Wersja pythona:  "+str(sys.version_info[0])+"."+str(sys.version_info[1]))
		print("Wymagana wersja pythona:  >="+str(min_version[0])+"."+str(min_version[1]))
