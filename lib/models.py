#!/usr/bin/env python3

from sqlalchemy import (Column, String, Integer, ForeignKey)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    company_id = Column(ForeignKey('companies.id')) #we say companies.id here because we are referencing the TABLENAME. SQLAlchemy uses the table name to find the table and generates a foreign key using the id column
    dev_id = Column(ForeignKey('devs.id'))
    
    def __repr__(self):
        return f'<Freebie {self.item_name}>'


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


