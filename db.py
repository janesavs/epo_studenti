from sqlmodel import Field, Session, SQLModel, create_engine, select

engine = create_engine("sqlite:///studenti.db")

PROGRAMY = ["Informační management", "Podniková ekonomika a management", "Obchod a podnikání"]


class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    jmeno: str
    prijmeni: str
    email: str
    rocnik: int
    program: str


SQLModel.metadata.create_all(engine)


def pridej_studenta(jmeno, prijmeni, email, rocnik, program):
    """Vloží nového studenta do databáze."""
    with Session(engine) as session:
        student = Student(jmeno=jmeno, prijmeni=prijmeni, email=email, rocnik=rocnik, program=program)
        session.add(student)
        session.commit()
       


def najdi_studenty(rocnik=None, program=None):
    """Vrátí studenty seřazené podle příjmení. Když je zadán ročník nebo program, jen odpovídající."""
    with Session(engine) as session:
        dotaz = select(Student)
        if rocnik is not None:
            dotaz = dotaz.where(Student.rocnik == rocnik)
        if program is not None:
            dotaz = dotaz.where(Student.program == program)

        dotaz = dotaz.order_by(Student.prijmeni)
        return session.exec(dotaz).all()


def nacti_studenta(student_id):
    """Vrátí jednoho studenta podle id (nebo None)."""
    with Session(engine) as session:
        return session.get(Student, student_id)
        


def uprav_studenta(student_id, jmeno, prijmeni, email, rocnik, program):
    """Přepíše údaje existujícího studenta."""
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if student is None:
            return
        student.jmeno = jmeno
        student.prijmeni = prijmeni
        student.email = email
        student.rocnik = rocnik
        student.program = program
        session.add(student)
        session.commit()


def naplnit_ukazkova_data():
    """Když je databáze prázdná, vloží ukázkové studenty."""
    if najdi_studenty():   # v databázi už někdo je -> nic nedělat
        return
    ukazkovi = [
        ("Jana", "Nováková", "jana.novakova@example.com", 3, PROGRAMY[0]),
        ("Petr", "Svoboda", "petr.svoboda@example.com", 1, PROGRAMY[1]),
        ("Lucie", "Dvořáková", "lucie.dvorakova@example.com", 2, PROGRAMY[0]),
        ("Tomáš", "Černý", "tomas.cerny@example.com", 3, PROGRAMY[2]),
        ("Eva", "Procházková", "eva.prochazkova@example.com", 1, PROGRAMY[0]),
        ("Martin", "Kučera", "martin.kucera@example.com", 2, PROGRAMY[1]),
    ]
    for s in ukazkovi:
        pridej_studenta(*s)
            
        


if __name__ == "__main__":
    naplnit_ukazkova_data()
    print(najdi_studenty())