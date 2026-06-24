# Zaspani Kawosze - aplikacja Django

Projekt aplikacji webowej dla siłowni, przeniesiony z wcześniejszej wersji konsolowej na Django.

## Zakres aplikacji

- zarządzanie klubowiczami,
- dodawanie, edycja i usuwanie klubowiczów,
- lista klubowiczów,
- cennik z danych zapisanych w bazie,
- grafik zajęć z danych zapisanych w bazie,
- strony FAQ, kontakt i strona główna,
- panel administratora Django,
- raport klubowiczów w formacie PDF,
- import danych startowych z plików JSON i CSV.

## Modele danych

W aplikacji `members` znajdują się modele:

- `GymMember` - klubowicze,
- `PriceItem` - pozycje cennika,
- `ScheduleEntry` - wpisy grafiku według godzin i dni tygodnia.

Domyślnie projekt korzysta z bazy SQLite.

## Instalacja

1. Utwórz i aktywuj środowisko wirtualne.
2. Zainstaluj zależności:

```powershell
pip install -r requirements.txt
```

3. Wykonaj migracje:

```powershell
python manage.py migrate
```

4. Zaimportuj dane startowe:

```powershell
python manage.py import_members
python manage.py import_price_list --clear
python manage.py import_schedule --clear
```

5. Uruchom serwer:

```powershell
python manage.py runserver
```

## Główne adresy

- `/` - strona główna,
- `/members/` - lista klubowiczów,
- `/members/add/` - dodawanie klubowicza,
- `/cennik/` - cennik,
- `/grafik/` - grafik,
- `/faq/` - FAQ,
- `/kontakt/` - kontakt,
- `/admin/` - panel administratora.

## Panel administratora

Modele `GymMember`, `PriceItem` i `ScheduleEntry` są zarejestrowane w panelu administratora.

Aby utworzyć konto administratora:

```powershell
python manage.py createsuperuser
```

Raport PDF można pobrać z listy klubowiczów w panelu admina:

1. zaznacz wybranych klubowiczów,
2. wybierz akcję `Pobierz raport wybranych klubowiczow (PDF)`,
3. kliknij `Wykonaj`.

## Formularz kontaktowy i e-mail

Formularz wysyła wiadomość do aktywnych superuserów, którzy mają uzupełniony adres e-mail. Jeśli taki adres nie istnieje, wiadomość jest wypisywana w konsoli serwera.

Do prawdziwej wysyłki SMTP ustaw zmienne środowiskowe:

```powershell
$env:EMAIL_HOST="smtp.example.com"
$env:EMAIL_PORT="587"
$env:EMAIL_HOST_USER="konto@example.com"
$env:EMAIL_HOST_PASSWORD="haslo-aplikacji"
$env:EMAIL_USE_TLS="true"
$env:DEFAULT_FROM_EMAIL="konto@example.com"
```

Bez `EMAIL_HOST` projekt używa bezpiecznego backendu konsolowego.

## Testy i sprawdzenie

Podstawowe sprawdzenie projektu:

```powershell
python manage.py check
```

Uruchomienie testów:

```powershell
python -m unittest discover -s tests
```

## Starsza wersja konsolowa

W repozytorium nadal znajdują się pliki wcześniejszej wersji konsolowej, m.in. `menu.py`, `funkcje.py`, `members_storage.py` i `user.py`. Obecna wersja webowa korzysta z Django, modeli i bazy danych.
