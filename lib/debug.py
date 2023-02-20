#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    freebie = session.query(Freebie).first()
    print("Freebie: ", freebie)
    print("Freebie.dev: ", freebie.dev)
    print("Freebie.company", freebie.company)

    company = session.query(Company).first()
    print("Company: ", company)
    print("Company.freebies:", company.freebies)
    print("Company.devs:", company.devs)

    dev = session.query(Dev).first()
    print("dev: ", dev)
    print("dev.freebies:", dev.freebies)
    print("dev.devs:", dev.companies)

    import ipdb; ipdb.set_trace()
