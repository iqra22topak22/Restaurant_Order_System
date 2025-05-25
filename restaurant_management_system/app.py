# Define MenuItem class
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
        return f"{self.name} - ${self.price} (Stock: {self.stock})"


# Define Customer class
class Customer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Customer: {self.name}"


# Define Order class
class Order:
    def __init__(self, customer):
        self.customer = customer
        self.items = []

    def add_item(self, menu_item, quantity):
        if menu_item.is_available(quantity):
            self.items.append((menu_item, quantity))
            menu_item.update_stock(quantity)
        else:
            print(f"Sorry, not enough stock for {menu_item.name}.")

    def generate_bill(self):
        total = 0
        print(f"\nOrder for {self.customer.name}:")
        for item, qty in self.items:
            subtotal = item.price * qty
            total += subtotal
            print(f"{item.name} x {qty} = ${subtotal:.2f}")
        print(f"Total Bill: ${total:.2f}")
        return total


# Define Payment class
class Payment:
    def __init__(self, amount, method="Cash"):
        self.amount = amount
        self.method = method

    def process_payment(self):
        print(f"Payment of ${self.amount:.2f} received via {self.method}.")


# Sample inventory and order process
def main():
    # Inventory
    menu = [
        MenuItem("Burger", 5.99, 10),
        MenuItem("Pizza", 8.99, 5),
        MenuItem("Fries", 2.99, 20),
        MenuItem("Coke", 1.50, 15)
    ]

    # Show Menu
    print("Menu:")
    for item in menu:
        print(item)

    # Customer places an order
    customer_name = input("\nEnter customer name: ")
    customer = Customer(customer_name)
    order = Order(customer)

    # Ordering loop
    while True:
        item_name = input("\nEnter item to order (or 'done' to finish): ").title()
        if item_name.lower() == 'done':
            break

        # Find the item in menu
        menu_item = next((item for item in menu if item.name == item_name), None)
        if not menu_item:
            print("Item not found in the menu.")
            continue

        try:
            quantity = int(input(f"Enter quantity of {item_name}: "))
            order.add_item(menu_item, quantity)
        except ValueError:
            print("Invalid quantity. Please enter a number.")

    # Generate bill
    total_amount = order.generate_bill()

    # Payment
    payment_method = input("\nEnter payment method (Cash/Credit Card/Other): ")
    payment = Payment(total_amount, method=payment_method)
    payment.process_payment()


if __name__ == "__main__":
    main()
