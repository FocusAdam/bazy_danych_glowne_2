"""
Moduł zapytania_sqlite
======================

Moduł zawiera funkcje wykonujące przykładowe zapytania SQL do bazy danych
sklepu internetowego w SQLite. Funkcje zakładają, że w środowisku,
w którym są uruchamiane, istnieje już obiekt ``conn`` utworzony przy
pomocy biblioteki ``sqlite3``, np. ``conn = sqlite3.connect("sklep.db")``.

Każda funkcja wykonuje zapytanie typu SELECT i zwraca wynik jako obiekt
``pandas.DataFrame``. Zapytania odpowiadają tematyce bazy sklepu internetowego
i wykorzystują między innymi złączenia, agregacje, grupowanie oraz podzapytania.
"""

import pandas as pd


def wykonaj_zapytanie_sqlite(polecenie):
    """
    Wykonuje zapytanie SQL w bazie SQLite i zwraca wynik jako DataFrame.

    Cel funkcji:
        Funkcja pomocnicza odpowiada za wykonanie przekazanego zapytania SQL
        przy użyciu istniejącego połączenia SQLite.

    Parametry:
        polecenie:
            Tekst zapytania SQL typu SELECT, które ma zostać wykonane.

    Dane wejściowe:
        Funkcja wymaga, aby wcześniej istniała zmienna globalna ``conn``
        reprezentująca połączenie z bazą SQLite.

    Dane wyjściowe:
        Obiekt ``pandas.DataFrame`` zawierający wynik zapytania.

    Opis działania:
        Funkcja wykorzystuje ``pandas.read_sql_query()``, wykonuje przekazane
        zapytanie SQL i zwraca wynik w postaci tabeli DataFrame.
    """
    return pd.read_sql_query(polecenie, conn)


# ============================================================
# 1. Ranking klientów według wartości zamówień
# ============================================================

def ranking_klientow_sqlite():
    """
    Wyświetla ranking klientów według łącznej wartości złożonych zamówień.

    Cel funkcji:
        Funkcja pozwala określić, którzy klienci wygenerowali największą
        wartość sprzedaży w sklepie internetowym.

    Wykorzystywane tabele:
        - ``Klienci``
        - ``Zamowienia``
        - ``Pozycje_Zamowienia``

    Zastosowane elementy SQL:
        - złączenia ``JOIN``
        - funkcja agregująca ``COUNT()``
        - funkcja agregująca ``SUM()``
        - ``GROUP BY``
        - ``ORDER BY``

    Dane wejściowe:
        Funkcja nie przyjmuje parametrów. Korzysta z istniejącego połączenia
        ``conn`` do bazy SQLite.

    Dane wyjściowe:
        DataFrame zawierający identyfikator klienta, imię, nazwisko, adres
        e-mail, liczbę zamówień oraz łączną wartość zamówień.

    Opis działania:
        Zapytanie łączy klientów z zamówieniami oraz pozycjami zamówień.
        Następnie grupuje dane według klienta i oblicza sumaryczną wartość
        zakupów. Wyniki sortowane są malejąco według wartości zamówień.
    """
    polecenie = """
    SELECT
        k.ID_Klienta,
        k.Imie,
        k.Nazwisko,
        k.Email,
        COUNT(DISTINCT z.ID_Zamowienia) AS Liczba_zamowien,
        COALESCE(SUM(pz.Ilosc * pz.Cena_historyczna), 0) AS Wartosc_zamowien
    FROM Klienci k
    JOIN Zamowienia z
        ON k.ID_Klienta = z.ID_Klienta
    JOIN Pozycje_Zamowienia pz
        ON z.ID_Zamowienia = pz.ID_Zamowienia
    GROUP BY
        k.ID_Klienta,
        k.Imie,
        k.Nazwisko,
        k.Email
    ORDER BY
        Wartosc_zamowien DESC,
        k.ID_Klienta ASC;
    """

    return wykonaj_zapytanie_sqlite(polecenie)


# ============================================================
# 2. Sprzedaż według kategorii
# ============================================================

