from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CatalogItem

engine = create_engine('sqlite:///catalogitems.db')
Base.metadata.bind = engine

#Books of John Grisham (= Category1)
category1 = Category(name = "John Grisham")

session.add(category1)
session.commit()


#Books of Dale Carnegie (= Category 2)
category2 = Category(name = "Dale Carnegie")

session.add(category2)
session.commit()


#Books of Jamie Oliver (= Category 3)
category3 = Category(name = "Jamie Oliver")

session.add(category3)
session.commit()

DBSession = sessionmaker(bind=engine)
session = DBSession()
