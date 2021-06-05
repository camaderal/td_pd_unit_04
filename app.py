import csv
import time
import datetime
from sqlalchemy.exc import NoResultFound 
from models import (Base, session, engine, Product)

def add_product_to_db(name, price, qty, upd_dt, show_msg=False):
    product = session.query(Product).filter(Product.product_name == name).one_or_none()

    if product == None:
        product = Product(product_name=name, product_price=price, product_quantity=qty, date_updated=upd_dt)
        session.add(product)
        session.commit()

        if show_msg:
            print("Product added!")

    elif product.date_updated <= upd_dt:
        product.product_name=name
        product.product_price=price
        product.product_quantity=qty
        product.date_updated=upd_dt
        session.commit()

        if show_msg:
            print("Product updated!")

    else:
        if show_msg:
            print("Product was already added/updated on a later date. This transaction will be cancelled.")

    if show_msg:
        time.sleep(1.5)
    


def format_price(price):
    price = price.replace("$", "")
    price = float(price)
    price = int(price * 100)

    return price

def reformat_price(price):
    return "$" + str(price * .01)


def format_qty(qty):
    return int(qty)


def format_upd_dt(upd_dt):
    return datetime.datetime.strptime(upd_dt, "%m/%d/%Y").date()

def ask_price():
    while True:
        price = input("Input price: ");
        try:
            float(price)
            return format_price(price)
        except ValueError:
            input('''
                \nInvalid input. 
                \rPlease only input numerical values(e.g: 10.99). 
                \rOnly up to two decimal places will be saved.
                \rPress enter to try again.''')


def ask_qty():
    while True:
        qty = input("Input quantity: ");
        try:
            return format_qty(qty)
        except ValueError:
            input('''
                \nInvalid input. 
                \rPlease only input numerical values(e.g: 25). 
                \rPress enter to try again.''')


def init_products():
    with open('inventory.csv') as csv_file:
        products = list(csv.reader(csv_file))
        for product in products[1:]:
            name = product[0]
            price = format_price(product[1])
            qty = format_qty(product[2])
            upd_dt = format_upd_dt(product[3])
            add_product_to_db(name, price, qty, upd_dt)
           

def add_product():
    name = input("Input product name: ")
    price = ask_price()
    qty = ask_qty()
    upd_dt = datetime.datetime.now().date()

    add_product_to_db(name, price, qty, upd_dt, True)


def view_product():
    while True:
        product_id = input("Enter product id: ")
        try:
            product = session.query(Product).filter_by(product_id=product_id).one()
        except NoResultFound as error:
            print(f"The product with the product id of '{product_id}' does not exist. Please try again.")
            continue

        print(f'''
            \n
            \rProduct Id: {product.product_id}
            \rName: {product.product_name}
            \rPrice: {reformat_price(product.product_price)}
            \rQuantity: {product.product_quantity}
            \rDate Updated: {product.date_updated}
            \r
        ''')
        input("Press any key to continue.")
        break

def backup_inventory():
    fieldnames = ["product_id","product_name","product_price","product_quantity","date_updated"]
    with open(file='backup.csv', mode="w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for product in session.query(Product).all():
            writer.writerow({
                "product_id": product.product_id,
                "product_name": product.product_name,
                "product_price": product.product_price,
                "product_quantity": product.product_quantity,
                "date_updated": product.date_updated,

            })

def show_menu():
    while True:
        print('''
            \nMy Store Inventory
            \r
            \r[V] View a product
            \r[A] Add a product
            \r[B] Backup inventory
            \r[E] Exit
            \r 
        ''')

        choice = input("Input an option: ").upper()
        if choice not in ['V', 'A', 'B', 'E']:
            input("Not a valid option. Please press any key to try again.")
            continue

        if choice == 'V':
            view_product()
        elif choice == 'A':
            add_product()
        elif choice == 'B':
            backup_inventory()
        else:
            print("Good day!")
            break

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    init_products()
    show_menu()