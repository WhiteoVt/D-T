
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class FastAPIVote(Base):
    __tablename__ = 'drf_vote'  

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, nullable=True)
    owner_id = Column(Integer, ForeignKey('auth_user.id'))  
    product_id = Column(Integer, ForeignKey('product.id')) 



class FastAPIProduct(Base):
    __tablename__ = 'drf_product'

    id = Column(Integer, primary_key=True, index=True)
    bggid = Column(Integer, nullable=True)
    name = Column(String)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    slug = Column(String(100), nullable=True, index=True, unique=True)
    min_players = Column(Integer, nullable=True)
    max_players = Column(Integer, nullable=True)
    image_url = Column(String, nullable=True)
    image1 = Column(String, nullable=True)  
    image2 = Column(String, nullable=True) 
    image3 = Column(String, nullable=True)  
    image4 = Column(String, nullable=True) 
    image5 = Column(String, nullable=True)  
    thumbnail = Column(String, nullable=True)  
    thumbnail_url = Column(String, nullable=True) 


