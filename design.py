import pandas as pd
from datetime import datetime
import streamlit as st

# Order Management System
class BakeryOrderManagement:
    def __init__(self):
        self.orders = pd.DataFrame(columns=["Customer Name", "Item", "Quantity", "Order Date"])

    def add_order(self, customer_name, item, quantity):
        order_date = datetime.now().strftime("%Y-%m-%d")
        new_order = pd.DataFrame([[customer_name, item, quantity, order_date]], 
                                 columns=["Customer Name", "Item", "Quantity", "Order Date"])
        self.orders = pd.concat([self.orders, new_order], ignore_index=True)

    def update_order(self, order_id, customer_name, item, quantity):
        self.orders.at[order_id, "Customer Name"] = customer_name
        self.orders.at[order_id, "Item"] = item
        self.orders.at[order_id, "Quantity"] = quantity

    def save_to_excel(self, file_name="My_cafe_orders.xlsx"):
        self.orders.to_excel(file_name, index=False)

# Initialize Bakery Management
bakery = BakeryOrderManagement()

# Streamlit App
st.title("🍰 Cafe Management System")
st.sidebar.title("Navigation")
option = st.sidebar.radio("Choose an option:", ["Add Order", "View Orders", "Update Order", "Save to Excel"])

# Add Order
if option == "Add Order":
    st.header("Add a New Order")
    customer_name = st.text_input("Customer Name")
    item = st.text_input("Item Ordered")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    
    if st.button("Add Order"):
        if customer_name and item:
            bakery.add_order(customer_name, item, quantity)
            st.success(f"Order added successfully for {customer_name}!")
        else:
            st.error("Please fill in all the fields.")

# View Orders
elif option == "View Orders":
    st.header("Current Orders")
    if bakery.orders.empty:
        st.info("No orders available.")
    else:
        st.dataframe(bakery.orders)

# Update Order
elif option == "Update Order":
    st.header("Update an Existing Order")
    if bakery.orders.empty:
        st.info("No orders to update.")
    else:
        order_id = st.number_input("Enter Order ID to update", min_value=0, max_value=len(bakery.orders)-1, step=1)
        selected_order = bakery.orders.iloc[order_id]
        
        st.write(f"Editing Order ID: {order_id}")
        customer_name = st.text_input("Customer Name", selected_order["Customer Name"])
        item = st.text_input("Item Ordered", selected_order["Item"])
        quantity = st.number_input("Quantity", min_value=1, step=1, value=int(selected_order["Quantity"]))
        
        if st.button("Update Order"):
            bakery.update_order(order_id, customer_name, item, quantity)
            st.success("Order updated successfully!")

# Save to Excel
elif option == "Save to Excel":
    st.header("Save Orders to Excel")
    file_name = st.text_input("Enter file name:", "Bakery_orders.xlsx")
    
    if st.button("Save"):
        bakery.save_to_excel(file_name)
        st.success(f"Orders saved to {file_name} successfully!")

# Footer
st.sidebar.markdown("---")
st.sidebar.write("Made with ❤️ using Streamlit")
