# program-tester.py
Skrypt pomagający testować programy wykonywalne.

## Opis
Skrypt powstał podczas moich zmagań z Olimpiadą Informatyczną. Z czasem potrafił coraz więcej, a że wydaje mi się użyteczny, postanowiłem go upublicznić.

Skrypt uruchamia program na paczce testów i porównuje standardowe wyjście z plikiem `*.out`. Nazwy testów muszą być postaci `*.in` dla danych wejściowych oraz `*.out` dla danych wyjściowych. Skrypt sprawdza tylko standardowe wyjście, wyjście diagnostyczne jest ignorowane.

Testy należy zdobyć samodzielnie :)

## Instalacja
Poniższe polecenia należy wykonać w konsoli. Zakładam, że na co dzień korzystasz z basha. Jeśli nie, wprowadź odpowiednie poprawki.

### Minimalna instalacja
Najpierw pobierz skrypt `program-tester.py`:

    # wget -O program-tester.py https://github.com/kotoko/program-tester-python/raw/master/program-tester.py

Potem nadaj mu prawa do wykonywania:

    # chmod +x program-tester.py

Na końcu uruchom:

    # ./program-tester

### Pełna instalacja
Zaletami pełnej instalacji są: łatwość aktualizacji skryptu, obsługa języka polskiego, wygoda uruchomienia skryptu. Wymaganiem jest wcześniejsze zainstalowanie programu **git**.

Zacznij od pobrania całego projektu:

    # git clone https://github.com/kotoko/program-tester-python.git -b master --single-branch ~/.program-tester

Nadaj skryptowi uprawnienia do wykonywania:

    # chmod +x ~/.program-tester/program-tester.py

Potem stwórz plik `~/.program-tester-update.sh`:

    # nano -w ~/.program-tester-update.sh

Oraz wklej do niego kod aktualizujący skrypt:

```bash
#!/bin/bash
# script's installation directory
DIRECTORY="$HOME/.program-tester/"

if [ ! -d "$DIRECTORY" ]; then
    echo "Missing directory: $DIRECTORY"
    exit 1
fi

# go to directory
cd "$DIRECTORY"

# clenup directory
git reset --hard origin/master
git clean -f -d

# update script
git pull

exit
```

Zapisz plik i zamknij edytor. Nadaj uprawnienia do wykonywania:

    # chmod +x ~/.program-tester-update.sh

Dodaj aliasy, by można było łatwo uruchomić skrypt:

    # echo 'alias program-tester="~/.program-tester/program-tester.py"' >> ~/.bash_aliases
    # echo 'alias program-tester-update="~/.program-tester-update.sh"' >> ~/.bash_aliases

Na końcu zrestartuj wszystkie konsole, które były wcześniej uruchomione, żeby zmiany weszły w życie. Wylogowanie się i zalogowanie ponownie powinno wystarczyć.

Aby uruchomić skrypt wpisz:

    # program-tester

Aby zaktualizować skrypt do najnowszej wersji wpisz:

    # program-tester-update

## TODO
- [ ] zmierzyć zużytą pamięć przez program
- [ ] nie uruchamiać programu po raz drugi podczas mierzenia czasu

