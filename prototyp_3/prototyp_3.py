import streamlit as st
from deta import Deta
from PIL import Image
import random
import qrcode
import pandas as pd
import numpy as np
import time

#_______________Databas saker__________________________________________
deta = Deta("a0nb3y9n_8mhjem33KMJEgDBcDRXLxABy2ZPDM79L")
db = deta.Base("users_db")



def insert_user(username, name, password, qr_code, value):
    data_to_add = {"key": username, "name": name, "password": password, "qr_code": qr_code, "value": value}
    if already_in_db(username, name) == "not in database":
        return db.put(data_to_add)
    else:
        return "user already in database"


def fetch_all_users():
    res = db.fetch()
    return res.items


def get_user_info(username):
    return db.get(username)


def update_user_data(username, updates):
    return db.update(updates, username)


def delete_user(username):
    return db.delete(username)


def already_in_db(username_to_check, name_to_check):
    try:
        username_to_check_info = get_user_info(username_to_check)
        if username_to_check_info["key"] == username_to_check:
            return "username already in system"
        elif username_to_check_info["name"] == name_to_check:
            return "name already in system"
    except:
        return "not in database"

def check_qr_code(qr_code_to_check):
    for i in fetch_all_users():
        if qr_code_to_check == i["qr_code"]:
            return "qr code already in database"
    return "qr code not in database"


#______________________________________________________________________

st.set_page_config(
    page_title="Kaffekortet",
    page_icon=":coffee:"
)


def generate_new_qr_code():
    data = str(random.randint(0, 250))
    if check_qr_code(data) == "qr code not in database":
        image = qrcode.make(data)
        image.save("{}.png".format(data))
        return data
    else:
        generate_new_qr_code()


def main_login():
    col1, col2 = st.columns([1, 1])
    with col1:
        st.title("Välkommen till Kaffekortet")
    with col2:
        st.image('hasbulla.gif', width=140)
    image = Image.open("Logo.png")
    st.sidebar.image(image)
    menu = ["Login", "Lägg till konto"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        username = st.sidebar.text_input("Användarnamn")
        password = st.sidebar.text_input("Lösenord", type="password")
        if st.sidebar.checkbox("Login"):
            try:
                password_db = get_user_info(username)["password"]
                if password == password_db:
                    st.sidebar.success("Inloggad som {}".format(username))
                    if get_user_info(username)["qr_code"] == "admin":
                        main_program_admin()
                    else:
                        main_program(username)
                else:
                    st.sidebar.warning("Fel lösenord eller användarnamn")
            except:
                st.sidebar.warning("Skriv in ett användarnamn och lösenord\n\nKontrollera att lösenordet och användarnamnet är rätt")

    elif choice == "Lägg till konto":
        st.subheader("Skapa ett konto")
        new_name = st.text_input("Namn")
        new_username = st.text_input("Användarnamn")
        new_password = st.text_input("Lösenord", type="password")
        qr_code = generate_new_qr_code()
        standard_value = "0"
        if st.button("Skapa konto"):
            if insert_user(new_username, new_name, new_password, qr_code, standard_value) == "user already in database":
                st.warning("Användarnamnet finns redan\n\nFörsök igen eller försök logga in")
            else:
                st.success("Du har nu skapat ett kaffekonto")
                st.info("Välj logga in i sidomenyn för att logga in")


def main_program(username):
    """Huvudprogram när man väl loggat in"""
    try:
        col1, col2 = st.columns((1, 1))
        with col1:
            st.image("./qr_codes/{}.png".format(get_user_info(username)["qr_code"]))
        with col2:
            st.subheader("Hej! {}!".format(get_user_info(username)["name"]))
            if get_user_info(username)["value"] != "0":
                st.write("\n\nDu har {} koppar kaffe kvar att använda.".format(get_user_info(username)["value"]))
            else:
                st.write(" \n\nOoh nej!\n Du har slut på kaffe. :(")
    except:
        st.write("Ops! något gick snett")

def main_program_admin():
    st.title("Admin")
    menu = ["Ta bort kaffekopp", "Lägg till kaffekopp",  "Visa information för ett konto", "Visa alla konton",
            "Hantera admin-konton"]
    choice = st.selectbox("Välj en meny", menu)
    if choice == "Ta bort kaffekopp":
        remove_value()
    if choice == "Lägg till kaffekopp":
        add_value()
    if choice == "Visa information för ett konto":
        show_specific_data()
    if choice == "Visa alla konton":
        show_accounts()
    if choice == ("Hantera admin-konton"):
        st.write("Hantering av adminkonton")


def remove_value():
    st.write("Här ska du kunna reducera antalet kaffekoppar för en användare.")


def add_value():
    st.write("Här kan du lägga till kaffekoppar hos en användare.")


def show_accounts():
    st.write("Här kan du se all statistik kring alla konton.")
    username_print= []
    name_print = []
    st.write("Totala antalet konton = {}".format(len(fetch_all_users())-1))

    for i in range(len(fetch_all_users())):
        if fetch_all_users()[i]["qr_code"] == "admin":
            continue
        else:
            if fetch_all_users()[i]["key"] not in username_print:
                username_print.append(fetch_all_users()[i]["key"])
                name_print.append(fetch_all_users()[i]["name"])
    d = {
        'Användarnamn': username_print, 
        'Namn': name_print}
    df = pd.DataFrame(data=d)
    st.dataframe(df, height=(35*len(fetch_all_users())), use_container_width=True)


def show_specific_data():
    st.write("Här kan du se specifik data för en viss användare.")


def manage_admin():
    st.write("Här kan du hantera olika admin-konton och dess befogenheter.")


if __name__ == "__main__":
    main_login()