def sprzedaz_wedlug_kategorii_sqlite():
    """
    Przedstawia sprzedaż produktów z podziałem na kategorie.

    Cel funkcji:
        Funkcja służy do sprawdzenia, które kategorie produktów generują
        największą sprzedaż w sklepie internetowym.

    Wykorzystywane tabele:
        - ``Kategorie``
        - ``Produkty``
        - ``Pozycje_Zamowienia``

    Zastosowane elementy SQL:
        - złączenia ``JOIN``
        - funkcje agregujące ``COUNT()`` i ``SUM()``
        - ``GROUP BY``
        - ``ORDER BY``

    Dane wejściowe:
        Funkcja nie przyjmuje parametrów. Korzysta z istniejącego połączenia
        ``conn`` do bazy SQLite.

    Dane wyjściowe:
        DataFrame zawierający identyfikator kategorii, nazwę kategorii,
        liczbę produktów, liczbę sprzedanych sztuk oraz wartość sprzedaży.

    Opis działania:
        Zapytanie łączy kategorie z produktami oraz pozycjami zamówień.
        Dla każdej kategorii obliczana jest liczba różnych produktów,
        liczba sprzedanych sztuk oraz całkowita wartość sprzedaży.
    """
    polecenie = """
    SELECT
        kat.ID_Kategorii,
        kat.Nazwa_kategorii,
        COUNT(DISTINCT p.ID_Produktu) AS Liczba_produktow,
        COALESCE(SUM(pz.Ilosc), 0) AS Liczba_sprzedanych_sztuk,
        COALESCE(SUM(pz.Ilosc * pz.Cena_historyczna), 0) AS Wartosc_sprzedazy
    FROM Kategorie kat
    JOIN Produkty p
        ON kat.ID_Kategorii = p.ID_Kategorii
    JOIN Pozycje_Zamowienia pz
        ON p.ID_Produktu = pz.ID_Produktu
    GROUP BY
        kat.ID_Kategorii,
        kat.Nazwa_kategorii
    ORDER BY
        Wartosc_sprzedazy DESC,
        kat.ID_Kategorii ASC;
    """

    return wykonaj_zapytanie_sqlite(polecenie)


# ============================================================
# 3. Pełny widok zamówień
# ============================================================

def pelne_zamowienia_sqlite():
    """
    Wyświetla pełny widok zamówień z danymi klienta, produktu, płatności i wysyłki.

    Cel funkcji:
        Funkcja pozwala przeanalizować kompletne informacje o zamówieniach
        znajdujących się w bazie sklepu internetowego.

    Wykorzystywane tabele:
        - ``Zamowienia``
        - ``Klienci``
        - ``Pozycje_Zamowienia``
        - ``Produkty``
        - ``Platnosci``
        - ``Wysylki``

    Zastosowane elementy SQL:
        - ``JOIN``
        - ``LEFT JOIN``
        - wyrażenie obliczeniowe ``Ilosc * Cena_historyczna``
        - ``ORDER BY``

    Dane wejściowe:
        Funkcja nie przyjmuje parametrów. Korzysta z istniejącego połączenia
        ``conn`` do bazy SQLite.

    Dane wyjściowe:
        DataFrame zawierający pełny opis zamówienia: dane klienta, produkt,
        ilość, cenę historyczną, wartość pozycji, status płatności oraz status
        wysyłki.

    Opis działania:
        Zapytanie rozpoczyna od tabeli zamówień, następnie dołącza klientów,
        pozycje zamówień, produkty, płatności i wysyłki. Dzięki ``LEFT JOIN``
        możliwe jest pokazanie także zamówień, które nie posiadają jeszcze
        wszystkich danych, np. wysyłki.
    """
    polecenie = """
    SELECT
        z.ID_Zamowienia,
        z.Data_zamowienia,
        z.Status_zamowienia,
        k.ID_Klienta,
        k.Imie,
        k.Nazwisko,
        k.Email,
        p.ID_Produktu,
        p.Nazwa AS Produkt,
        pz.Ilosc,
        pz.Cena_historyczna,
        pz.Ilosc * pz.Cena_historyczna AS Wartosc_pozycji,
        pl.Metoda_platnosci,
        pl.Status_platnosci,
        w.Firma_kurierska,
        w.Numer_listu,
        w.Status_paczki
    FROM Zamowienia z
    JOIN Klienci k
        ON z.ID_Klienta = k.ID_Klienta
    LEFT JOIN Pozycje_Zamowienia pz
        ON z.ID_Zamowienia = pz.ID_Zamowienia
    LEFT JOIN Produkty p
        ON pz.ID_Produktu = p.ID_Produktu
    LEFT JOIN Platnosci pl
        ON z.ID_Zamowienia = pl.ID_Zamowienia
    LEFT JOIN Wysylki w
        ON z.ID_Zamowienia = w.ID_Zamowienia
    ORDER BY
        z.ID_Zamowienia ASC,
        p.ID_Produktu ASC;
    """

    return wykonaj_zapytanie_sqlite(polecenie)


# ============================================================
# 4. Najlepiej oceniane produkty
# ============================================================

