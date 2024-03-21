#!/usr/bin/env python3

from sqlalchemy import create_engine, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Person(Base):
    __tablename__ = "people"

    ssn = Column("ssn", Integer, primary_key=True)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    gender = Column("gender", CHAR)
    age = Column("age", Integer)

    def __init__(self, ssn, first, last, gender, age):
        self.ssn = ssn
        self.firstname = first
        self.lastname = last
        self.gender = gender
        self.age = age

    def __repr__(self):
        return f"({self.ssn}) {self.firstname} {self.lastname} ({self.gender}, {self.age})"

engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

person = Person(12312, "Mike", "Smith", "m", 35)
session.add(person)
session.commit()

p1 = Person(56012, "Foden", "Jack", "m", 32)
p2 = Person(15612, "Joan", "Wood", "f", 19)
p3 = Person(19412, "Peter", "Duke", "m", 29)
p4 = Person(13872, "Mary", "Ann", "f", 25)

# Adding multiple records
session.add_all([p1, p2, p3, p4])
session.commit()
