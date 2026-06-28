===========================
Wprowadzenie
===========================

:Autor:
    Adam Tarkowski

Niniejszy rozdział stanowi indywidualne wprowadzenie do sprawozdania z kursu
baz danych, realizowanego w semestrze letnim roku akademickiego 2025/2026.

Wprowadzenie tematyczne
=======================

Raport dokumentuje pełny cykl pracy z relacyjną bazą danych: od zagadnień
związanych z utrzymaniem infrastruktury, przez analizę wymagań i projektowanie
struktury danych, aż po implementację, zasilenie bazy danymi i wykonywanie
zapytań. Część literaturowa przybliża praktyczne aspekty eksploatacji
PostgreSQL — dobór sprzętu, konfigurację serwera, kontrolę i konserwację,
monitorowanie, diagnostykę, partycjonowanie, bezpieczeństwo, tworzenie kopii
zapasowych oraz zagadnienia wydajności, skalowania i replikacji.

Część projektowa opiera się na przykładzie systemu zarządzania sprzedażą
w sklepie internetowym. Przeanalizowano procesy związane z obsługą klientów,
produktów, producentów, kategorii, kodów rabatowych, zamówień, płatności,
wysyłek i opinii. Na tej podstawie powstały: model konceptualny, model logiczny
w trzeciej postaci normalnej oraz dwa modele fizyczne — dostosowane odpowiednio
do PostgreSQL i SQLite. Szczególną uwagę poświęcono prawidłowemu odwzorowaniu
zależności między danymi, zachowaniu historii cen produktów w zamówieniach
oraz właściwemu zastosowaniu kluczy i więzów integralności.

Kolejna część raportu przedstawia implementację schematów w obu systemach
zarządzania bazą danych, a także wsadowe wprowadzanie danych z pliku CSV
przy użyciu skryptów w języku Python. Opisano tam walidację danych, weryfikację
istnienia rekordów powiązanych, wymaganą kolejność operacji oraz obsługę
transakcji i błędów. W celu sprawdzenia poprawności działania baz przygotowano
zapytania wykorzystujące złączenia, agregacje, grupowanie, sortowanie
i podzapytania — oddzielnie dla PostgreSQL i SQLite — co pozwala na
bezpośrednie porównanie zachowania obu silników na identycznym modelu danych.

Wnioski z ćwiczeń i eksperymentów
=================================

Przeprowadzone ćwiczenia potwierdziły, że jakość bazy danych zależy przede
wszystkim od rzetelnego rozpoznania procesów biznesowych i zależności między
danymi. Pominięcie kontekstu transakcji lub błędne odwzorowanie relacji
wiele-do-wielu skutkowałoby utratą kluczowych informacji. Problem ten
rozwiązano w projekcie przez wprowadzenie tabeli ``Pozycje_Zamowienia``,
która wiąże zamówienia z produktami, przechowując jednocześnie liczbę sztuk
i historyczną cenę zakupu.

Normalizacja do trzeciej postaci normalnej skutecznie ograniczyła powielanie
danych i ryzyko anomalii przy operacjach wstawiania, modyfikowania i usuwania
rekordów. Okazało się jednak, że czytelniejsza struktura tabel pociąga za sobą
konieczność łączenia wielu relacji przy odtwarzaniu pełnego obrazu sprzedaży.
Przygotowane zapytania dowodzą, że wypracowany model umożliwia zarówno
szczegółowy wgląd w historię zamówień, jak i przekrojowe analizy — tworzenie
rankingów klientów, zestawień sprzedaży według kategorii czy porównań ocen
produktów. Wszystkie wartości sprzedaży są wyliczane wyłącznie dla zakończonych
płatności, z pominięciem zamówień anulowanych i z uwzględnieniem historycznego
rabatu.

Przeniesienie tego samego modelu logicznego na PostgreSQL i SQLite wykazało,
że migracja między silnikami jest możliwa, lecz wymaga dostosowania typów
danych, mechanizmów generowania identyfikatorów i pewnych elementów składni.
PostgreSQL dysponuje precyzyjniejszymi typami — takimi jak ``NUMERIC`` czy
``TIMESTAMP`` — podczas gdy SQLite opiera się na prostszym systemie klas
przechowywania. Mimo tych różnic oba systemy egzekwują ten sam zestaw reguł
integralności, a odpowiadające sobie zapytania dają porównywalne wyniki.

Eksperymenty z importem danych uwypukliły znaczenie walidacji wejściowej,
więzów integralności i transakcji. Rekordy muszą być wstawiane w kolejności
wynikającej z zależności między tabelami, a błąd pojedynczej pozycji nie może
pozostawiać niekompletnego zamówienia w bazie. Wiersze należące do jednego
zamówienia są przetwarzane w ramach tej samej transakcji, dzięki czemu
niepowodzenie dowolnego kroku powoduje wycofanie całości. Takie podejście
zapewnia spójność danych nawet przy automatycznym zasilaniu bazy dużą liczbą
rekordów.

Całość wykonanych prac pokazała, że poprawne zaprojektowanie tabel to dopiero
punkt wyjścia, a nie koniec zagadnienia. W środowisku produkcyjnym równie
istotne okazują się konfiguracja serwera, bieżące monitorowanie, dbałość o
bezpieczeństwo, regularne kopie zapasowe i świadome planowanie wydajności.
Projektowanie, implementacja, testowanie zapytań oraz administracja składają
się na jeden spójny proces, którego celem jest system niezawodny, bezpieczny
i gotowy na dalszy rozwój.


Spis wszystkich użytych w raporcie repozytoriów
================================================

Repozytoria tematyczne
-----------------------

* `Sprzęt dla bazy danych <https://github.com/karaskamil/Sprzet-dla-bazy-danych.git>`_
* `Konfiguracja bazy danych PostgreSQL <https://github.com/Youarecheck/Bazy_Danych_Tematyczne_Repo_MK.git>`_
* `Kontrola i konserwacja bazy danych <https://github.com/pawlos1337/Bazy-danych-temat.git>`_
* `Monitorowanie i diagnostyka <https://github.com/OskarProgrammer/monitorowanie_i_diagnostyka.git>`_
* `Wydajność, skalowanie i replikacja danych <https://github.com/KMachoK/Tematyczne.git>`_
* `Partycjonowanie danych <https://github.com/domino0472/Partycjonowani-Danych.git>`_
* `Bezpieczeństwo baz danych <https://github.com/oski486/BazyDanych-Subject.git>`_
* `Kopie zapasowe i odzyskiwanie danych <https://github.com/Koko9077/Kopie-zapasowe-i-odzyskiwanie-danych.git>`_

Modele
------

* `Model konceptualny, logiczny i fizyczny <https://github.com/OskarProgrammer/model-konceptualny-logiczny-fizyczny.git>`_

Implementacja
-------------

* `Implementacja bazy danych <https://github.com/OskarProgrammer/implementacja-bazy-danych.git>`_

Repozytorium główne
--------------------

* `Repozytorium główne <https://github.com/OskarProgrammer/bazy_danych_glowne_3.git>`_
