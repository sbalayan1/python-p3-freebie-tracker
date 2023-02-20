#!/usr/bin/env python3

# Script goes here!
from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Freebie, Company, Dev


if __name__ == "__main__":
    engine = create_engine("sqlite:///freebies.db")
    Session = sessionmaker(bind=engine)
    session = Session()
    session.query(Freebie).delete()
    session.query(Company).delete()
    session.query(Dev).delete()

    print("seeding DATA!!!!!")
    faker = Faker()
    #company needs: name, year
    companies = []
    devs = []
    for i in range(0, 100):
        company = Company(name=faker.name(), founding_year=random.randint(1990, 2023))
        dev = Dev(name=faker.name())
        session.add(company)
        session.add(dev)
        session.commit()
        companies.append(company.id)
        devs.append(dev.id)

    #freebie needs: item_name, value, company_id, dev_id

    for i in range(0, 50):
        freebie = Freebie(
            item_name=faker.name(), 
            value=random.randint(0,100), 
            company_id=companies[i],
            dev_id=devs[i]
        )
        session.add(freebie)
        session.commit()

    session.close()

    print("Session closed!!!!")
    