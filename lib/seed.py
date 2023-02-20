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
    company = Company(name=faker.name(), founding_year=random.randint(1990, 2023))
    session.add(company)

    #dev needs: name
    dev = Dev(name=faker.name())
    session.add(dev)
    session.commit()

    #freebie needs: item_name, value, company_id, dev_id
    freebie = Freebie(
        item_name=faker.name(), 
        value=random.randint(0,100), 
        company_id=company.id, 
        dev_id=dev.id)

    session.add(freebie)
    session.commit()
    session.close()

    print("Session closed!!!!")
    