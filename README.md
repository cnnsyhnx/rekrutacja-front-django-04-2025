# Menedżer Wydarzeń Uniwersytetu w Siedlcach

## 📌 O projekcie

**Menedżer Wydarzeń UWS** to aplikacja internetowa stworzona dla Uniwersytetu w Siedlcach, umożliwiająca organizację, zarządzanie i promocję wydarzeń uczelnianych. Aplikacja została zaprojektowana z myślą o łatwości użytkowania, dostępności oraz zgodności z wytycznymi identyfikacji wizualnej UWS.

## ✨ Funkcjonalności

- 🔍 **Przeglądanie wydarzeń** – lista nadchodzących wydarzeń na stronie głównej  
- 📄 **Szczegóły wydarzeń** – pełne informacje o każdym wydarzeniu  
- 🗓️ **Widok miesięczny** – kalendarz z zaplanowanymi wydarzeniami  
- ➕ **Tworzenie wydarzeń** – formularz do dodawania nowych wydarzeń  
- ✏️ **Edycja wydarzeń** – możliwość aktualizacji informacji o wydarzeniach  
- 🗑️ **Usuwanie wydarzeń** – możliwość usunięcia własnych wydarzeń  
- 👤 **Rejestracja i logowanie użytkowników** – każdy użytkownik może utworzyć konto i się zalogować  
- 📂 **Profil użytkownika** – panel użytkownika z przeglądem nadchodzących oraz przeszłych wydarzeń, w których bierze udział  
- ⚙️ **Zarządzanie własnymi wydarzeniami** – możliwość edycji i usunięcia wydarzeń utworzonych przez siebie  
- 🇵🇱 **Polskie tłumaczenie** – pełne wsparcie dla języka polskiego  
- 📱 **Responsywny design** – dostosowanie do urządzeń mobilnych i desktopowych  

## 🧰 Technologie

- Django 5.2  
- Bootstrap 5.3  
- JavaScript  
- HTML5 / CSS3  
- SQLite (baza danych)  
- Wsparcie dla i18n (internacjonalizacji)  

## ⚙️ Instalacja

```bash
git clone https://github.com/cnnsyhnx/rekrutacja-front-django-04-2025.git
cd rekrutacja-front-django-04-2025
```

```bash
pip install -r requirements.txt
```

```bash
python manage.py migrate
```

```bash
python manage.py runserver
```

Otwórz przeglądarkę i przejdź do:  
`http://127.0.0.1:8000/`

## 📁 Struktura projektu

- `event_manager/` – Główny projekt Django  
- `events/` – Aplikacja Django zarządzająca wydarzeniami  
- `users/` – Aplikacja Django odpowiedzialna za profile użytkowników  
- `templates/` – Szablony HTML  
- `static/` – Pliki statyczne (CSS, JavaScript, obrazy)  
- `locale/` – Pliki tłumaczeń  

## 🖼️ Zrzuty ekranu

### 🏠 Strona główna
![Strona główna](./screenshots/home.png)  
*Strona główna z listą wydarzeń*

### 📅 Widok zaplanowanych zdarzeń
![Zaplanowane wydarzenia](./screenshots/scheduled_events_view.png)  
*Umożliwia wyświetlanie zaplanowanych wydarzeń na ekranie głównym.*

### 🗓️ Widok miesięczny
![Widok miesięczny](./screenshots/monthly_view.png)  
*Kalendarz z widokiem miesięcznym*

### 📃 Widok listy wydarzeń
![Lista wydarzeń](./screenshots/list_view.png)  
*Umożliwia wyświetlanie zdarzeń w formacie listy*

### ℹ️ Szczegóły wydarzenia
![Szczegóły wydarzenia](./screenshots/event_detail.png)  
*Strona ze szczegółami wydarzenia*

### 📝 Formularz wydarzenia
![Formularz wydarzenia](./screenshots/event_form.png)  
*Formularz do tworzenia/edycji wydarzeń*

### 🗓️ Lista bieżącego miesiąca
![Widok bieżącego miesiąca](./screenshots/current_month_list_view.png)  
*Umożliwia wyświetlanie wydarzeń z bieżącego miesiąca*

### 👤 Profil użytkownika
![Profil użytkownika](./screenshots/profile_view.png)  
*Panel profilu umożliwia użytkownikowi przeglądanie swoich przyszłych i minionych wydarzeń, a także zarządzanie nimi (edycja, usuwanie).*

## 👥 Autorzy

Projekt został opracowany dla Uniwersytetu w Siedlcach przez [Jan](mailto:cnnsyhnx@gmail.com).

## 📄 Licencja

© 2025 Uniwersytet w Siedlcach. Wszelkie prawa zastrzeżone.