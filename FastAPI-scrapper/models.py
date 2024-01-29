from sqlalchemy import create_engine, Column, Integer, String, Sequence, Text, Boolean, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "postgresql://maciej:maciej@database:5432/DiceAndTiles"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, Sequence("item_id_seq"), primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)




class Product(Base):
    __tablename__ = 'drf_fetched_product'

    id = Column(Integer, primary_key=True, index=True)
    bggid = Column(Integer, nullable=True)
    name = Column(String)
    description = Column(Text, nullable=True)
    slug = Column(String, nullable=True)
    min_players = Column(Integer, nullable=True)
    max_players = Column(Integer, nullable=True)
    image_url = Column(String, nullable=True)
    thumbnail_url = Column(String, nullable=True)

   


# Base.metadata.create_all(bind=engine)
