from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()
Base = declarative_base()


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    last_change_date = Column(DateTime, default=datetime.utcnow)
    warehouse_name = Column(String)
    country_name = Column(String)
    oblast_okrug_name = Column(String)
    region_name = Column(String)
    supplier_article = Column(String)
    nm_id = Column(Integer)
    barcode = Column(String)
    category = Column(String)
    subject = Column(String)
    brand = Column(String)
    total_price = Column(Float)
    order_type = Column(String)
    sticker = Column(String)
    g_number = Column(String)
    srid = Column(String)


class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    last_change_date = Column(DateTime, default=datetime.utcnow)
    warehouse_name = Column(String)
    country_name = Column(String)
    oblast_okrug_name = Column(String)
    region_name = Column(String)
    supplier_article = Column(String)
    nm_id = Column(Integer)
    barcode = Column(String)
    category = Column(String)
    subject = Column(String)
    brand = Column(String)
    total_price = Column(Float)
    for_pay = Column(Float)
    order_type = Column(String)
    sticker = Column(String)
    g_number = Column(String)
    srid = Column(String)


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)


#
engine = create_engine('postgresql://aroxan:7799@localhost/marketplay')


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
