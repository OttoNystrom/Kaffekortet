import csv
import random
import qrcode
import os


def draw_line():
    """ritar en linje"""

    print(50 * "-")


def clear_screen():
    """Tömmer skärmen och skriver ut rubriken"""

    os.system("cls")
    draw_line()
    print("Välkommen till Kaffekortet!\n")
    draw_line()


def is_it_int(question):
    """Checkar ifall svaret på en fråga är en interger och skickar tillbaka värdet ifall det är det.
    Annars ställs frågan om tills svaret är en integrer"""

    while True:
        try:
            value = int(input(question))
            return value
        except ValueError:
            print("Vänligen skriv in en siffra\n")


def yes_or_no(question):
    """Ställer en fråga och ger inte sig förrens svaret är varken ja eller nej"""

    print("\n")
    while True:
        answer = input(question).casefold()

        if answer == "ja":
            return "ja"

        if answer == "nej":
            break
        else:
            print("Du kan bara svara ja eller nej, försök igen.\n")


def print_csv_file(what_to_read):
    """Skriver ut alla värden under den rubriken du anger"""

    with open("database.csv", "r") as csv_file_database:
        reader_for_csv_file = csv.DictReader(csv_file_database)

        for line_in_csv_file in reader_for_csv_file:
            print(line_in_csv_file["name"], "---", line_in_csv_file[what_to_read])


def delete_user_in_csv_file(user_to_be_deleted, back_to_user):
    """Tar bort en användare i databasen"""

    file = open("database.csv", "r")
    Reader = csv.reader(file)
    L = []
    found = False
    for row in Reader:
        if row[0] == user_to_be_deleted:
            found = True
        else:
            L.append(row)
    file.close()

    if found:
        file = open("database.csv", "w+", newline="")
        Writer = csv.writer(file)
        Writer.writerows(L)
        file.seek(0)
        file.close()

    else:
        print("Användaren hittades inte")

    os.remove("C:\Qr_codes\{}.jpeg".format(user_to_be_deleted))

    if back_to_user == "admin":
        back_to_main_menu_admin()
    else:
        start_menu_main()


def update_user_data(heading_to_update, old_value, new_value):
    """Uppdaterar ett visst värde för en viss användare"""

    file = open("database.csv", "r")
    reader = csv.reader(file)
    new_value_list = []
    i = 0
    found = False

    if heading_to_update == "code":
        i = 0
    if heading_to_update == "email":
        i = 1
    if heading_to_update == "password":
        i = 2
    if heading_to_update == "name":
        i = 3
    if heading_to_update == "value":
        i = 4

    for row in reader:
        if row[i] == old_value:
            found = True
            row[i] = new_value
        new_value_list.append(row)
    file.close()

    if found:
        file = open("database.csv", "w+", newline="")
        writer = csv.writer(file)
        writer.writerows(new_value_list)
        file.seek(0)
        file.close()
    else:
        print("Användaren hittades inte")


def check_if_already_in_file(data_to_check):
    """Checkar ifall datan redan finns i filen"""

    with open("database.csv", "r") as csv_file_database:
        reader_for_csv_file = csv.DictReader(csv_file_database)
        for line_in_csv_file in reader_for_csv_file:
            header = ["code", "email", "password", "name", "value"]
            for i in range(len(header) - 1):
                if header[i] == "password":
                    continue
                if data_to_check[0][i] == line_in_csv_file[header[i]]:
                    return "already in file"
        else:
            return "not in file"


def add_account():
    """Adderar ett konto till databasen. Ifall kontot redan finns så läggs det inte till"""

    clear_screen()
    print("* För att komma tillbaka skriver du bara: tillbaka. *\n ")
    name_to_add = input("Namn: ")
    if name_to_add.lower() == "tillbaka":
        return
    else:
        clear_screen()
        print("* För att komma tillbaka skriver du bara: tillbaka. *\n ")
        email_to_add = input("Email: ")
    if email_to_add.lower() == "tillbaka":
        return
    else:
        clear_screen()
        print("* För att komma tillbaka skriver du bara: tillbaka. *\n ")
        password_to_add = input("Lösenord: ")
    if password_to_add.lower() == "tillbaka":
        return
    code_to_add = generate_qr_code()
    total_data_to_add = [code_to_add, email_to_add, password_to_add, name_to_add, "0"]
    if check_if_already_in_file([total_data_to_add]) == "not in file":
        file = open("database.csv", "a", newline="")
        writer = csv.writer(file)
        writer.writerows([total_data_to_add])
        file.close()
        return
    else:
        clear_screen()
        if yes_or_no("Användaren finns redan, vill du försöka igen? ") == "ja":
            add_account()
        else:
            return


