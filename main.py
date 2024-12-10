import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize session state for storage (if not already initialized)
if 'orders' not in st.session_state:
    st.session_state.orders = pd.DataFrame(columns=["Customer Name", "Item", "Quantity", "Order Date"])
if 'customers' not in st.session_state:
    st.session_state.customers = pd.DataFrame(columns=["Customer Name", "Order History"])

# Bakery Order Management
class BakeryOrderManagement:
    def __init__(self):
        self.orders = st.session_state.orders
        self.customers = st.session_state.customers

    def add_order(self, customer_name, item, quantity, order_date):
        order_date = pd.to_datetime(order_date).strftime("%Y-%m-%d")  # Convert to proper date format
        
        
        new_order = pd.DataFrame([[customer_name, item, quantity, order_date,]],
                             columns=["Customer Name", "Item", "Quantity", "Order Date"])
        st.session_state.orders = pd.concat([st.session_state.orders, new_order], ignore_index=True)
    
    # Add to customer order history
        if customer_name not in self.customers["Customer Name"].values:
            new_customer = pd.DataFrame([{"Customer Name": customer_name, "Order History": []}])
            self.customers = pd.concat([self.customers, new_customer], ignore_index=True)
    
        customer_index = self.customers[self.customers["Customer Name"] == customer_name].index[0]
        order_history = self.customers.at[customer_index, "Order History"]
        order_history.append({"Item": item, "Quantity": quantity, "Date": order_date})
        self.customers.at[customer_index, "Order History"] = order_history
    
        st.write(f"Order for {item} (Quantity: {quantity}) placed successfully!")

    def view_orders(self):
        st.write("### Orders")
        if self.orders.empty:
            st.write("No orders available.")
        else:
        # Ensure 'Order Date' is formatted
            self.orders['Order Date'] = pd.to_datetime(self.orders['Order Date']).dt.strftime('%Y-%m-%d')
            st.dataframe(self.orders)


    def update_order_status(self, order_id, new_status):
        if order_id < 0 or order_id >= len(self.orders):
            st.write("Order not found.")
        else:
            st.session_state.orders.at[order_id, 'Status'] = new_status
            st.write(f"Order ID {order_id} status updated to {new_status}")

    def save_to_excel(self):
        self.orders.to_excel("new_orders.xlsx", index=False)
        st.write("Orders saved to Excel.")

    def customer_history(self, customer_name):
        if customer_name not in self.customers["Customer Name"].values:
            st.write(f"No order history found for {customer_name}.")
        else:
            customer_index = self.customers[self.customers["Customer Name"] == customer_name].index[0]
            st.write(self.customers.at[customer_index, "Order History"])

    def sales_analytics(self):
        # Sales Over Time: Total orders by date
        orders_by_date = self.orders.groupby('Order Date')['Quantity'].sum().reset_index()

        # Most Popular Items
        popular_items = self.orders.groupby('Item')['Quantity'].sum().reset_index().sort_values(by='Quantity', ascending=False)

        # Total Sales by Item
        total_sales = self.orders['Quantity'].sum()

        # Plot Sales Over Time
        st.write("### Sales Over Time (Quantity by Date)")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=orders_by_date, x='Order Date', y='Quantity', ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Plot Most Popular Items
        st.write("### Most Popular Items")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=popular_items, x='Item', y='Quantity', ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Display Total Sales
        st.write(f"### Total Sales: {total_sales} items sold.")

# Streamlit UI
st.title("Bakery Order Management System")
bakery = BakeryOrderManagement()

# Sidebar Navigation
option = st.sidebar.selectbox("Select an Option", ["Add Order", "View Orders", "Update Order Status", "Customer History", "Export to Excel", "Sales Analytics"])

if option == "Add Order":
    st.write("### Add New Order")
    customer_name = st.text_input("Customer Name")
    item = st.text_input("Item")  # User can input any item
    quantity = st.number_input("Quantity", min_value=1, max_value=100)
    order_date = st.date_input("Order Date", min_value=datetime.today())
    
    if st.button(f"Add Order for {item}"):
        bakery.add_order(customer_name, item, quantity, order_date)

elif option == "View Orders":
    st.write("### All Orders")
    bakery.view_orders()

elif option == "Update Order Status":
    st.write("### Update Order Status")
    order_id = st.number_input("Enter Order ID", min_value=0)
    new_status = st.selectbox("Select Status", ["Pending", "In Progress", "Completed"])
    
    if st.button("Update Status"):
        bakery.update_order_status(order_id, new_status)

elif option == "Customer History":
    st.write("### View Customer Order History")
    customer_name = st.text_input("Enter Customer Name")
    
    if st.button("Show History"):
        bakery.customer_history(customer_name)

elif option == "Export to Excel":
    st.write("### Export Orders to Excel")
    if st.button("Export"):
        bakery.save_to_excel()

elif option == "Sales Analytics":
    st.write("### Sales Analytics")
    bakery.sales_analytics()

# Display Real-Time Orders
st.sidebar.write("### Real-Time Orders")
st.sidebar.write(f"Orders: {len(st.session_state.orders)}")
