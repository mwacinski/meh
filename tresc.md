Utwórz prosty panel logowania i rejestracji ze zintegrowaną bazą danych przy użyciu
SQLAlchemy. Po zalogowaniu do panelu ma wyświetlać się komunikat: Hello,
<Twoja nazwa użytkownika>. You're with us for <ilość minionych dni od rejestracji> days.

2.   Utwórz program w Pythonie wyświetlający następujące opcje (w formie menu):
Dodaj notatkę
Usuń notatkę
Wyświetl wszystkie notatki
Edytuj notatkę


Po wybraniu odpowiedniej opcji i uzupełnieniu potrzebnych informacji,
program ma wysyłać odpowiednio spreparowany request HTTP do Flaskowego API
i modyfikować bazę danych. Dla uproszczenia zakładamy, że połączenie z API
nie wymaga żadnego uwierzytelnienia.

3.
Stwórz widoki, które umożliwią Ci dodawanie dowolnych tytułów filmów do bazy
wraz z krótką opinią co do filmu, oddzielny widok na wyświetlanie dodanych
tytułów filmów, oraz widok na wyświetlanie "podsumowania" - tytuły filmów + opinie.
Zadbaj o poprawne zaprojektowanie modelów bazodanowych.

Podpowiedź
Może okazać się być konieczne zaimplementowanie relacji między tabelą filmów a opinii.
