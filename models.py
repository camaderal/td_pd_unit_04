from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# create a database
engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# inventory.db
class Product(Base):
    __tablename__ = 'inventory'

    product_id = Column(Integer, primary_key=True)
    product_name = Column('Name', String)
    product_quantity = Column('Quantity', Integer)
    product_price = Column('Price', Integer)
    date_updated = Column('Updated', DateTime)

    def __repr__(self) :
        return f'Name: {self.product_name} | Quantity:{self.product_quantity} | Price: {self.product_price} | Updated:{self.date_updated} '