#!/usr/bin/env python3

from sqlalchemy import (Column, String, Integer, ForeignKey, create_engine, asc)
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()

def create_session():
    engine = create_engine("sqlite:///freebies.db")
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    company_id = Column(ForeignKey('companies.id')) #we say companies.id here because we are referencing the TABLENAME. SQLAlchemy uses the table name to find the table and generates a foreign key using the id column
    dev_id = Column(ForeignKey('devs.id'))
    
    def __repr__(self):
        return f'<Freebie {self.item_name}>'
    
    
    def print_details(self):
        print(f'{self.dev.name} owns {self.item_name} from {self.company.name}')


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship('Freebie', backref='company')
    devs = association_proxy('freebies', 'dev', creator=lambda d: Freebie(dev=d)) 

    #why do we need an association proxy? 
        #an association proxy creates a read/write view of an attribute ACROSS a relationship. The benefit is that it essentially conceals the usage of a middle attribute within a many to many relationship
        #in the above, we look through the freebies table and create an association between the Dev and Company models using the dev column within freebies. 


    def __repr__(self):
        return f'<Company {self.name}>'

    def give_freebie(self, dev, item_name, value):
        pass
        freebie = Freebie(item_name = item_name, value = value, company_id = self.id, dev_id = dev.id)

    
    @classmethod
    def oldest_company(cls):
        pass
        session = create_session()
        oldest_company = session.query(cls).order_by(asc(cls.founding_year)).limit(1).first()
        session.close()
        return oldest_company


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    freebies = relationship('Freebie', backref='dev')
    companies = association_proxy('freebies', 'company', creator=lambda c: Freebie(company=d))

    #why do we need the creator method here? 
        #when we add a new company to our companies attribute, we need to create a new instance of the middle object. Under the hood, Freebies is what establishes the relationship between Dev and Company. To create a new instance of Freebies, you would need all of its required fields like item_name, value, company_id, dev_id, etc. The creator function lets us avoid this problem by allowing us to create that middle object instance using a single argument. 

    def __repr__(self):
        return f'<Dev {self.name}>'

    def received_one(self, item_name):
        return item_name in [freebie.item_name for freebie in self.freebies]
    
    def give_away(self, dev, freebie):
        #if the freebie belongs to the current dev
        if (self.received_one(freebie.item_name)):
            freebie.dev_id = dev.id
            return freebie




