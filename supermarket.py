import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='',
        password=''
    )
    
    if conn.is_connected():
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS grocery")
        cursor.execute("USE grocery")
        
        print("Connected to MySQL database")

        # Create tables for inventory, customers, and users
        cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                            product_name VARCHAR(255) PRIMARY KEY,
                            price FLOAT,
                            quantity INT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                            username VARCHAR(255) PRIMARY KEY,
                            member VARCHAR(3))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            username VARCHAR(255) PRIMARY KEY,
                            password VARCHAR(255) NOT NULL)''')

        # Initialize the database with some sample data
        inventory_data = [
            ("Lays", 10.0, 100),
            ("Kurkure", 30.0, 50),
            ("Bingo", 20.0, 150),
            ("Maggie", 20.0, 50),
            ("Maaza", 42.0, 70),
            ("Pepsi", 20.0, 80)
        ]

        customers_data = [
            ("akhil", "yes"),
            ("sonu", "no"),
            ("jayanth", "yes")
        ]

        users_data = [
            ("admin", "1234")
        ]

        # Insert inventory data
        for item in inventory_data:
            cursor.execute('''
                INSERT INTO inventory (product_name, price, quantity) 
                VALUES (%s, %s, %s) 
                ON DUPLICATE KEY UPDATE price=%s, quantity=%s
            ''', (item[0], item[1], item[2], item[1], item[2]))

        # Insert customer data
        for customer in customers_data:
            cursor.execute('''
                INSERT INTO customers (username, member) 
                VALUES (%s, %s) 
                ON DUPLICATE KEY UPDATE member=%s
            ''', (customer[0], customer[1], customer[1]))

        # Insert user data
        for user in users_data:
            cursor.execute('''
                INSERT INTO users (username, password) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE password=%s
            ''', (user[0], user[1], user[1]))

        conn.commit()
        print("Sample data inserted successfully")

        # Displays total inventory
        def Display_Inventory():
            cursor.execute('SELECT * FROM inventory')
            rows = cursor.fetchall()
            print("Product\t\tPrice\tQuantity")
            for row in rows:
                print(f"{row[0]}\t\t{row[1]}\t{row[2]}")

        # Inventory management
        def Inventory():
            commands = int(input("1. Check inventory\n2. Add products\n3. Remove products\n4. Modify\n5. Go back\nEnter your command: "))
            
            if commands == 1:  # Displays inventory
                Display_Inventory()
            
            elif commands == 2:  # Adding products
                new_product = input("Enter new product name: ")
                price = float(input("Enter price: "))
                quantity = int(input("Enter quantity: "))
                cursor.execute('''INSERT INTO inventory (product_name, price, quantity) VALUES (%s, %s, %s)''', (new_product, price, quantity))
                conn.commit()
                print(f"{new_product} added to inventory.")
                Display_Inventory()

            elif commands == 3:  # Delete products
                deleted_product = input("Enter product name to be deleted: ")
                cursor.execute('''DELETE FROM inventory WHERE product_name = %s''', (deleted_product,))
                conn.commit()
                print(f"{deleted_product} removed from inventory.")
                Display_Inventory()

            elif commands == 4:  # Modify products
                Display_Inventory()
                product_name = input("Enter which product to be modified: ")
                modify = int(input("What do you want to modify?\n1. Name\n2. Price\n3. Quantity\nEnter command: "))
                if modify == 1:
                    new_name = input("Enter new name: ")
                    cursor.execute('''UPDATE inventory SET product_name = %s WHERE product_name = %s''', (new_name, product_name))
                elif modify == 2:
                    price = float(input("Enter new price: "))
                    cursor.execute('''UPDATE inventory SET price = %s WHERE product_name = %s''', (price, product_name))
                elif modify == 3:
                    quantity = int(input("Enter new quantity: "))
                    cursor.execute('''UPDATE inventory SET quantity = %s WHERE product_name = %s''', (quantity, product_name))
                conn.commit()
                Display_Inventory()

        # Billing section
        def Billing():
            print("1. Billing\n2. Exit")
            bill_commands = int(input("Enter command: "))
            if bill_commands == 1:
                total_bill = 0
                cart = {}
                while True:
                    print("1. Add items\n2. Remove items\n3. Modify quantity\n4. Checkout\n5. Exit")
                    sub_command = int(input("Enter sub-command: "))
                    if sub_command == 1:
                        product = input("Enter product to add: ")
                        cursor.execute('''SELECT price, quantity FROM inventory WHERE product_name = %s''', (product,))
                        result = cursor.fetchone()
                        if result:
                            price, available_quantity = result
                            quantity = int(input("Enter quantity: "))
                            if quantity <= available_quantity:
                                cursor.execute('''UPDATE inventory SET quantity = quantity - %s WHERE product_name = %s''', (quantity, product))
                                if product in cart:
                                    cart[product]['quantity'] += quantity
                                else:
                                    cart[product] = {"price": price, "quantity": quantity}
                                total_bill += price * quantity
                                print(f"{quantity} of {product} added to bill. Subtotal: {total_bill}")
                            else:
                                print(f"\033[91mInsufficient stock for {product}\033[00m")
                        else:
                            print(f"\033[91mProduct {product} not found!\033[00m")

                    elif sub_command == 2:
                        product = input("Enter product to remove: ")
                        if product in cart:
                            quantity = cart[product]['quantity']
                            cursor.execute('''UPDATE inventory SET quantity = quantity + %s WHERE product_name = %s''', (quantity, product))
                            total_bill -= cart[product]['price'] * quantity
                            del cart[product]
                            print(f"{product} removed from bill. Subtotal: {total_bill}")
                        else:
                            print(f"\033[91mProduct {product} not in bill!\033[00m")

                    elif sub_command == 3:
                        product = input("Enter product to modify quantity: ")
                        if product in cart:
                            new_quantity = int(input("Enter new quantity: "))
                            old_quantity = cart[product]['quantity']
                            if new_quantity > old_quantity:
                                difference = new_quantity - old_quantity
                                cursor.execute('''SELECT quantity FROM inventory WHERE product_name = %s''', (product,))
                                available_quantity = cursor.fetchone()[0]
                                if available_quantity >= difference:
                                    cursor.execute('''UPDATE inventory SET quantity = quantity - %s WHERE product_name = %s''', (difference, product))
                                    cart[product]['quantity'] = new_quantity
                                    total_bill += cart[product]['price'] * difference
                                    print(f"Quantity of {product} updated to {new_quantity}. Subtotal: {total_bill}")
                                else:
                                    print(f"\033[91mInsufficient stock for {product}\033[00m")
                            else:
                                difference = old_quantity - new_quantity
                                cursor.execute('''UPDATE inventory SET quantity = quantity + %s WHERE product_name = %s''', (difference, product))
                                cart[product]['quantity'] = new_quantity
                                total_bill -= cart[product]['price'] * difference
                                print(f"Quantity of {product} updated to {new_quantity}. Subtotal: {total_bill}")
                        else:
                            print(f"\033[91mProduct {product} not in bill!\033[00m")

                    elif sub_command == 4:
                        print(f"Total bill is: {total_bill}")
                        break

                    elif sub_command == 5:
                        break

                    else:
                        print(f"\033[91mINVALID COMMAND!\033[00m")
            elif bill_commands == 2:
                pass

        # Check user credentials
        def check_credentials(username, password):
            cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
            user = cursor.fetchone()
            return user is not None

        # Main page
        menu = "WELCOME TO GROCERY MANAGEMENT SYSTEM"
        dash_length = len(menu) + 2
        print('-' * dash_length)
        print(f"\033[92m {menu}\033[00m")
        print('-' * dash_length)
        print("Please Login!")

        flag = True
        count = 0
        while flag:
            commands = int(input("1. Login\n2. Exit\nEnter command: "))
            if commands == 1:
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                if check_credentials(username, password):
                    print(f"Welcome {username}!")
                    new_flag = True
                    while new_flag:
                        admin_commands = int(input("1. Inventory\n2. Billing\n3. Log out\nEnter command: "))
                        if admin_commands == 1:
                            print("Inventory")
                            Inventory()
                        elif admin_commands == 2:
                            print("Billing")
                            Billing()
                        elif admin_commands == 3:
                            print("Log out")
                            new_flag = False
                        else:
                            print(f"\033[91mINVALID COMMAND!\033[00m")
                else:
                    count += 1
                    print(f"\033[91mINVALID CREDENTIALS\033[00m")
                    if count == 3:
                        print("Too many attempts, you suck.")
                        flag = False
            elif commands == 2:
                flag = False
            else:
                print(f"\033[91mINVALID COMMAND!\033[00m")

except Error as e:
    print(f"Error connecting to MySQL database: {e}")

finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection closed")
