import streamlit as st
from datetime import datetime

# Define classes (MenuItem, Customer, Order, Payment, MenuManager)
class MenuItem:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def is_available(self, quantity):
        return self.stock >= quantity

    def update_stock(self, quantity):
        if self.is_available(quantity):
            self.stock -= quantity
        else:
            raise ValueError(f"Not enough {self.name} in stock.")

    def __str__(self):
        return f"{self.name} - ${self.price:.2f} (Stock: {self.stock})"

class Customer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Customer: {self.name}"

class Order:
    def __init__(self, customer):
        self.customer = customer
        self.items = []  # List of tuples: (MenuItem, quantity)
        self.order_time = datetime.now()

    def add_item(self, menu_item, quantity):
        if menu_item.is_available(quantity):
            self.items.append((menu_item, quantity))
            menu_item.update_stock(quantity)
            return f"{quantity} x {menu_item.name} added to the order."
        else:
            return f"❌ Not enough stock for {menu_item.name}."

    def cancel_item(self, item_name):
        for i, (item, qty) in enumerate(self.items):
            if item.name.lower() == item_name.lower():
                item.stock += qty
                del self.items[i]
                return f"❌ {item.name} x {qty} has been cancelled and stock updated."
        return f"❌ No item named '{item_name}' found in the order."

    def generate_bill(self):
        total = 0
        bill = f"🧾 Order for {self.customer.name}\n"
        bill += f"🕒 Order Time: {self.order_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        if not self.items:
            bill += "No items in the order.\n"
        for item, qty in self.items:
            subtotal = item.price * qty
            total += subtotal
            bill += f"{item.name} x {qty} = ${subtotal:.2f}\n"
        bill += f"\n💰 Total Bill: ${total:.2f}"
        return bill, total

class Payment:
    def __init__(self, amount, method="Cash"):
        self.amount = amount
        self.method = method

    def process_payment(self):
        return f"✅ Payment of ${self.amount:.2f} received via {self.method}."

class MenuManager:
    def __init__(self, menu_list):
        self.menu = menu_list

    def show_menu(self):
        return [str(item) for item in self.menu]

    def find_item(self, name):
        for item in self.menu:
            if item.name.lower() == name.lower():
                return item
        return None

# Initialize menu_manager once
if "menu_manager" not in st.session_state:
    menu_items = [
        MenuItem("Burger", 5.99, 10),
        MenuItem("Pizza", 8.99, 5),
        MenuItem("Fries", 2.99, 20),
        MenuItem("Coke", 1.50, 15)
    ]
    st.session_state.menu_manager = MenuManager(menu_items)

menu_manager = st.session_state.menu_manager

# Input for dynamic customer name
customer_name = st.text_input("Enter customer name:", value=st.session_state.get("customer_name", "Ali"))

# If customer name changed, create new Customer and Order
if customer_name != st.session_state.get("customer_name", ""):
    st.session_state.customer_name = customer_name
    st.session_state.customer = Customer(customer_name)
    st.session_state.order = Order(st.session_state.customer)
    if "total" in st.session_state:
        del st.session_state.total  # reset total on new order

customer = st.session_state.customer
order = st.session_state.order

# App Title
st.title("🍽️ Restaurant Order System")

# Show current customer
st.markdown(f"**Current Customer:** {customer.name}")

# Show Menu
st.subheader("📋 Menu")
for item in menu_manager.show_menu():
    st.write(item)

# Add Multiple Items to Order
st.subheader("➕ Add Multiple Items to Order")
item_names = [item.name for item in menu_manager.menu]
selected_items = st.multiselect("Select items to add", item_names)

item_quantities = {}
for item_name in selected_items:
    qty = st.number_input(f"Quantity for {item_name}", min_value=1, max_value=20, value=1, step=1, key=f"qty_{item_name}")
    item_quantities[item_name] = qty

if st.button("Add Selected Items"):
    for item_name, qty in item_quantities.items():
        item = menu_manager.find_item(item_name)
        message = order.add_item(item, qty)
        if "❌" in message:
            st.error(message)
        else:
            st.success(message)

# Cancel Item
st.subheader("❌ Cancel Item from Order")
cancel_name = st.text_input("Enter item name to cancel", key="cancel_input")
if st.button("Cancel Item"):
    cancel_msg = order.cancel_item(cancel_name)
    if "❌" in cancel_msg:
        st.error(cancel_msg)
    else:
        st.warning(cancel_msg)

# Show Bill
if st.button("🧾 Generate Bill"):
    bill, total = order.generate_bill()
    st.text(bill)
    st.session_state.total = total

# Process Payment
if "total" in st.session_state and st.session_state.total > 0:
    st.subheader("💳 Payment")
    method = st.selectbox("Select payment method", ["Cash", "Credit Card", "Mobile Payment"])
    if st.button("Pay Now"):
        payment = Payment(st.session_state.total, method=method)
        st.success(payment.process_payment())
        st.session_state.total = 0
