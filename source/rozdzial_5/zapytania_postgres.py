"""
Moduł zapytania_postgres
========================

Moduł zawiera funkcje wykonujące przykładowe zapytania SQL do bazy danych
sklepu internetowego w PostgreSQL. Funkcje zakładają, że w środowisku,
w którym są uruchamiane, istnieje już obiekt ``dbEngine`` utworzony przy
pomocy SQLAlchemy, np. ``dbEngine = create_engine(connection)``.

Każda funkcja wykonuje zapytanie typu SELECT i zwraca wynik jako obiekt
``pandas.DataFrame``. Zapytania odpowiadają tematyce bazy sklepu internetowego
i wykorzystują między innymi złączenia, agregacje, grupowanie oraz podzapytania.
"""

import pandas as pd
from sqlalchemy import text


def wykonaj_zapytanie_postgres(polecenie):
    """
    Wykonuje zapytanie SQL w bazie PostgreSQL i zwraca wynik jako DataFrame.

    Cel funkcji:
        Funkcja pomocnicza odpowiada za wykonanie przekazanego zapytania SQL
        przy użyciu istniejącego połączenia SQLAlchemy.

    Parametry:
        polecenie:
            Tekst zapytania SQL typu SELECT, które ma zostać wykonane.

    Dane wejściowe:
        Funkcja wymaga, aby wcześniej istniała zmienna globalna ``dbEngine``
        reprezentująca silnik połączenia z bazą PostgreSQL.

    Dane wyjściowe:
        Obiekt ``pandas.DataFrame`` zawierający wynik zapytania.

    Opis działania:
        Funkcja otwiera połączenie z bazą danych, wykonuje zapytanie za pomocą
        ``connection.execute(text(polecenie))``, pobiera nazwy kolumn oraz
        wszystkie rekordy, a następnie zwraca wynik w postaci tabeli DataFrame.
    """
    with dbEngine.connect() as connection:
        tabela = connection.execute(text(polecenie))
        connection.commit()

        kolumny = tabela.keys()
        dane = tabela.fetchall()

    return pd.DataFrame(dane, columns=kolumny)


# ============================================================
# 1. Ranking klientów według wartości zamówień
# ============================================================

def ranking_klientow_postgres():
    """
    Wyświetla ranking klientów według łącznej wartości złożonych zamówień.

    Cel funkcji:
        Funkcja pozwala określić, którzy klienci wygenerowali największą
        wartość sprzedaży w sklepie internetowym.

    Wykorzystywane tabele:
        - ``klienci``
        - ``zamowienia``
        - ``pozycje_zamowienia``

    Zastosowane elementy SQL:
        - złączenia ``JOIN``
        - funkcja agregująca ``COUNT()``
        - funkcja agregująca ``SUM()``
        - ``GROUP BY``
        - ``ORDER BY``

    Dane wejściowe:
        Funkcja nie przyjmuje parametrów. Korzysta z istniejącego połączenia
        ``dbEngine`` do bazy PostgreSQL.

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
        k.id_klienta,
        k.imie,
        k.nazwisko,
        k.email,
        COUNT(DISTINCT z.id_zamowienia) AS liczba_zamowien,
        COALESCE(SUM(pz.ilosc * pz.cena_historyczna), 0) AS wartosc_zamowien
    FROM klienci k
    JOIN zamowienia z
        ON k.id_klienta = z.id_klienta
    JOIN pozycje_zamowienia pz
        ON z.id_zamowienia = pz.id_zamowienia
    GROUP BY
        k.id_klienta,
        k.imie,
        k.nazwisko,
        k.email
    ORDER BY
        wartosc_zamowien DESC,
        k.id_klienta ASC;
    """

    return wykonaj_zapytanie_postgres(polecenie)


# ============================================================
# 2. Sprzedaż według kategorii
# ============================================================

def sprzedaz_wedlug_kategorii_postgres():
    """
    Przedstawia sprzedaż produktów z podziałem na kategorie.

    Cel funkcji:
        Funkcja służy do sprawdzenia, które kategorie produktów generują
        największą sprzedaż w sklepie internetowym.

    Wykorzystywane tabele:
        - ``kategorie``
        - ``produkty``
        - ``pozycje_zamowienia``

    Zastosowane elementy SQL:
        - złączenia ``JOIN``
        - funkcje agregujące ``COUNT()`` i ``SUM()``
        - ``GROUP BY``
        - ``ORDER BY``

    Dane wejściowe:
        Funkcja nie przyjmuje parametrów. Korzysta z istniejącego połączenia
        ``dbEngine`` do bazy PostgreSQL.

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
        kat.id_kategorii,
        kat.nazwa_kategorii,
        COUNT(DISTINCT p.id_produktu) AS liczba_produktow,
        COALESCE(SUM(pz.ilosc), 0) AS liczba_sprzedanych_sztuk,
        COALESCE(SUM(pz.ilosc * pz.cena_historyczna), 0) AS wartosc_sprzedazy
    FROM kategorie kat
    JOIN produkty p
        ON kat.id_kategorii = p.id_kategorii
    JOIN pozycje_zamowienia pz
        ON p.id_produktu = pz.id_produktu
    GROUP BY
        kat.id_kategorii,
        kat.nazwa_kategorii
    ORDER BY
        wartosc_sprzedazy DESC,
        kat.id_kategorii ASC;
    """

    return wykonaj_zapytanie_postgres(polecenie)


# ============================================================
# 3. Pełny widok zamówień
# ============================================================

