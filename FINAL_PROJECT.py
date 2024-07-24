import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Snehil@19",
    database="thriftster"
)


    
def OrderItems():
    try: 
        phNo=loginBuyer()
        cursor=mydb.cursor()
        cursor.execute("SELECT* FROM product")
        for row in cursor:
            if row[7] != 1:
                print(row)
        item_id=int(input("Enter the ID of the item you want to order: "))
        card_no=input("Enter your card number: ")
        cursor.execute("SELECT Price FROM Product WHERE Product_ID = %s", (item_id,)) 
        row = cursor.fetchone()
        cost=row[0]
        cursor.execute(f"INSERT INTO Payment (Phone_Number, Total_Cost, Card_Number) VALUES ({phNo}, {cost},{card_no})")
        cursor.execute(f"SELECT payment_ID FROM Payment WHERE Phone_Number={phNo} AND Card_Number={card_no}")
        row1=cursor.fetchone()
        payment_ID=row1[0]
        cursor.execute(f"INSERT INTO `order`(Order_date, Phone_Number, Total_Cost, Payment_ID) VALUES (CURDATE(), {phNo}, {cost}, {payment_ID});")
        cursor.execute(f"SELECT Order_ID FROM `order` WHERE payment_ID={payment_ID}")
        row2=cursor.fetchone()
        OrderID=row2[0]
        cursor.execute(f"INSERT INTO Order_info VALUES ({OrderID}, {item_id}) ")
        cursor.execute(f"UPDATE Product SET sold=1 WHERE Product_ID={item_id}")   
        mydb.commit()
    
    except mysql.connector.Error as e:
        mydb.rollback()
        print("Error has ocurred rolling back....")
        

    
    
def AddToCart():
    phNo=loginBuyer()
    cursor=mydb.cursor()
    cursor.execute("SELECT* FROM product")
    for row in cursor:
        if row[7] != 1:
            print(row)
    item_id=int(input("Enter the ID of the item you want to add to cart: "))
    cursor.execute(f"SELECT Cart_ID FROM Cart WHERE Phone_NUMBER='{phNo}'")
    row=cursor.fetchone()
    CartID=row[0]
    if CartID is None:
        print("Error! Please LOGIN")
        
    cursor.execute(f"INSERT INTO Cart_Info VALUES ({CartID},{item_id});")
    mydb.commit()
    
def CheckoutCart():
    cost=0;
    phNo=viewCart()
    cursor=mydb.cursor()
    cursor.execute(f"SELECT p.Product_ID, p.Product_Name, p.Price, p.Size, p.Gender, p.Category FROM Cart_Info ci JOIN Product p ON ci.Product_ID = p.Product_ID WHERE ci.Cart_ID = (SELECT Cart_ID FROM CART WHERE Phone_Number ={phNo});")
    for row in cursor:
        cost+=row[2]
    card_no=input("Enter your card number: ")
    cursor.execute(f"INSERT INTO Payment (Phone_Number, Total_Cost, Card_Number) VALUES ({phNo}, {cost},{card_no})")
    cursor.execute(f"SELECT payment_ID FROM Payment WHERE Phone_Number={phNo} AND Card_Number={card_no}")
    row1=cursor.fetchone()
    payment_ID=row1[0]
    cursor.execute(f"INSERT INTO `order`(Order_date, Phone_Number, Total_Cost, Payment_ID) VALUES (CURDATE(), {phNo}, {cost}, {payment_ID});")
    cursor.execute(f"SELECT Order_ID FROM `order` WHERE payment_ID={payment_ID}")
    row2=cursor.fetchone()
    OrderID=row2[0]
    cursor.execute(f"SELECT p.Product_ID, p.Product_Name, p.Price, p.Size, p.Gender, p.Category FROM Cart_Info ci JOIN Product p ON ci.Product_ID = p.Product_ID WHERE ci.Cart_ID = (SELECT Cart_ID FROM CART WHERE Phone_Number ={phNo});")
    for row in cursor:
        cursor.execute(f"INSERT INTO Order_info VALUES ({OrderID}, {row[0]}) ")
        cursor.execute(f"UPDATE Product SET sold=1 WHERE Product_ID={row[0]}")
    
    mydb.commit()
    
        
    
    
def viewCart():   
    phNo=loginBuyer()
    cursor=mydb.cursor()
    cursor.execute(f"SELECT p.Product_ID, p.Product_Name, p.Price, p.Size, p.Gender, p.Category FROM Cart_Info ci JOIN Product p ON ci.Product_ID = p.Product_ID WHERE ci.Cart_ID = (SELECT Cart_ID FROM CART WHERE Phone_Number ={phNo});")
    for row in cursor:
        print(row)
    return phNo;

def giveFeedback():
    phNo=input("Enter the number of the seller you want to give feedback to: ")
    feedback=input("Enter the feedback: ")
    rating=float(input("Enter the rating: "))
    cursor=mydb.cursor()
    cursor.execute(f"INSERT INTO Feedback(Phone_Number, Rating, Feedback) VALUES ({phNo},{rating},'{feedback}');")
    mydb.commit()

