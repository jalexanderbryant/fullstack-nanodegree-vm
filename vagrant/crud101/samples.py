from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, engine

Base.metadata.bind = engine
session = sessionmaker(bind = engine)()

# Veggie Burgers
veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for burger in veggieBurgers:
    print(burger.id)
    print(burger.price)
    print(burger.restaurant.name)
    print("\n")

# Single veggie burger
vb = session.query(MenuItem).filter_by(id = 3).one()
print("Before change:", vb.id, vb.name, vb.price)

vb.price = '$4.99'
#session.add(vb)
#session.commit()

vb = session.query(MenuItem).filter_by(id = 3).one()
print("After change:", vb.id, vb.name, vb.price)

for veggieBurger in veggieBurgers:
    if veggieBurger.price != '$2.99':
        veggieBurger.price = '$2.99'
        #session.add(veggieBurger)
        #session.commit(i)

# Delete
spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
print("Item to be deleted: ", spinach.name)
session.delete(spinach)
session.commit()

spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()



#items = session.query(MenuItem).all()
#count = session.query(MenuItem).count()
#print("Total Items: {}".format(count))
#for item in items:
#    print(item.name)