def najlepiej_oceniane_produkty_sqlite():
    """
    Wyświetla najlepiej oceniane produkty wraz z kategorią i producentem.

    Cel funkcji:
        Funkcja pozwala sprawdzić, które produkty uzyskały najwyższe oceny
        wystawione przez klientów.

    Wykorzystywane tabele:
        - ``Produkty``
        - ``Kategorie``
        - ``Producenci``
        - ``Opinie``

    Zastosowane elementy SQL:
        - złączenia ``JOIN``
        - funkcja agregująca ``AVG()``
        - funkcja agregująca ``COUNT()``
        - ``GROUP BY``
        - ``ORDER BY``

    Dane wejściowe:
        Funkcja nie przyjmuje parametrów. Korzysta z istniejącego połączenia
        ``conn`` do bazy SQLite.

    Dane wyjściowe:
        DataFrame zawierający identyfikator produktu, nazwę produktu,
        kategorię, producenta, średnią ocenę oraz liczbę opinii.

    Opis działania:
        Zapytanie łączy produkty z kategoriami, producentami i opiniami.
        Następnie dla każdego produktu oblicza średnią ocenę oraz liczbę opinii.
        Wyniki są sortowane od najwyżej ocenianych produktów.
    """
    polecenie = """
    SELECT
        p.ID_Produktu,
        p.Nazwa AS Produkt,
        kat.Nazwa_kategorii,
        pr.Nazwa_producenta,
        ROUND(AVG(o.Ocena), 2) AS Srednia_ocena,
        COUNT(o.ID_Opinii) AS Liczba_opinii
    FROM Produkty p
    JOIN Kategorie kat
        ON p.ID_Kategorii = kat.ID_Kategorii
    JOIN Producenci pr
        ON p.ID_Producenta = pr.ID_Producenta
    JOIN Opinie o
        ON p.ID_Produktu = o.ID_Produktu
    GROUP BY
        p.ID_Produktu,
        p.Nazwa,
        kat.Nazwa_kategorii,
        pr.Nazwa_producenta
    ORDER BY
        Srednia_ocena DESC,
        Liczba_opinii DESC,
        p.ID_Produktu ASC;
    """

    return wykonaj_zapytanie_sqlite(polecenie)


# ============================================================
# 5. Produkty droższe od średniej ceny w swojej kategorii
# ============================================================

def produkty_drozsze_od_sredniej_sqlite():
    """
    Wyszukuje produkty droższe od średniej ceny produktów w tej samej kategorii.

    Cel funkcji:
        Funkcja pozwala wskazać produkty, których aktualna cena jest wyższa niż
        przeciętna cena produktów należących do tej samej kategorii.

    Wykorzystywane tabele:
        - ``Produkty``
        - ``Kategorie``

    Zastosowane elementy SQL:
        - złączenie ``JOIN``
        - podzapytanie skorelowane
        - funkcja agregująca ``AVG()``
        - ``WHERE``
        - ``ORDER BY``

    Dane wejściowe:
        Funkcja nie przyjmuje parametrów. Korzysta z istniejącego połączenia
        ``conn`` do bazy SQLite.

    Dane wyjściowe:
        DataFrame zawierający produkt, kategorię, aktualną cenę oraz średnią
        cenę produktów w tej samej kategorii.

    Opis działania:
        Dla każdego produktu wykonywane jest podzapytanie obliczające średnią
        cenę produktów z tej samej kategorii. Następnie zwracane są tylko te
        produkty, których cena jest większa od obliczonej średniej.
    """
    polecenie = """
    SELECT
        p.ID_Produktu,
        p.Nazwa AS Produkt,
        kat.Nazwa_kategorii,
        p.Cena_aktualna,
        ROUND((
            SELECT AVG(p2.Cena_aktualna)
            FROM Produkty p2
            WHERE p2.ID_Kategorii = p.ID_Kategorii
        ), 2) AS Srednia_cena_w_kategorii
    FROM Produkty p
    JOIN Kategorie kat
        ON p.ID_Kategorii = kat.ID_Kategorii
    WHERE p.Cena_aktualna > (
        SELECT AVG(p2.Cena_aktualna)
        FROM Produkty p2
        WHERE p2.ID_Kategorii = p.ID_Kategorii
    )
    ORDER BY
        kat.Nazwa_kategorii ASC,
        p.Cena_aktualna DESC,
        p.ID_Produktu ASC;
    """

    return wykonaj_zapytanie_sqlite(polecenie)


__all__ = [
    "wykonaj_zapytanie_sqlite",
    "ranking_klientow_sqlite",
    "sprzedaz_wedlug_kategorii_sqlite",
    "pelne_zamowienia_sqlite",
    "najlepiej_oceniane_produkty_sqlite",
    "produkty_drozsze_od_sredniej_sqlite",
]