def change_password(username):
    """Ändra ett lösenord hos användaren"""

    clear_screen()
    with open("database.csv", "r") as csv_file_database:
        reader_for_csv_file = csv.DictReader(csv_file_database)
        for line_in_csv_file in reader_for_csv_file:
            if username == line_in_csv_file["email"]:
                print("* För att komma tillbaka skriver du bara: tillbaka. *\n ")
                old_password = input("Gammalt lösenord: ")
                if old_password == "tillbaka":
                    start_menu_user(username)
                if str(old_password) == line_in_csv_file["password"]:
                    clear_screen()
                    print("* För att komma tillbaka skriver du bara: tillbaka. *\n ")
                    new_password = input("Ditt nya lösenord: ")
                    if new_password == "tillbaka":
                        start_menu_user(username)
                    verify_password = ""
                    while verify_password != new_password:
                        clear_screen()
                        print("* För att komma tillbaka skriver du bara: tillbaka. *\n ")
                        verify_password = input("Verifiera ditt nya lösenord genom att skriva det igen: ")
                        if verify_password == "tillbaka":
                            start_menu_user(username)
                    update_user_data("password", str(old_password), str(new_password))
                    return
                else:
                    clear_screen()
                    print("Fel lösenord.\n")
                    if yes_or_no("Vill du försöka igen? ") == "ja":
                        change_password(username)
                    else:
                        start_menu_user(username)


def change_qr_code():
    """Du kan ändra QR-koden för ett konto genom att mata in den gammla samt en ny kod."""

    clear_screen()
    print("* För att komma tillbaka skriver du bara: tillbaka. *\n ")
    old_qr_code = input("Gammla qr-koden: ")
    if old_qr_code.lower() == "tillbaka":
        back_to_main_menu_admin()
    if check_if_already_in_file([[old_qr_code, "email", "password", "name", "value"]]) == "already in file":
        with open("database.csv", "r") as csv_file_database:
            reader_for_csv_file = csv.DictReader(csv_file_database)
            for line_in_csv_file in reader_for_csv_file:
                if old_qr_code == line_in_csv_file["code"]:
                    clear_screen()
                    if yes_or_no("Är du säker på att du vill ändra QR-koden för {}? ".format(
                            line_in_csv_file["name"])) == "ja":
                        update_user_data(line_in_csv_file["email"], line_in_csv_file["code"], generate_qr_code())
                        os.remove("C:\Qr_codes\{}.jpeg".format(old_qr_code))
                        start_menu_admin()
                    else:
                        back_to_main_menu_admin()
    else:
        print("Qr-koden finns inte i systemet.")
        if yes_or_no("Vill du försöka igen? ") == "ja":
            change_qr_code()
        else:
            start_menu_admin()


def update_all_qr_codes():
    """Uppdaterar alla qr-koder i databasen samt jpeg bilderna"""

    with open("database.csv", "r") as csv_file_database:
        reader_for_csv_file = csv.DictReader(csv_file_database)

        for line_in_csv_file in reader_for_csv_file:
            if line_in_csv_file["code"] == "code":
                continue
            else:
                old_qr_code = line_in_csv_file["code"]
                update_user_data(line_in_csv_file["email"], line_in_csv_file["code"], generate_qr_code())
                try:
                    os.remove("C:\Qr_codes\{}.jpeg".format(old_qr_code))
                except FileNotFoundError:
                    continue


def generate_qr_code():
    """Skapar en unik QR-kod för varje user."""

    qr_code = []
    for i in range(0, 10):
        qr_code.append(str(random.randrange(0, 10)))
    data = "".join(map(str, qr_code))
    if check_if_already_in_file([[data, "email", "password", "name", "value"]]) == "already in file":
        generate_qr_code()

    qr = qrcode.QRCode(version=1,
                       box_size=10,
                       border=5)

    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='orange',
                        back_color='white')

    file_name = "C:\Qr_codes\{}.jpeg".format(data)
    img.save(file_name)

    return data


def start_menu_main():
    """Den första menyn du möts av."""

    clear_screen()
    print("[1] Logga in")
    print("[2] Skapa ett konto")
    choice = is_it_int("Välj en meny: ")
    while 0 < choice < 3:
        if choice == 1:
            inlogg_username()
        if choice == 2:
            add_account()
            start_menu_main()
    else:
        start_menu_main()


