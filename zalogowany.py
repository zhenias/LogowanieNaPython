import tkinter as tk
import requests
import http.cookiejar

cookie_jar = http.cookiejar.CookieJar()
api = "https://api-dziennik.dziennik-szkola.ct8.pl/getMe"

def wylogujSie():
    o.destroy()

def getMe(access_token_cookie):

    if access_token_cookie is None:
        return "KUR**, TOKEN POTRZEBUJE!!!"

    datas = {
        'access_token': access_token_cookie
    }

    r = requests.post(api, json = datas)

    if r.status_code == 200:
        print("==============================================")
        print(f"udało sięę zalogować :>) wkońcu, status_code: %s" % r.status_code)
        print("==============================================")
        return r.json()
    else:
        print("Wystąpił błąd, kod statusu: ", r.status_code)
        print("===================================")
        print(f"Wystąpił błąd: {r}")
        print("===================================")

def oknoPowitalne(popupStare, json):
    global o
    o = tk.Tk()
    if popupStare:
        popupStare.destroy()

    access_token = None
    access_token = json['message']['access_token']

    print(f"access_token: {access_token}")

    me = getMe(access_token)

    print(f"Twoje dane z API: %s" % me)

    me = me['message'];

    o.title("Zalogowano")
    o.geometry("500x500")

    lbl = tk.Label(o, text = f"Status autoryzacji, kod: {json['status']} \n "
                             f"Imię: {me['user_name']} \n "
                             f"Nazwisko: {me['user_lastname']} \n "
                             f"Czy jesteś pracownikiem (1 = tak, 0 = nie): {me['is_pracownik']} \n"
                             f"Alias: {me['alias']} \n"
                             f"UserId: {me['user_id']} \n"
                             f"Display name: {me['display_name']} \n"
                             f"Szczęśliwy numerek w twojej szkole: {me['szczesliwy_numerek']} \n"
                             f"Czy masz włączone 2FA: {me['is_2fa']} \n"
                             f"Login: {me['login']} \n")
    lbl.pack()

    wyloguj = tk.Button(o, text = "Zamknij okno", command=wylogujSie)
    wyloguj.pack(pady=10)

    o.mainloop()