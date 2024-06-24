# Dylemat Więźnia - Aplikacja Turniejowa

## Opis Aplikacji
Aplikacja symuluje turniej Axelroda, który polega na rozeg raniu pomiędzy
graczami pojedynków obierając pewną strategię. Każdy pojedynek to podjęcie decyzji czy
chcemy donieść na naszego przeciwnika(D) lub zachować milczenie(M). W przypadku gdy obie
strony postanowią milczeć dostają one 3 lata odsiadki. W sytuacji, gdzie jedna strona milczy, a
druga donosi, gracz który postanowił milczeć dostaje 10 lat odsiadki, natomiast gracz który
doniósł nie ponosi żadnych konsekwencji. Ostatnia możliwość, to gdy oboje gracze donoszą, co
skutkuje tym, że obaj dostają złagodzony wyrok 7 lat odsiadki. 

Nasza aplikacja zawiera 6 strategii:
- ZawszeMilcz (gracz zawsze milczy)
- ZawszeDonos (gracz zawsze donosi)
- TitForTat (gracz pierwszy ruch zawsze milczy, a potem wykonuje ostatni ruch przeciwnika)
- Losowo (gracz pseudolosowo wybiera czy milczeć lub donosić)
- Uraza (tak długo jak przeciwnik nie zdradził i nie doniósł, decyzją gracza zawsze będzie milczenie, w przypadku donosu, trzymana jest uraza i do końca decyzją jest donos)
- PrzebaczajaceTitForTat (gracz postępuje tak samo jak w przypadku strategii TitForTat, z jedną zmianą, a mianowicie, w przypadku donosu przez przeciwnika w poprzedniej rundzie, istnieje 20% szans na to, że zostanie to przebaczone i gracz będzie milczał)

## Struktura aplikacji 
App.py - to główny plik zawierający aplikację 

test_unit.py - to plik zawierający testy jednostkowe

test_integration.py - to plik zawierający testy integracyjne 

test_acceptance.py - to plik zawierający testy akceptacyjne

templates / index.html - to plik zawierający kod strony internetowej, na której wyświetla się aplikacja


### Testy Jednostkowe


1. **Testy metod strategii**:
    - Sprawdzają, czy metoda `strategy` w każdej klasie strategii (`ZawszeMilcz`, `ZawszeDonos`, `TitForTat`, `Losowo`, `Uraza`, `PrzebaczajaceTitForTat`) zwraca poprawne wartości dla różnych wejść.

    ```python
    class TestStrategies(unittest.TestCase):

        def test_zawsze_milcz(self):
            player = ZawszeMilcz("Test")
            self.assertEqual(player.strategy([]), 'M')
        
        def test_zawsze_donos(self):
            player = ZawszeDonos("Test")
            self.assertEqual(player.strategy([]), 'D')

        def test_tit_for_tat(self):
            player = TitForTat("Test")
            self.assertEqual(player.strategy([]), 'M')
            self.assertEqual(player.strategy(['D']), 'D')
        
        def test_losowo(self):
            player = Losowo("Test")
            self.assertIn(player.strategy([]), ['M', 'D'])

        def test_uraza(self):
            player = Uraza("Test")
            self.assertEqual(player.strategy([]), 'M')
            self.assertEqual(player.strategy(['D']), 'D')

        def test_przebaczajace_tit_for_tat(self):
            player = PrzebaczajaceTitForTat("Test")
            self.assertEqual(player.strategy([]), 'M')
            self.assertIn(player.strategy(['D']), ['M', 'D'])

    ```

2. **Testy funkcji `play_round`**:
    - Sprawdzają, czy funkcja `play_round` poprawnie aktualizuje historię ruchów.

    ```python
    class TestPlayRound(unittest.TestCase):

        def test_play_round(self):
            player1 = ZawszeMilcz("Test")
            player2 = ZawszeDonos("Test")
            history1, history2 = play_round(player1, player2, [], [])
            self.assertEqual(history1, ['M'])
            self.assertEqual(history2, ['D'])

    ```