def start_menu_admin():
    """Huvudmeny för admin"""

    clear_screen()
    print("[1] Skriv ut information\n"
          "[2] Lägg till konto\n"
          "[3] Ta bort konto\n"
          "[4] Ändra QR-kod\n"
          "[5] Checka ifall något finns i databasen\n"
          "[6] Uppdatera alla QR-koder\n"
          "[7] Logga ut\n\n")
    choice = is_it_int("Välj en meny: ")
    while 0 < choice < 8:
        if choice == 1:
            clear_screen()
            print(
                "Vad vill du skriva ut: "
                "\n[1] Alla koder"
                "\n[2] Alla email-adresser"
                "\n[3] Alla lösenord"
                "\n[4] Namn på alla i databasen"
                "\n[5] Alla olika värden på antalet kaffekoppar"
                "\n[6] Tillbaka till huvudmenyn\n\n")
            choice_1 = is_it_int("Välj något utifrån menyn: ")
            while 0 < choice_1 < 7:
                if choice_1 == 1:
                    clear_screen()
                    print("Alla QR-koder: ")
                    print_csv_file("code")
                    back_to_main_menu_admin()
                    break

                if choice_1 == 2:
                    clear_screen()
                    print("Alla email-adresser: ")
                    print_csv_file("email")
                    back_to_main_menu_admin()
                    break

                if choice_1 == 3:
                    clear_screen()
                    print("Alla lösenord: ")
                    print_csv_file("password")
                    back_to_main_menu_admin()
                    break

                if choice_1 == 4:
                    clear_screen()
                    print("Namn på alla i databasen: ")
                    print_csv_file("name")
                    back_to_main_menu_admin()
                    break

                if choice_1 == 5:
                    clear_screen()
                    print("Alla olika värden på antalet kaffekoppar: ")
                    print_csv_file("value")
                    back_to_main_menu_admin()
                    break

                if choice_1 == 6:
                    start_menu_admin()
        if choice == 2:
            clear_screen()
            add_account()
            back_to_main_menu_admin()
            break
        if choice == 3:
            clear_screen()
            user_to_be_deleted = input("QR-kod för användaren som ska tas bort: ")
            if yes_or_no("Är du säker? ") == "ja":
                delete_user_in_csv_file(user_to_be_deleted, "admin")
                print("Användaren är nu borttagen.")
            back_to_main_menu_admin()
            break
        if choice == 4:
            clear_screen()
            change_qr_code()
            break
        if choice == 5:
            clear_screen()
            name_to_check = input("Namn: ")
            email_to_check = input("Email: ")
            code_to_check = input("QR-kod: ")
            data_to_check = [code_to_check, email_to_check, "password", name_to_check, "value"]
            if check_if_already_in_file([data_to_check]) == "already in file":
                print("Finns i databasen")
            else:
                print("Finns inte i databasen")
            back_to_main_menu_admin()
            break
        if choice == 6:
            clear_screen()
            if yes_or_no("Är du säker på att du vill uppdatera alla qr_koder? ") == "ja":
                update_all_qr_codes()
            else:
                start_menu_admin()
            start_menu_admin()
            break
        if choice == 7:
            start_menu_main()
            break
        break
    else:
        start_menu_admin()


def start_menu_user(user):
    """Huvudmenyn för användaren"""
    clear_screen()
    print("[1] Visa QR-kod\n"
          "[2] Visa information\n"
          "[3] Byta QR-kod\n"
          "[4] Byta lösenord\n"
          "[5] Ta bort konto\n"
          "[6] Logga ut\n")
    choice = is_it_int("Välj från menyn ovan: ")
    while 0 < choice < 7:
        if choice == 1:
            clear_screen()
            print("Funktionen finns inte än... *Printa personlig QR-kod*")
            back_to_main_menu_user(user)
            break
        if choice == 2:
            user_menu_info(user)
            back_to_main_menu_user(user)
        if choice == 3:
            clear_screen()
            if yes_or_no("Är du säker? ") == "ja":
                with open("database.csv", "r") as csv_file_database:
                    reader_for_csv_file = csv.DictReader(csv_file_database)
                    for line_in_csv_file in reader_for_csv_file:
                        if user == line_in_csv_file["email"]:
                            os.remove("C:\Qr_codes\{}.jpeg".format(line_in_csv_file["code"]))
                            new_qr_code = generate_qr_code()
                            update_user_data(user, line_in_csv_file["code"], new_qr_code)
                            print("Du har nu uppdaterat din QR-kod")
            back_to_main_menu_user(user)
        if choice == 4:
            change_password(user)
            clear_screen()
            print("Ditt lösenord är nu uppdaterat.\n")
            back_to_main_menu_user(user)
        if choice == 5:
            clear_screen()
            with open("database.csv", "r") as csv_file_database:
                reader_for_csv_file = csv.DictReader(csv_file_database)
                for line_in_csv_file in reader_for_csv_file:
                    if line_in_csv_file["email"] == user:
                        user_to_delete = line_in_csv_file["code"]
            print("Genom att du tar bort ditt konto kommer all data att raderas.\n"
                  "Du kommer inte kunna använda några koppar du har kvar i ditt saldo")
            if yes_or_no("Är du säker på att du vill ta bort ditt konto? ") == "nej":
                back_to_main_menu_user(user)
            else:
                delete_user_in_csv_file(user_to_delete, "")
        if choice == 6:
            start_menu_main()
    else:
        start_menu_user(user)


