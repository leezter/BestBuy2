from products import Product
from store import Store


def start(store):
    """ 
    Runs the main user interface loop for the store system.

    Displays a menu with options to:
    1. List all products currently available in the store
    2. Show the total quantity of all products
    3. Make an order by selecting products and quantities
    4. Exit the program

    Handles user input, displays relevant store data,
    and manages edge cases such as invalid input or stock issues.
    """

    while True:
        print("\nStore Menu")
        print("----------")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        choice = input("Please choose a number: ")

        if choice == "1":
            print("------")
            for index, product in enumerate(store.get_all_products(), start=1):
                print(f"{index}. {product.show()}")
            print("------")

        elif choice == "2":
            total = store.get_total_quantity()
            print(f"Total of {total} items in store")

        elif choice == "3":
            print("------")
            active_products = store.get_all_products()
            for index, product in enumerate(active_products, start=1):
                print(f"{index}. {product.show()}")
            print("------")

            order_list = []

            while True:
                user_input = input("Which product # do you want? ")
                if user_input.strip() == "":
                    break

                try:
                    product_index = int(user_input) - 1
                    if product_index < 0 or product_index >= len(active_products):
                        print("Error adding product!")
                        continue

                    quantity_str = input("What amount do you want? ")
                    quantity = int(quantity_str)

                    product = active_products[product_index]
                    if quantity <= 0 or quantity > product.get_quantity():
                        print("Error while making order! Quantity larger than what exists")
                        continue

                    order_list.append((product, quantity))
                    print("Product added to list!")

                except ValueError:
                    print("Error adding product!")

            try:
                total_price = store.order(order_list)
                print("********")
                print(f"Order made! Total payment: ${total_price}")
            except Exception as e:
                print(f"Error while making order: {e}")

        elif choice == "4":
            break

        else:
            print("Error with your choice! Try again!")


def main():
    """ setup initial stock of inventory. """
    product_list = [ 
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250)
    ]
    best_buy = Store(product_list)
    start(best_buy)

if __name__  == "__main__":
    main()