def AddtoWishlist():
    phNo=loginBuyer()
    cursor=mydb.cursor()
    cursor.execute("SELECT* FROM product")
    for row in cursor:
        if row[7] != 1:
            print(row)
    item_id=int(input("Enter the ID of the item you want to add to wishlist: "))
    cursor.execute(f"INSERT INTO Wishlist VALUES ('{phNo}',{item_id})")
    mydb.commit()
    
def viewListedItems():
    phNo=loginSeller()
    cursor=mydb.cursor()
    cursor.execute(f"SELECT* FROM product WHERE Phone_Number='{phNo}'")
    for row in cursor:
        print(row)

def listNewItem():
    phNo=loginSeller()
    cursor=mydb.cursor()
    price=float(input("Enter the price of the item: "))
    size=input("Enter the Size: ")
    gender=input("Enter the gender: ")
    Category=input("Enter the category: ")
    productName=input("Enter the name of the product: ")
    cursor.execute(f"INSERT INTO Product(Phone_Number, Price, Size, Gender, Category, Product_Name, sold) VALUES ('{phNo}', {price}, '{size}','{gender}','{Category}','{productName}', 0 ) ")
    mydb.commit()

def createLogin():
    cursor=mydb.cursor()
    phNo=input("Enter your phone Number: ")
    firstName=input("Enter your first Name: ")
    lastName=input("Enter your last Name: ")
    houseNo=int(input("Enter your house Number: "))
    colony=input("Enter your colony: ")
    city=input("Enter your city: ")
    date_string = input("Enter a date (YYYY-MM-DD): ")
    cursor.execute(f"INSERT INTO user VALUES ('{phNo}','{firstName}','{lastName}',{houseNo},'{colony}','{city}', '{date_string}',0)")
    mydb.commit()
    
def loginBuyer():
    phNo = input("Enter your phone Number: ")
    return phNo

def loginSeller():
    phNo = input("Enter your phone Number: ")
    return phNo

def loginBuyerMenu():
    print("1. Order Items")
    print("2. Add Items in Cart")
    print("3. Checkout from Cart")
    print("4. View Your Cart")
    print("5. Give feedback")
    print("6. Add to wishlist")

def loginSellerMenu():
    print("1. View Listed Items")
    print("2. List New Item")
    
    
def diplayMenu():
    print("1. Login as Buyer")
    print("2. Login as Seller")
    print("3. Create Login")
    print("4. Enter as Admin")
    print("5. Exit")
    
def main():
    while True:
        diplayMenu()
        choice = input("Enter your choice: ")
        if choice=='5':
            print("Thank you!")
            break
        if choice== '1':
            loginBuyerMenu()
            choice1 = input("Enter your choice: ")
            if choice1=='1':
                OrderItems()
            if choice1=='2':
                AddToCart()
            if choice1=='4':
                viewCart()
            if choice1=='3':
                CheckoutCart()
            if choice1=='5':
                giveFeedback()
            if choice1=='6':
                AddtoWishlist()
                
        if choice=='2':
            loginSellerMenu()
            choice2= input("Enter your choice: ")
            if choice2=='1':
                viewListedItems()
            if choice2== '2':
                listNewItem()
        
        if choice=='3':
            createLogin()
        
        if choice== '4':
            pw=input("Enter Password: ")
            if pw =='Snehil':
                print("1. Find users who haven't made any orders")
                print("2. Find users who aren't sellers ")
                print("3. Arrange the users in descending order according to the no. of orders they have")
                print("4. View all Users")
                print("5. View all products")
                choice = int(input("Enter your choice: "))
                cursor = mydb.cursor()
            if choice == 1:
                cursor.execute("SELECT u.First_Name, u.Last_Name FROM user u LEFT JOIN `Order` o ON u.Phone_Number = o.Phone_Number WHERE o.Order_ID IS NULL;")
                for rows in cursor:
                    print(rows)
            elif choice == 2:
                cursor.execute("SELECT u.Phone_Number, u.first_name FROM user AS u WHERE u.Phone_Number NOT IN(SELECT p.Phone_Number FROM Product AS p);")
                for rows in cursor:
                    print(rows)
            elif choice == 3:
                cursor.execute("SELECT u.Phone_Number, u.First_Name, u.Last_Name, COUNT(o.Order_ID) AS Order_Count FROM user u LEFT JOIN `Order` o ON u.Phone_Number = o.Phone_Number GROUP BY u.Phone_Number, u.First_Name, u.Last_Name ORDER BY Order_Count DESC;")
                for rows in cursor:
                    print(rows)
            elif choice == 4:
                cursor.execute("SELECT * FROM user")
                for rows in cursor:
                    print(rows)
            elif choice == 5:
                cursor.execute("SELECT* FROM product")
                for rows in cursor:
                    print(rows)
        
    
        
    
if __name__== '__main__':
    main()