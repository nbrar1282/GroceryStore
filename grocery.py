def get_products():
    import csv
    print("Get the list of products from store.csv")
    with open("store.csv", "r") as fp:
        reader = csv.DictReader(fp)
        print(reader)
        products = {}
        for product_dict in reader:
            name = product_dict["product"]
            print(name)
            price = float(product_dict["price"])
            print(price)
            qty = float(product_dict["quantity"])
            products[name] = {"price": price, "quantity": qty}
        return products

get_products()


def view_store_inventory():
    
    print("Use get_products to print the store inventory")
    store = get_products()
    for product, info in store.items():
        print(f"{product}: {info['quantity']} available, ${info['price']} each")
   


def view_all_pending_orders():
    from pathlib import Path
    p=Path("orders/pending")
    for element in p.iterdir():
        print(element)
    print("List all pending orders")
    




def view_pending_order(order_file):
    print("Print information about", order_file)

    # Get store information
    store = get_products()

    # Read the order file
    with open(f"orders/pending/{order_file}", "r") as fp:
        lines = fp.readlines()
        new_orders=[]
        new_orders1=[]
        items = []
        total = 0
        for line in lines:
            order_lines=line.strip().split()
            order_lines2= [line.strip()]
            new_orders.append(order_lines)
            new_orders1.append(order_lines2)
            
        # Parse the order information
        name = new_orders1[0][0]
        address = '        '+new_orders1[1][0]
        address1 = '        '+new_orders1[2][0]

        for element in new_orders[3:]:
                item_name= element[:-1]
                item_name1= ' '.join(item_name)
                item_qty = float(element[-1])
                item_price= store[item_name1]["price"]
                item_total = float(item_qty) * float(item_price)
                item_total = round(item_total, 2)
                total += item_total
                items.append((item_qty, item_name1, item_total))
        # print(items)
        # print(order_lines)
        # print(new_orders)
        
    
        # Print the order information
        print(f"Order for: {name}")
        print(f"{address}\n{address1}")
        print("--- PRODUCT LIST ---")
        for item in items:
            print(f"{item[0]} x {item[1]} = ${item[2]}")
        print(f"--- TOTAL = ${round(total, 2)} ---")





 
def save_products(items):
    import csv

    with open("store.csv", "w") as fp:
        writer = csv.writer(fp)
        writer.writerow(["product", "price", "quantity"])
        for item in items.items():
            writer.writerow([item[0], item[1]["price"], item[1]["quantity"]])

            




import pathlib

def process_pending_order(order_file):
    import csv
    # 1. Read from the file
    store = get_products()
    order_items = []
    store_items=[]

    with open(f"orders/pending/{order_file}", "r") as fp:
        lines = fp.readlines()
        
        for line in lines[:3]:
            order_lines2= f'{line.strip()}\n' 
            store_items.append(order_lines2)
       
        
        # 2. Add the subtotal for each item to the grocery list
        total =0
        
        out_of_stock = []
        
        for line in lines[3:]:
            item_name, item_qty = line.strip().rsplit(' ', 1)
            item_qty= float(item_qty)
            store_qty = float(store[item_name]["quantity"])
            if store_qty >= item_qty:
                item_price = store[item_name]["price"]
                item_total = float(item_qty) * float(item_price)
                total += item_total
                order_items.append((item_name, float(item_qty), item_total))
                line = line.strip() + f' {round(item_total, 2)}\n'
                store_items.append(line)
            elif store_qty < item_qty:
                if store_qty > 0 :
                    item_price = store[item_name]["price"]
                    item_total = float(store_qty) * float(item_price)
                    total += item_total
                    order_items.append((item_name, float(store_qty), item_total))
                    line = line.strip() + f' {round(item_total, 2)}\n'
                    store_items.append(line)
                    print(f' !!!!!Order Adjusted for {item_name} as there are only {store_qty}s available instead of {item_qty}!!!!')
                else:
                    item_price = store[item_name]["price"]
                    item_total = 0.00
                    total += item_total
                    order_items.append((item_name, 0.00, item_total))
                    line = line.strip() + f' {round(item_total,2)}\n'
                    store_items.append(line)
                    out_of_stock.append((item_name, item_price))
                    print(f'!!!!!!!!!Sorry no stock is there for {item_name}!!!!!!!!!!!')


        

        
        with open(f"orders/pending/{order_file}", "w") as f:
               for line in store_items: 
                f.writelines(line)

       # 3. Add the total amount for the order at the bottom of the file         
        with open(f"orders/pending/{order_file}", "a") as fd:
            fd.writelines(f'!!Total amount is ${round(total, 2)}!!!')         
           

        
       
    # 4. Update the store.csv file to reflect the new store inventory
    for item in order_items:
        store_qty = float(store[item[0]]["quantity"])
        item_qty = float(item[1])
        store[item[0]]["quantity"] -= item_qty
        
    save_products(store)
       
               

    # with open("store.csv", "w") as fp:
    #     writer = csv.writer(fp)
    #     writer.writerow(["product", "price", "quantity"])
    #     for item in store.items():
    #         writer.writerow([item[0], item[1]["price"], item[1]["quantity"]])

    # 5. Move the order file from the pending folder to the completed folder
    pending_order_path = pathlib.Path("orders/pending") / order_file
    completed_order_path = pathlib.Path("orders/completed") / order_file
    if not pathlib.Path("orders/completed").exists():
        pathlib.Path("orders/completed").mkdir()
    pending_order_path.rename(completed_order_path)


    

    


def view_out_of_stock():
    print('out of  stock')
    import csv
    out_of_stock = []
    with open("store.csv", "r") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            if float(row["quantity"]) == 0:
                out_of_stock.append(row["product"])
    if len(out_of_stock) > 0:
        print("The following items are out of stock:")
        for item in out_of_stock:
            print(f"- {item}")
    else:
        print("No items are currently out of stock.")
    

    




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
        if user_choice in ("0", "1", "2", "3", "4"):
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