3. **Testy funkcji `calculate_scores`**:
    - Sprawdzają, czy funkcja `calculate_scores` poprawnie oblicza wyniki na podstawie historii ruchów.

    ```python
    class TestCalculateScores(unittest.TestCase):

        def test_calculate_scores(self):
            history1 = ['M', 'D']
            history2 = ['M', 'M']
            score1, score2 = calculate_scores(history1, history2)
            self.assertEqual(score1, 3)
            self.assertEqual(score2, 13)

    ```

### Testy Integracyjne 

1. **Testy funkcji `play_game`**:
    - Sprawdzają, czy funkcja `play_game` poprawnie przeprowadza całą grę pomiędzy dwoma graczami.

    ```python
    class TestPlayGame(unittest.TestCase):

        def test_play_game(self):
            player1 = ZawszeMilcz("Test")
            player2 = ZawszeDonos("Test")
            score1, score2 = play_game(player1, player2, rounds=10)
            self.assertEqual(score1, 100)
            self.assertEqual(score2, 0)

    ```

2. **Testy funkcji `run_tournament`**:
    - Sprawdzają, czy funkcja `run_tournament` poprawnie przeprowadza cały turniej i zwraca wyniki.

    ```python
    class TestRunTournament(unittest.TestCase):

        def test_run_tournament(self):
            players = [ZawszeMilcz("Zawsze milcz"), ZawszeDonos("Zawsze donos")]
            results, total_scores = run_tournament(players)
            self.assertIn("Zawsze milcz", results)
            self.assertIn("Zawsze donos", results)

    ```

### Testy Akceptacyjne 

1. **Testy end-to-end**:
    - Testują aplikację w rzeczywistych warunkach, sprawdzając, czy interfejs użytkownika poprawnie wyświetla wyniki turnieju.

    ```python
    class TestAcceptance(unittest.TestCase):

        @classmethod
        def setUpClass(cls):
            cls.server_thread = Thread(target=app.run, kwargs={'port': 8943, 'debug': False, 'use_reloader': False})
            cls.server_thread.setDaemon(True)
            cls.server_thread.start()
            cls.driver = webdriver.Chrome()

        @classmethod
        def tearDownClass(cls):
            cls.driver.quit()
            # To stop the Flask server you may need to use another method depending on your environment.

        def test_index(self):
            self.driver.get('http://127.0.0.1:8943/')
            self.assertIn("Tournament Results", self.driver.page_source)

    ```
## Wyniki testów

Testy jednostkowe
```python 
........
----------------------------------------------------------------------
Ran 8 tests in 0.002s

OK
```

Testy integracyjne 
```python 
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
```

Testy akceptacyjne 
```python 
DeprecationWarning: setDaemon() is deprecated, set the daemon attribute instead
  cls.server_thread.setDaemon(True)
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8943
Press CTRL+C to quit

DevTools listening on ws://127.0.0.1:51377/devtools/browser/cb704c8a-be85-489c-91d9-8b6e920feae7
127.0.0.1 - - [24/Jun/2024 14:02:39] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [24/Jun/2024 14:02:39] "GET /favicon.ico HTTP/1.1" 404 -
.
----------------------------------------------------------------------
Ran 1 test in 4.690s

OK
```

## Wykorzystane narzędzia i biblioteki 


- Flask

Flask to framework webowy dla Pythona, używany jest do tworzenia serwera aplikacji.

- Flask-Testing

Flask-Testing to rozszerzenie Flask, które dostarcza narzędzi do testowania aplikacji opartych na Flask. 

- Selenium

Selenium to narzędzie do automatyzacji przeglądarek internetowych. Używane jest do testowania interfejsów użytkownika w aplikacjach webowych, pozwala na automatyzację interakcji z przeglądarką, takich jak wprowadzanie danych, klikanie przycisków itp.

- unittest

unittest to wbudowany moduł w Pythonie, który zapewnia wsparcie dla tworzenia i uruchamiania testów. 
    