def pelne_zamowienia_postgres():
    """
    Wyświetla pełny widok zamówień z danymi klienta, produktu, płatności i wysyłki.

    Cel funkcji:
        Funkcja pozwala przeanalizować kompletne informacje o zamówieniach
        znajdujących się w bazie sklepu internetowego.

    Wykorzystywane tabele:
        - ``zamowienia``
        - ``klienci``
        - ``pozycje_zamowienia``
        - ``produkty``
        - ``platnosci``
        - ``wysylki``

    Zastosowane elementy SQL:
        - ``JOIN``
        - ``LEFT JOIN``
        - wyrażenie obliczeniowe ``ilosc * cena_historyczna``
        - ``ORDER BY``

    Dane wejściowe:
        Funkcja nie przyjmuje parametrów. Korzysta z istniejącego połączenia
        ``dbEngine`` do bazy PostgreSQL.

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
        z.id_zamowienia,
        z.data_zamowienia,
        z.status_zamowienia,
        k.id_klienta,
        k.imie,
        k.nazwisko,
        k.email,
        p.id_produktu,
        p.nazwa AS produkt,
        pz.ilosc,
        pz.cena_historyczna,
        pz.ilosc * pz.cena_historyczna AS wartosc_pozycji,
        pl.metoda_platnosci,
        pl.status_platnosci,
        w.firma_kurierska,
        w.numer_listu,
        w.status_paczki
    FROM zamowienia z
    JOIN klienci k
        ON z.id_klienta = k.id_klienta
    LEFT JOIN pozycje_zamowienia pz
        ON z.id_zamowienia = pz.id_zamowienia
    LEFT JOIN produkty p
        ON pz.id_produktu = p.id_produktu
    LEFT JOIN platnosci pl
        ON z.id_zamowienia = pl.id_zamowienia
    LEFT JOIN wysylki w
        ON z.id_zamowienia = w.id_zamowienia
    ORDER BY
        z.id_zamowienia ASC,
        p.id_produktu ASC;
    """

    return wykonaj_zapytanie_postgres(polecenie)


# ============================================================
# 4. Najlepiej oceniane produkty
# ============================================================

def najlepiej_oceniane_produkty_postgres():
    """
    Wyświetla najlepiej oceniane produkty wraz z kategorią i producentem.

    Cel funkcji:
        Funkcja pozwala sprawdzić, które produkty uzyskały najwyższe oceny
        wystawione przez klientów.

    Wykorzystywane tabele:
        - ``produkty``
        - ``kategorie``
        - ``producenci``
        - ``opinie``

    Zastosowane elementy SQL:
        - złączenia ``JOIN``
        - funkcja agregująca ``AVG()``
        - funkcja agregująca ``COUNT()``
        - ``GROUP BY``
        - ``ORDER BY``

    Dane wejściowe:
        Funkcja nie przyjmuje parametrów. Korzysta z istniejącego połączenia
        ``dbEngine`` do bazy PostgreSQL.

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
        p.id_produktu,
        p.nazwa AS produkt,
        kat.nazwa_kategorii,
        pr.nazwa_producenta,
        ROUND(AVG(o.ocena), 2) AS srednia_ocena,
        COUNT(o.id_opinii) AS liczba_opinii
    FROM produkty p
    JOIN kategorie kat
        ON p.id_kategorii = kat.id_kategorii
    JOIN producenci pr
        ON p.id_producenta = pr.id_producenta
    JOIN opinie o
        ON p.id_produktu = o.id_produktu
    GROUP BY
        p.id_produktu,
        p.nazwa,
        kat.nazwa_kategorii,
        pr.nazwa_producenta
    ORDER BY
        srednia_ocena DESC,
        liczba_opinii DESC,
        p.id_produktu ASC;
    """

    return wykonaj_zapytanie_postgres(polecenie)


# ============================================================
# 5. Produkty droższe od średniej ceny w swojej kategorii
# ============================================================

def produkty_drozsze_od_sredniej_postgres():
    """
    Wyszukuje produkty droższe od średniej ceny produktów w tej samej kategorii.

    Cel funkcji:
        Funkcja pozwala wskazać produkty, których aktualna cena jest wyższa niż
        przeciętna cena produktów należących do tej samej kategorii.

    Wykorzystywane tabele:
        - ``produkty``
        - ``kategorie``

    Zastosowane elementy SQL:
        - złączenie ``JOIN``
        - podzapytanie skorelowane
        - funkcja agregująca ``AVG()``
        - ``WHERE``
        - ``ORDER BY``

    Dane wejściowe:
        Funkcja nie przyjmuje parametrów. Korzysta z istniejącego połączenia
        ``dbEngine`` do bazy PostgreSQL.

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
        p.id_produktu,
        p.nazwa AS produkt,
        kat.nazwa_kategorii,
        p.cena_aktualna,
        ROUND((
            SELECT AVG(p2.cena_aktualna)
            FROM produkty p2
            WHERE p2.id_kategorii = p.id_kategorii
        ), 2) AS srednia_cena_w_kategorii
    FROM produkty p
    JOIN kategorie kat
        ON p.id_kategorii = kat.id_kategorii
    WHERE p.cena_aktualna > (
        SELECT AVG(p2.cena_aktualna)
        FROM produkty p2
        WHERE p2.id_kategorii = p.id_kategorii
    )
    ORDER BY
        kat.nazwa_kategorii ASC,
        p.cena_aktualna DESC,
        p.id_produktu ASC;
    """

    return wykonaj_zapytanie_postgres(polecenie)


__all__ = [
    "wykonaj_zapytanie_postgres",
    "ranking_klientow_postgres",
    "sprzedaz_wedlug_kategorii_postgres",
    "pelne_zamowienia_postgres",
    "najlepiej_oceniane_produkty_postgres",
    "produkty_drozsze_od_sredniej_postgres",
]
