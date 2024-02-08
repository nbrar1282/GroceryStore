def get_products():
    print("Get the list of products from store.csv")


def view_store_inventory():
    print("Use get_products to print the store inventory")


def view_all_pending_orders():
    print("List all pending orders")


def view_pending_order(order_file):
    print("Print information about", order_file)


def save_products(store_data):
    print("Save product inventory to store.csv")


def process_pending_order(order_file):
    print("Process the order", order_file)


def view_out_of_stock():
    print("List all products that are out of stock (quantity < 0)")


def main():
    running = True
    while running:
        print("Choose below:")
        print("1. view all pending orders")
        print("2. view a pending order")
        print("3. process an order")
        print("4. view products out of stock")
        print("0. exit")
        user_choice = input("? ")
        if user_choice in ("0", "1", "2", "3"):
            running = False

    if user_choice == "1":
        view_all_pending_orders()

    elif user_choice == "2":
        order_number = input("Which order number would you like to view? ")
        filename = order_number + ".txt"
        view_pending_order(filename)

    elif user_choice == "3":
        order_number = input("Which order number would you like to process? ")
        filename = order_number + ".txt"
        process_pending_order(filename)
        view_store_inventory()

    elif user_choice == "4":
        view_out_of_stock()

    return user_choice


if __name__ == "__main__":
    again = True
    while again:
        user_choice = main()
        if user_choice == "0":
            again = False