def back_to_main_menu_admin():
    """Frågar ifall du vill tillbaka till huvudmenyn"""

    draw_line()
    print("\n[1] Tillbaka till huvudmenyn"
          "\n[2] Logga ut")
    while True:
        choice = is_it_int("\nVälj ifrån menyn ovan: ")
        if choice == 1:
            start_menu_admin()
            break
        if choice == 2:
            start_menu_main()
            break
        else:
            clear_screen()
            print("\nVänligen välj endast ifrån menyn ovan")
            back_to_main_menu_admin()


def back_to_main_menu_user(user):
    """Frågar ifall du vill tillbaka till användarmenyn"""

    draw_line()
    print("\n[1] Tillbaka till huvudmenyn"
          "\n[2] Logga ut")
    while True:
        choice = is_it_int("\nVälj ifrån menyn ovan: ")
        if choice == 1:
            start_menu_user(user)
            break
        if choice == 2:
            start_menu_main()
        else:
            clear_screen()
            print("\nVänligen välj endast ifrån menyn ovan")
            back_to_main_menu_user(user)


def inlogg_username():
    """Ser ifall användarnamnet du skriver in finns i databasen"""
    clear_screen()
    print("* För att komma tillbaka skriver du bara: tillbaka. *\n ")
    username = input("Email: ")
    admin_email = "admin@admin.se"
    admin_password = "1234"

    if username.lower() == "tillbaka":
        start_menu_main()

    if username == admin_email:
        inlogg_password(admin_email, admin_password, username)

    data_to_check = ["code", username, "password", "name", "value"]
    if check_if_already_in_file([data_to_check]) == "already in file":
        with open("database.csv", "r") as csv_file_database:
            reader_for_csv_file = csv.DictReader(csv_file_database)
            for line_in_csv_file in reader_for_csv_file:
                if username == line_in_csv_file["email"]:
                    inlogg_password("non-admin", line_in_csv_file["password"], username)
    else:
        print("Emailen finns inte.\n")
        draw_line()

        if yes_or_no("Vill du försöka igen? ") == "ja":
            inlogg_username()
        else:
            print("Ok välkommen åter.")


def inlogg_password(admin_email, correct_password, user):
    """Ser ifall lösenordet som anges är korrekt jämfört med databasen"""
    clear_screen()
    while True:
        print("* För att komma tillbaka skriver du bara: tillbaka. *\n ")
        password = input("Lösenord: ")
        if user.lower() == "tillbaka":
            inlogg_username()
            return
        if user == admin_email:
            if password == correct_password:
                start_menu_admin()
                break
        if password == correct_password:
            start_menu_user(user)
            break
        else:
            clear_screen()
            print("Fel lösenord försök igen.\n")
            draw_line()


def user_menu_info(user):
    """Info som printas ut för användaren"""

    clear_screen()
    with open("database.csv", "r") as csv_file_database:
        reader_for_csv_file = csv.DictReader(csv_file_database)

        for line_in_csv_file in reader_for_csv_file:
            if user == line_in_csv_file["email"]:
                print("Hej {}!".format(line_in_csv_file["name"]))
                print("\n"
                      "Du har {} koppar kvar att använda :D\n\n"
                      "Din QR-kod: {}\n"
                      "Din Email: {}\n"
                      "Din verifieringskod: {}\n".format(line_in_csv_file["value"], line_in_csv_file["code"],
                                                         line_in_csv_file["email"], line_in_csv_file["password"]))


start_menu_main()
