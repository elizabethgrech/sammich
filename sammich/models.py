from sqlalchemy import (
    Column,
    INTEGER,
    VARCHAR,
    DATETIME,
    BOOLEAN,
    DATE,
    NUMERIC)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

#----------------------------------------------------------------------------------------------------------------------#
#                                            Table Structures                                                          #
#----------------------------------------------------------------------------------------------------------------------#


class Users(Base):
    __tablename__ = 'users'
    id = Column(INTEGER, primary_key=True)
    first_name = Column(VARCHAR)
    last_name = Column(VARCHAR)


class FoodItems(Base):
    __tablename__ = 'fooditems'
    id = Column(INTEGER, primary_key=True, unique=True)
    name = Column(INTEGER)
    type = Column(VARCHAR)
    servings = Column(INTEGER)
    calories = Column(INTEGER)
    carbs = Column(INTEGER)
    fat = Column(INTEGER)
    protien = Column(INTEGER)


class FoodType(Base):
    __tablename__ = 'foodtype'
    id = Column(INTEGER,primary_key=True, unique=True)
    name = Column(VARCHAR)


class NutritionList(Base):
    __tablename__ = 'nutritionlist'
    id = Column(INTEGER,primary_key=True, unique=True)
    fooditemsid = Column(INTEGER)
    nutritiontypeid = Column(INTEGER)


class NutritionType(Base):
    __tablename__ = 'nutritiontype'
    id = Column(INTEGER,primary_key=True, unique=True)
    name = Column(VARCHAR, unique=True)


class Servings(Base):
    __tablename__ = 'servings'
    id = Column(INTEGER,primary_key=True, unique=True)
    fooditemsid = Column(INTEGER)
    servingtype = Column(INTEGER)
    servingsize = Column(NUMERIC)


class ServingType(Base):
    __tablename__ = 'servingtype'
    id = Column(INTEGER,primary_key=True, unique=True)
    unitid = Column(INTEGER)
    unitname = Column(VARCHAR)


class units(Base):
    __tablename__ = 'units'
    id = Column(INTEGER,primary_key=True, unique=True)
    name = Column(INTEGER)
    abriviation = Column(INTEGER)
