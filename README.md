# jpydzr10-zaspani-kawosze

Webowa aplikacja Django dla silowni **Zaspani Kawosze**.

Projekt zaczal sie jako aplikacja konsolowa, ale aktualny milestone dotyczy wersji webowej:

- interfejs webowy,
- konfiguracja bazy SQLite,
- wczytywanie danych z bazy,
- panel administratora,
- przeniesienie funkcji klubowiczow, cennika i grafiku do Django.

Stare pliki konsolowe nadal sa w repozytorium jako material historyczny, ale glownym punktem wejscia jest teraz `manage.py`.

## Stack

- Python
- Django
- SQLite
- HTML/CSS
- proste pliki CSV/JSON do importu danych

## Uruchomienie lokalne

1. Aktywuj lub utworz srodowisko wirtualne.

   Jesli masz juz `.venv`:

   ```bash
   source .venv/bin/activate
   ```

2. Zainstaluj zaleznosci:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Wykonaj migracje bazy:

   ```bash
   python manage.py migrate
   ```

4. Zaimportuj dane demo:

   ```bash
   python manage.py import_members
   python manage.py import_price_list --clear
   python manage.py import_schedule --clear
   ```

5. Uruchom aplikacje:

   ```bash
   python manage.py runserver
   ```

6. Otworz w przegladarce:

   ```txt
   http://127.0.0.1:8000/
   ```

## Konto demo administratora

Panel administratora jest dostepny pod adresem:

```txt
http://127.0.0.1:8000/admin/
```

Na potrzeby prezentacji mozna utworzyc konto demo:

```bash
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); user, created = User.objects.get_or_create(username='Zaspani', defaults={'is_staff': True, 'is_superuser': True}); user.is_staff = True; user.is_superuser = True; user.set_password('Kawosze'); user.save()"
```

Dane demo:

```txt
login: Zaspani
haslo: Kawosze
```

To konto sluzy tylko do lokalnego demo projektu.

## Co dziala

- Strona glowna aplikacji.
- Cennik pobierany z bazy danych.
- Aktywne i nieaktywne plany taryfowe.
- Wybor planu z prosta symulacja platnosci.
- Grafik zajec pobierany z bazy.
- FAQ z podstawowymi pytaniami i odpowiedziami.
- Formularz kontaktowy w trybie demo.
- Lista, dodawanie, edycja i usuwanie klubowiczow dla administratora.
- Panel administratora Django.

## Platnosci

Platnosci sa obecnie tylko symulacja.

Po kliknieciu `Wybierz plan` aplikacja pokazuje ekran potwierdzenia testowego. Nie ma integracji z prawdziwym operatorem platnosci i nie sa pobierane prawdziwe pieniadze.

## Dane

Pliki uzywane do importu:

- `members.json` - klubowicze,
- `cennik _zaspani_k.csv` - cennik,
- `grafik _zaspani_k.csv` - grafik.

## Testy

Uruchomienie testow:

```bash
python manage.py test
```

Sprawdzenie konfiguracji Django:

```bash
python manage.py check
```

## Co zostaje na kolejny milestone

- logowanie zdarzen,
- raporty o uzytkownikach,
- dodatkowa wersja jezykowa,
- pelne uwierzytelnianie uzytkownikow,
- prawdziwy mailing,
- prawdziwe platnosci.
