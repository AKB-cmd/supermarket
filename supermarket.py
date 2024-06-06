# Creating a dictionary of inventory
inventory = {"Lays": {"price": 10.0, "quantity": 100},
             "Kurkure": {"price": 30.0, "quantity": 50},
             "Bingo": {"price": 20.0, "quantity": 150},
             "Maggie": {"price": 20.0, "quantity": 50},
             "Maaza": {"price": 42.0, "quantity": 70},
             "Pepsi": {"price": 20.0, "quantity": 80}}

cred = ("admin", "1234")
# Customers with and without membership
customers = {"akhil": {"member": "yes"},
             "sonu": {"member": "no"},
             "jayanth": {"member": "yes"}}

# Displays total inventory
def Display_Inventory(inventory):
    for key, value in inventory.items():
        print(f"{key}\t\t{value['price']}\t{value['quantity']}")

# Inventory management
def Inventory(inventory):
    commands = int(input("1. Check inventory\n2. Add products\n3. Remove products\n4. Modify\n5. Go back\nEnter your command: "))
    
    if commands == 1:  # Displays inventory
        print("Product\t\tPrice\tQuantity")
        Display_Inventory(inventory)
    
    elif commands == 2:  # Adding products
        new_product = input("Enter new product name: ")
        price = float(input("Enter price: "))
        quantity = int(input("Enter quantity: "))
        inventory[new_product] = {"price": price, "quantity": quantity}
        print(f"{new_product} added to inventory.")
        Display_Inventory(inventory)

    elif commands == 3:  # Delete products
        deleted_product = input("Enter product name to be deleted: ")
        if deleted_product in inventory:
            del inventory[deleted_product]
            print(f"{deleted_product} removed from inventory.")
        else:
            print(f"\033[91m{deleted_product} not found!\033[00m")
        Display_Inventory(inventory)

    elif commands == 4:  # Modify products
        Display_Inventory(inventory)
        product_name = input("Enter which product to be modified: ")
        if product_name in inventory.keys():
            modify = int(input("What do you want to modify?\n1. Name\n2. Price\n3. Quantity\nEnter command: "))
            if modify == 1:
                name = input("Enter new name: ")
                inventory[name] = inventory.pop(product_name)
            elif modify == 2:
                price = float(input("Enter new price: "))
                inventory[product_name]['price'] = price
            elif modify == 3:
                quantity = int(input("Enter new quantity: "))
                inventory[product_name]['quantity'] = quantity
            Display_Inventory(inventory)

# Billing section
def Billing():
    print("1. Billing\n2. Exit")
    bill_commands = int(input("Enter command: "))
    cart = {}
    if bill_commands == 1:
        total_bill = 0
        while True:
            print("1. Add items\n2. Remove items\n3. Modify quantity\n4. Checkout\n5. Exit")
            sub_command = int(input("Enter sub-command: "))

            if sub_command == 1:
                product = input("Enter product to add: ")
                if product in inventory:
                    quantity = int(input("Enter quantity: "))
                    if quantity <= inventory[product]['quantity']:
                        inventory[product]['quantity'] -= quantity
                        if product in cart:
                            cart[product]['quantity'] += quantity
                        else:
                            cart[product] = {"price": inventory[product]['price'], "quantity": quantity}
                        total_bill += inventory[product]['price'] * quantity
                        print(f"{quantity} of {product} added to bill. Subtotal: {total_bill}")
                    else:
                        print(f"\033[91mInsufficient stock for {product}\033[00m")
                else:
                    print(f"\033[91mProduct {product} not found!\033[00m")

            elif sub_command == 2:
                product = input("Enter product to remove: ")
                if product in cart:
                    quantity = cart[product]['quantity']
                    total_bill -= cart[product]['price'] * quantity
                    inventory[product]['quantity'] += quantity
                    del cart[product]
                    print(f"{product} removed from bill. Subtotal: {total_bill}")
                else:
                    print(f"\033[91mProduct {product} not in bill!\033[00m")

            elif sub_command == 3:
                product = input("Enter product to modify quantity: ")
                if product in cart:
                    new_quantity = int(input("Enter new quantity: "))
                    difference = new_quantity - cart[product]['quantity']
                    if inventory[product]['quantity'] >= difference:
                        cart[product]['quantity'] = new_quantity
                        inventory[product]['quantity'] -= difference
                        total_bill += cart[product]['price'] * difference
                        print(f"Quantity of {product} updated to {new_quantity}. Subtotal: {total_bill}")
                    else:
                        print(f"\033[91mInsufficient stock for {product}\033[00m")
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
        if username == cred[0] and password == cred[1]:
            print(f"Welcome {username}!")
            new_flag = True
            while new_flag:
                admin_commands = int(input("1. Inventory\n2. Billing\n3. Log out\nEnter command: "))
                if admin_commands == 1:
                    print("Inventory")
                    Inventory(inventory)
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
