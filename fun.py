import tkinter as tk
import requests
import http.cookiejar
import zalogowany

def zamknijOkno():
    o.destroy()

cookie_jar = http.cookiejar.CookieJar()
api = "https://api-dziennik.dziennik-szkola.ct8.pl/token"

def wylogujSie():
    nowe_okno("Zaloguj się", "Zaloguj się")

def authorization_code(code):
    print("zaczynam funkcje authorization_code")

    data = {
        'grant_type': 'authorization_code',
        'code': code
    }

    print("to ja ale przed zapytaniem do: ", api)

    res = requests.post(api, json = data)

    if res.status_code == 200:
        print("udalo sie zalogowac mordko: ", res.text)

        # Zapisz ciasteczka uzyskane z odpowiedzi HTTP do pliku
        with open('cookies.txt', 'w') as cookies_file:
            cookies_file.write("%s" % res.json())  # Zapisz ciasteczka do pliku

        zalogowany.oknoPowitalne(o, res.json())

    else:
        print("nie udalo sie zalogowac, blad: ", res.status_code)


def zapytanieDoDziennika(login, haslo):
    print("Zaczyna inicjazje logowania")

    data = {
        'grant_type': 'password',
        'login': login,
        'password': haslo
    }

    print("To znowu ja, inicjuje już przed requests.post")
    response = requests.post(api, json=data)

    print("jestem już po requests.post")

    if response.status_code == 200:
        print("======================================================")

        json_data = response.json()

        if 'code' in json_data['message']:
            authorization_code(json_data['message']['code'])
            return 0
        elif 'token' in json_data['message']:
            return ("Chyba twoje konto wymaga 2FA autoryzacji. \n"
                    "Aplikacja nie obsługuje 2FA.");
            return 0
        else:
            print("========================")
            print("Wystąpił błąd podczas oznalezienie code, ciąg znaków z json %s" % json_data)
            print("========================")
            return 0

    else:
        print("LAMUS hahahah")
        print("Błąd autoryzacji: %s" % response.status_code);

def pokaz_wpisane_dane():
    wpisane_dane = login.get()
    etykieta_wyniku.config(text="Login: " + wpisane_dane)

def autoryzujSie():
    l = login.get()
    h = haslo.get()
    zapytanieDoDziennika(l, h)

def nowe_okno(nazwa, tekst):
    global login, etykieta_wyniku, haslo, o

    o = tk.Tk()
    o.title(nazwa)

    e = tk.Label(o, text = tekst)
    e.pack(pady=20)

    login = tk.Entry(o, width=20, font=("Arial", 12))
    login.pack(pady=2)

    haslo = tk.Entry(o, width=20, font=("Arial", 12), show = "*")
    haslo.pack(pady=2)

    # Przycisk do pokazania wprowadzonych danych
    przycisk = tk.Button(o, text="Zamknij", command=o.destroy)
    przycisk.pack()

    # Przycisk do pokazania wprowadzonych danych
    przycisk2 = tk.Button(o, text="Autoryzuj się", command=autoryzujSie)
    przycisk2.pack()

    # Etykieta wyniku
    etykieta_wyniku = tk.Label(o, text="", font=("Arial", 12))
    etykieta_wyniku.pack(pady=10)

    o.geometry("300x300")

    o.mainloop()

