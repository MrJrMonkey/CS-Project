from datetime import datetime
import mysql.connector as ms
from tabulate import tabulate



db = ms.connect(host="localhost", user="jrmonkey", passwd="120418", database="stocks")
cursor = db.cursor()

def display_items():
    cursor.execute("SELECT * FROM Items")
    res = cursor.fetchall()

    header = ["Prod_ID", "Prod_Name", "num_of_items", "MRP"]
    table = [[i[0], i[1], i[2], f"₹{i[3]}"] for i in res]

    print(tabulate(table, headers=header, tablefmt="grid"))

display_items()



def display_items1():
    cursor.execute("SELECT * FROM Items")
    res = cursor.fetchall()

    print(f"{'Prod_ID'.ljust(10)} | {'Prod_Name'.ljust(25)} | {'num_of_items'.ljust(15)} | {'MRP'.ljust(10)}")
    print("=" * 70)  

    for i in res:
        print(f"{str(i[0]).ljust(10)} | {i[1].ljust(25)} | {str(i[2]).ljust(15)} | ₹{str(i[3]).ljust(10)}")
display_items1()

def getData():
    try:
        cursor.execute("SELECT * FROM Items")
        res = cursor.fetchall()
        print("\n")
        print("Prod_ID | Prod_Name | num_of_items | MRP")
        for i in res:
            print(i[0], ":", i[1], ":", i[2], ":", "₹", i[3])
        print("\nSuccessfully fetched data\n")

    except Exception as ex:
        print(f"Error: {ex}")

def addData():
    id = input("Enter ID of Product: ")
    name = input("Enter Name of Product: ")
    num = input("Enter Number of Products: ")
    mrp = float(input("Enter Price of Product: "))
    qu = f"INSERT INTO Items VALUES ({id},'{name}',{num},{mrp:.2f})"
    cursor.execute(qu)
    db.commit()
    print("\n\tData Added Successfully\n")

def updateData():
    print("Prod_ID | Prod_Name | num_of_items | MRP\n")
    try:
        q1 = input("Enter the column name to change: ")
        q2 = input("Enter the data to change: ")
        q3 = input("Enter the column name for Where Clause: ")
        q4 = input("Enter the data for identification for Where Clause: ")

        up = f"UPDATE Items SET {q1} = %s WHERE {q3} = %s"
        cursor.execute(up, (q2, q4))
        db.commit()

        print("\n\tData Updated Successfully\n")
    
    except Exception as ex:
        print(ex)

def deleteData():
    pid = int(input("Enter Product ID to Remove: "))
    qry = f"DELETE FROM Items WHERE Prod_ID = {pid}"
    cursor.execute(qry)
    print("Data Removed Successfully\n")
    db.commit()

def addStocks():
    cursor.execute("SELECT * FROM Items")
    res = cursor.fetchall()
    print("\nProd_ID | Prod_Name | num_of_items | MRP")
    for i in res:
        print(i[0], ":", i[1], ":", i[2], ":", "₹", i[3])
    try:
        print("\n")
        qq2 = int(input("Enter the Product ID: "))
        qq1 = int(input("Enter the added stocks to change: "))
        
        cursor.execute("SELECT * FROM Items WHERE Prod_ID = %s", (qq2,))
        row = cursor.fetchone()  
        if row:
            print(f"Current stock for Prod_ID {qq2}: {row[2]}")
            
            new_stock = row[2] + qq1
            cursor.execute("UPDATE Items SET num_of_items = %s WHERE Prod_ID = %s", (new_stock, qq2))
            db.commit()
            print(f"Updated stock for Prod_ID {qq2}: {new_stock}")
        else:
            print(f"No product found with Prod_ID {qq2}")
    except Exception as ex:
        print(ex)

def generate_receipt(sales):
    total_mrp = 0
    receipt_lines = []

    # Header
    receipt_lines.append("=================================================================\n")
    receipt_lines.append("                         SALES RECEIPT                          \n")
    receipt_lines.append("=================================================================\n")
    receipt_lines.append(f"{'Prod_ID':<10} | {'Prod_Name':<20} | {'Qty':<5} | {'Price':<10} | {'Subtotal':<10}\n")
    receipt_lines.append("-----------------------------------------------------------------\n")

    for sale in sales:
        product_id, quantity_sold = sale
        cursor.execute("SELECT * FROM Items WHERE Prod_ID = %s", (product_id,))
        row = cursor.fetchone()

        if row:
            product_name = row[1]
            current_stock = row[2]
            price_per_unit = row[3]

            if current_stock >= quantity_sold:
                subtotal = price_per_unit * quantity_sold
                total_mrp += subtotal
                new_stock = current_stock - quantity_sold

                cursor.execute("UPDATE Items SET num_of_items = %s WHERE Prod_ID = %s", (new_stock, product_id))
                db.commit()

                # Format the line with fixed-width fields
                receipt_lines.append(f"{product_id:<10} | {product_name:<20} | {quantity_sold:<5} | ₹{price_per_unit:<9} | ₹{subtotal:<10}\n")
            else:
                receipt_lines.append(f"Insufficient stock for Prod_ID {product_id}.\n")
        else:
            receipt_lines.append(f"No product found with Prod_ID {product_id}.\n")

    receipt_lines.append("-----------------------------------------------------------------\n")
    receipt_lines.append(f"{'Total Amount:':<45} ₹{total_mrp}\n")
    receipt_lines.append("=================================================================\n")
    receipt_lines.append("                Thank you for shopping!                       \n")
    receipt_lines.append("                     Date: " + datetime.now().strftime('%Y-%m-%d') + "\n")
    receipt_lines.append("                     Time: " + datetime.now().strftime('%H:%M:%S') + "\n")
    receipt_lines.append("=================================================================\n")

    receipt = ''.join(receipt_lines)
    print(receipt)
    return receipt

def billSystem():
    sales = []
    try:
        while True:
            qq2 = int(input("Enter the Product ID (or 0 to finish): "))
            if qq2 == 0:
                break

            qq1 = int(input("Enter the quantity sold: "))
            sales.append((qq2, qq1))

        generate_receipt(sales)

    except Exception as ex:
        print(f"An error occurred: {ex}")
        print("Some problem occurred")
 
def main():
    while True:
        print("1.Make Bill")
        print("2.Get data form table")
        print("3.Update sold stocks from table")
        print("4.Add data to table")
        print("5.Change data from table")
        print("6.Remove data from table")
        print("0.Exit\n")

        ch = input("Enter Choice: ")
        if ch == "1":
            billSystem()
        elif ch == "2":
            display_items1()
        elif ch == "3":
            addStocks()
        elif ch == "4":
            addData()
        elif ch == "5":
            updateData()
        elif ch == "6":
            deleteData()
        elif ch == "0":
            break
        else:
            print("\n\tInvalid Choice\n")

if __name__ == "__main__":
    main()
