start = """Witaj, akustyku!
Jestem oficjalnym świątecznym botem, choć niektórzy wolą nazywać mnie SS-manem.
Nie spełnie każdego twojego życzenia - to zadanie dla Twojego Mikołaja
Moim jest jedynie połączyć Cię z nim ( ͡° ͜ʖ ͡°)

Blabla, komendy:
/help - wyświetla tę wiadomość

/register - potwierdza Twoją chęć do uczestniczenia w SS
/unregister - anuluje Twoją chęć do uczestniczenia w SS
/status - zwraca Twój obecny status zapisu do SS
"""

insufficient_permissions = "Nie masz dostępu do tej komendy"
on_error = """Coś, coś się zepsuło i nie było mnie słychać
Skontaktuj się z administratorę"""

password_request = "Gib passy plox"
wrong_password = "Nie udało się Cię zarejestrować :<"
cancel = "To elo"

successful_registration = "Zarejestrowano pomyślnie, towarzyszu {}"
already_registered = "Towarzysz {} był już w bazie"
unregistered_message = "Nie będziesz brał już udziału w SS"

user_registered = "Bierzesz udział w SS"
not_registered = "I tak nie brałeś udziału w SS"
user_not_registered = "Nie bierzesz udziału w SS"

ss_started = """AKUSTYKU
Z dniem dzisiejszym Secret Santa Anno Domini 2019
In Habemus Papam uznaje się za rozpoczęte!

Tobie przypadł zaszczyt obdarowania prezentem {}a.
"""
ss_help = """
Nowe komendy to:
/ask - Forwarduje wiadomość do Twojego prezentowanego.
/reply - Odpowiada na pytanie Twojego SS-Mana
(innymi słowy wysyła jemu wiadomość).

Daily reminder
Wysyłając pytanie/odpowiedź nie zdradzić swojej tożsamości!
"""

message_request = "_Pisz, albo /cancel_"
got_message = "_Masz 1 (słownie: jedną) nową wiadomość od {}:_"
message_send = "_Wiadomość wysłana :)_"
message_failed = "_Wiadomość niewysłana :(_\n_Poskarż się adminowi_"


def who_to_alias(to_who):
    return {
            'giver_chat_id': 'osoby która Ci daje prezent, '
                             'użyj /reply, aby odpowiedzieć',
            'taker_chat_id': 'osoby której dajesz prezent, '
                             'użyj /ask, aby odpowiedzieć'
    }[to_who]
