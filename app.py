import streamlit as st

from db import (
    PROGRAMY,
    nacti_studenta,
    najdi_studenty,
    naplnit_ukazkova_data,
    pridej_studenta,
    uprav_studenta,
)

ROCNIKY = [1, 2, 3, 4, 5]

st.set_page_config(page_title="Studenti")
naplnit_ukazkova_data()


if "vybrany_id" not in st.session_state:
    st.session_state.vybrany_id = None


def chyba_ve_formulari(jmeno, prijmeni, email):
    """Vrátí text chyby, nebo None, když jsou údaje v pořádku."""
    if not jmeno or not prijmeni or not email:
        return "Vyplňte jméno, příjmení i e-mail."
    if "@" not in email:
        return "E-mail nemá správný formát."
    return None


def stranka_seznam():
    """Seznam studentů s filtrem; jména jsou tlačítka do detailu."""
    st.title("Seznam studentů")

    sloupec1, sloupec2 = st.columns(2)
    with sloupec1:
        vyber_rocnik = st.selectbox("Ročník", ["Vše"] + ROCNIKY)
    with sloupec2:
        vyber_program = st.selectbox("Studijní program", ["Vše"] + PROGRAMY)

    
    rocnik = None if vyber_rocnik == "Vše" else vyber_rocnik
    program = None if vyber_program == "Vše" else vyber_program

    studenti = najdi_studenty(rocnik, program)
    st.write(f"Nalezeno studentů: {len(studenti)}")

    if not studenti:
        st.info("Žádný student neodpovídá filtru.")
    for s in studenti:
        if st.button(f"{s.prijmeni} {s.jmeno}", key=f"student_{s.id}"):
            st.session_state.vybrany_id = s.id
            st.rerun()


def stranka_detail(student_id):
    """Všechny informace o studentovi a formulář pro úpravu."""
    student = nacti_studenta(student_id)

    if st.button("← Zpět na seznam"):
        st.session_state.vybrany_id = None
        st.rerun()

    if student is None:
        st.error("Student nebyl nalezen.")
        return

    st.title(f"{student.jmeno} {student.prijmeni}")
    st.write(f"**E-mail:** {student.email}")
    st.write(f"**Ročník:** {student.rocnik}")
    st.write(f"**Studijní program:** {student.program}")

    st.subheader("Upravit údaje")
    with st.form("uprava"):
        jmeno = st.text_input("Jméno", value=student.jmeno)
        prijmeni = st.text_input("Příjmení", value=student.prijmeni)
        email = st.text_input("E-mail", value=student.email)
        rocnik = st.selectbox("Ročník", ROCNIKY, index=ROCNIKY.index(student.rocnik))
        program = st.selectbox(
            "Studijní program",
            PROGRAMY,
            index=PROGRAMY.index(student.program) if student.program in PROGRAMY else 0,
        )
        ulozit = st.form_submit_button("Uložit změny")

    if ulozit:
        chyba = chyba_ve_formulari(jmeno, prijmeni, email)
        if chyba:
            st.error(chyba)
        else:
            uprav_studenta(student_id, jmeno, prijmeni, email, rocnik, program)
            st.success("Změny jsou uložené.")


def stranka_pridat():
    """Formulář pro vložení nového studenta."""
    st.title("Přidat studenta")

    with st.form("novy", clear_on_submit=True):
        jmeno = st.text_input("Jméno")
        prijmeni = st.text_input("Příjmení")
        email = st.text_input("E-mail")
        rocnik = st.selectbox("Ročník", ROCNIKY)
        program = st.selectbox("Studijní program", PROGRAMY)
        pridat = st.form_submit_button("Přidat")

    if pridat:
        chyba = chyba_ve_formulari(jmeno, prijmeni, email)
        if chyba:
            st.error(chyba)
        else:
            pridej_studenta(jmeno, prijmeni, email, rocnik, program)
            st.success(f"Student {jmeno} {prijmeni} byl přidán.")


stranka = st.sidebar.radio("Menu", ["Seznam studentů", "Přidat studenta"])

if stranka == "Přidat studenta":
    stranka_pridat()
elif st.session_state.vybrany_id is not None:
    stranka_detail(st.session_state.vybrany_id)
else:
    stranka_seznam()
