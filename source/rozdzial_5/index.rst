================================================
Zapytania do bazy danych
================================================

:Autorzy:
    1. Oskar Wrona
    2. Kamil Lewandowski
    3. Adam Tarkowski

Cel rozdziału
=============

Celem rozdziału jest przedstawienie funkcji napisanych w języku Python,
które wykonują zapytania SQL do utworzonej wcześniej bazy danych sklepu
internetowego.

Funkcje zostały przygotowane osobno dla baz PostgreSQL oraz SQLite.
Ich wywołanie powoduje wykonanie odpowiedniego zapytania SQL do bazy danych
oraz zwrócenie wyniku w postaci tabelarycznej, możliwej do wyświetlenia
w środowisku JupyterLab.

Przygotowane funkcje służą do sprawdzenia działania bazy danych oraz wykonania
przykładowych analiz dotyczących klientów, zamówień, produktów, kategorii,
płatności, wysyłek i opinii.

Zakres zapytań
==============

Przygotowane zapytania obejmują następujące zagadnienia omawiane na zajęciach:

* selekcję danych i funkcje wierszowe,
* funkcje agregujące,
* połączenia i złączenia tabel,
* podzapytania,
* sortowanie oraz grupowanie danych.

Zakres tematyczny zapytań został dobrany do zastosowania utworzonej bazy danych,
czyli obsługi sklepu internetowego.

Przygotowane zapytania
======================

W ramach zadania utworzono pięć funkcji wykonujących zapytania do bazy danych:

#. ranking klientów według wartości zamówień,
#. sprzedaż według kategorii,
#. pełny widok zamówień,
#. najlepiej oceniane produkty,
#. produkty droższe od średniej ceny w swojej kategorii.

Każde zapytanie zostało przygotowane w dwóch wariantach: dla bazy PostgreSQL
oraz dla bazy SQLite. Dzięki temu możliwe jest sprawdzenie, czy obie bazy danych
zwracają zgodne wyniki dla tych samych danych wejściowych.

Weryfikacja działania w JupyterLab
==================================

Funkcje zostały wykonane i sprawdzone w środowisku JupyterLab. Notebooki
zawierające wywołania funkcji oraz wyniki zapytań znajdują się w następujących
lokalizacjach:

* ``Sprawozdanie_z_modelu/zapytania_do_bazy_wlasne_psql.ipynb`` - notebook z zapytaniami dla bazy PostgreSQL.
* ``Sprawozdanie_z_modelu/zapytania_do_bazy_wlasne_sqlite.ipynb`` - notebook z zapytaniami dla bazy SQLite.

W notebookach zweryfikowano, że przygotowane funkcje poprawnie wykonują
zapytania SQL oraz zwracają wyniki zgodne ze strukturą utworzonej bazy danych.

Organizacja modułów
===================

Funkcje zostały zapisane w dwóch modułach Pythona:

* ``zapytania_postgres.py`` - moduł zawierający funkcje wykonujące zapytania
  do bazy PostgreSQL,
* ``zapytania_sqlite.py`` - moduł zawierający funkcje wykonujące zapytania
  do bazy SQLite.

Moduły znajdują się w katalogu rozdziału:

.. code-block:: text

   source/
   └── rozdzial_5/
       ├── index.rst
       ├── zapytania_postgres.py
       └── zapytania_sqlite.py

Dzięki wykorzystaniu dokumentacji automatycznej Sphinx pobiera opisy funkcji
bezpośrednio z komentarzy dokumentacyjnych znajdujących się w kodzie źródłowym.
Pozwala to uniknąć ręcznego przepisywania tej samej dokumentacji w dwóch
miejscach.

Opis przygotowanych funkcji
===========================

Ranking klientów według wartości zamówień
-----------------------------------------

Funkcja wyświetla klientów, którzy wygenerowali największą wartość zamówień.
Zapytanie łączy dane z tabel klientów, zamówień oraz pozycji zamówień.
Następnie grupuje rekordy według klienta i oblicza liczbę zamówień oraz
łączną wartość zakupów.

W zapytaniu wykorzystano między innymi:

* ``JOIN``,
* ``COUNT()``,
* ``SUM()``,
* ``GROUP BY``,
* ``ORDER BY``.

Sprzedaż według kategorii
-------------------------

Funkcja przedstawia sprzedaż produktów z podziałem na kategorie. Dla każdej
kategorii obliczana jest liczba różnych produktów, liczba sprzedanych sztuk
oraz łączna wartość sprzedaży.

W zapytaniu wykorzystano między innymi:

* połączenie tabel kategorii, produktów i pozycji zamówień,
* funkcje agregujące,
* grupowanie danych według kategorii.

Pełny widok zamówień
--------------------

Funkcja zwraca pełny widok zamówień, obejmujący dane klienta, produktu,
pozycji zamówienia, płatności oraz wysyłki.

Zapytanie wykorzystuje wiele złączeń, w tym ``JOIN`` oraz ``LEFT JOIN``.
Dzięki temu możliwe jest pokazanie także takich zamówień, które nie mają
wszystkich powiązanych danych, na przykład wysyłki lub opinii.

Najlepiej oceniane produkty
---------------------------

Funkcja pokazuje produkty posiadające opinie użytkowników. Dla każdego produktu
obliczana jest średnia ocena oraz liczba opinii. Wyniki są sortowane według
średniej oceny oraz liczby opinii.

W zapytaniu wykorzystano:

* ``AVG()``,
* ``COUNT()``,
* ``GROUP BY``,
* połączenia tabel produktów, kategorii, producentów i opinii.

Produkty droższe od średniej ceny w kategorii
---------------------------------------------

Funkcja wyszukuje produkty, których aktualna cena jest wyższa niż średnia cena
produktów należących do tej samej kategorii.

Zapytanie wykorzystuje podzapytanie skorelowane. Dla każdego produktu liczona
jest średnia cena produktów w jego kategorii, a następnie wybierane są tylko
te produkty, których cena jest większa od tej średniej.

Dokumentacja funkcji PostgreSQL
===============================

Poniżej znajduje się automatycznie wygenerowana dokumentacja modułu
``zapytania_postgres.py``. Dokumentacja została pobrana z komentarzy
dokumentacyjnych funkcji zapisanych w kodzie źródłowym.

.. automodule:: zapytania_postgres
   :members:
   :undoc-members:
   :show-inheritance:

Dokumentacja funkcji SQLite
===========================

Poniżej znajduje się automatycznie wygenerowana dokumentacja modułu
``zapytania_sqlite.py``. Dokumentacja została pobrana z komentarzy
dokumentacyjnych funkcji zapisanych w kodzie źródłowym.

.. automodule:: zapytania_sqlite
   :members:
   :undoc-members:
   :show-inheritance:

Podsumowanie
============

W ramach rozdziału przygotowano funkcje wykonujące zapytania SQL do bazy danych
sklepu internetowego. Zapytania zostały dobrane tak, aby wykorzystywały różne
elementy języka SQL, w tym złączenia tabel, funkcje agregujące, grupowanie,
sortowanie oraz podzapytania.

Funkcje zostały przygotowane w dwóch wariantach: dla PostgreSQL oraz SQLite.
Pozwala to sprawdzić, czy obie wersje bazy danych zwracają zgodne wyniki dla
tych samych danych. Wyniki działania funkcji zostały zweryfikowane w notebookach
JupyterLab, a dokumentacja funkcji została wygenerowana automatycznie przy
użyciu mechanizmu ``autodoc`` dostępnego w Sphinx.
