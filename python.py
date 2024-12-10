import pandas as pd
from datetime import datetime

#order manangement system
class BakeryOrderMangement():
    def __init__(self):
        self.orders = pd.DataFrame(columns=["Customer Name", "Item", "Quantity", "Order Date"])

    def add_order(self):
        customer_name = input("Enter customer name: ")
        item = input("Enter item ordered: ")
        try:
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print("Invalid quantity. Please enter a valid number.")
            return
        order_date = datetime.now().strftime("%Y-%m-%d")
        new_order = pd.DataFrame([[customer_name, item, quantity, order_date]], 
                         columns=["Customer Name", "Item", "Quantity", "Order Date"])

        self.orders = pd.concat([self.orders, new_order], ignore_index=True)

        print("\nOrder added successfully")


    def view_orders(self):
        print("\ncurrent Orders")
        if self.orders.empty:
            print('No orders available')
        else:
            print(self.orders)

    def update_orders(self):
        try:
            order_id = int(input("Enter order ID to update: "))
        except ValueError:
            print("Invalid ID. Please enter a valid number.")
            return
        if order_id < 0 or order_id >= len(self.orders):
            print("order not found")
        else:
            print("Updating Order Id: ", order_id)
            self.orders.at[order_id,'Customer Name'] = input("Enter a new customer name: ")
            self.orders.at[order_id, "Item"] = input("Enter new item: ")
            try:
                self.orders.at[order_id, "Quantity"] = int(input("Enter new quantity: "))
            except ValueError:
                print("Invalid quantity. Update aborted.")
                return

            print('Order updated successfully')

    def save_to_excel(self):
        self.orders.to_excel("Bakery_orders.xlsx",index = False)
        print('Orders saved to excel successfully')

bakery = BakeryOrderMangement()

while True:
    print("\n --- Bakery Order Management System --- \n\n")
    print("1. Add Orders")
    print("2. View Orders")
    print("3. Update Orders")
    print("4. Save to Excel")
    print("5. Exit")

    choice = input("Enter your Choice: ")

    if choice == "1":
        bakery.add_order()
    elif choice == "2":
        bakery.view_orders()
    elif choice == "3":
        bakery.update_orders()
    elif choice == "4":
        bakery.save_to_excel()
    elif choice == "5":
        break
    else:
        print("Invalid choice . please ty again")