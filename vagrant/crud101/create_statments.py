from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, engine

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

r1 = Restaurant(name = "Pizza Palace")
# session.add(r1)
cheesepizza = MenuItem(name = "Cheese Pizza",
                       description= "Made with all natural ingredients",
                       course = "Entree",
                       price = '$5.99',
                       restaurant = r1)

session.add(cheesepizza)
# session.commit()

# print(session.query(MenuItem).all())
q = session.query(Restaurant).all()
for e in q:
  print(e.name)
# print(session.query(Restaurant).all())


