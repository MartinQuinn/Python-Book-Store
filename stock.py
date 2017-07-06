# Martin Quinn
# Small Stock program
# 06/07/2017

import sqlite3
import time
import datetime

conn = sqlite3.connect('bookshop.db')
c = conn.cursor()

def menu():
	print("press 1 : to add stock.")
	print("press 2 : to check stock. ")
	print("press 3 : to enter a reservation. ")
	print("press 4 : to view reservations. ")
	print("press q : to quit program. ")
	return input('What would you like to do?')

run = menu()

def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS stock(datestamp TEXT, book TEXT, author TEXT, Price FLOAT, quantity INTEGER)')
	c.execute('CREATE TABLE IF NOT EXISTS customers(datestamp TEXT, fullname TEXT, address TEXT, phoneNo TEXT)')
	c.execute('CREATE TABLE IF NOT EXISTS reservations(datestamp TEXT, customer TEXT, book TEXT, price FLOAT)')

def search_cx(person):
	c.execute("SELECT count() FROM customers WHERE fullname = (?)",(person,))
	data = c.fetchall()
	print(data)
	if data == [(0,)]:
		print("Customer not in database, please add customer")
		dynamic_cx()
		return 0
	else:
		return 0


def dynamic_cx():
	unix = time.time()
	date = str(datetime.datetime.fromtimestamp(unix).strftime('%d-%m-%Y %H:%M:%S'))
	name = input('Full name: ')
	address = input('Address: ')
	phone = input('Phone Number: ')

	c.execute("INSERT INTO customers (datestamp, fullname, address, phoneNo) VALUES (?,?,?,?)",
			  (date, name, address, phone))
	conn.commit()

def create_reservation(person, book):
	unix = time.time()
	date = str(datetime.datetime.fromtimestamp(unix).strftime('%d-%m-%Y %H:%M:%S'))

	c.execute("SELECT price FROM stock WHERE book = (?)", (book,))
	for row in c.fetchall():
		print(row[0])
		price =  row[0]
	c.execute("INSERT INTO reservations (datestamp, customer, book, price) VALUES (?,?,?,?)",
			  (date, person, book, price))
	conn.commit()

def addToStock():
	unix = time.time()
	date = str(datetime.datetime.fromtimestamp(unix).strftime('%d-%m-%Y %H:%M:%S'))
	book = input('Book name : ')
	author = input('Author : ')
	price = input('Price : ')
	quantity = input('Quantity : ')

	c.execute("INSERT INTO stock (datestamp, book, author, price, quantity) VALUES (?,?,?,?,?)",
			  (date, book, author, price, quantity))
	conn.commit()

def checkStock():
	c.execute("SELECT book, author, price, quantity FROM stock")
	data = c.fetchall()
	for row in data:
		print(row)

def query_stock(book):
	c.execute("SELECT * FROM stock WHERE book = (?) AND quantity > 0", (book,))
	data = c.fetchall()
	print(data)
	if data == [(0,)]:
		print("Book out of Stock")
		return 0
	else:
		return 1

def makeReservation():
	book = input('What book was reserved?')
	query_stock(book)
	if query_stock(book) == 1:
		c.execute("UPDATE stock SET quantity = quantity - 1 where book = (?)", (book,))
		person = input('Who reserved the book?')
		search_cx(person)
		create_reservation(person, book)
		print("{} reserved {}".format(person, book))
		conn.commit()
	else:
		print("{} is out of stock".format(book))
		menu()

def viewReservations():
	c.execute("SELECT datestamp, customer, book, price FROM reservations")
	data = c.fetchall()
	for row in data:
		print(row)

# create_table()

while True:
# to add stock #
	if run == '1':
		addToStock()
		run = menu()

# to check stock #
	elif run == '2':
		checkStock()
		run = menu()

# to enter a reservation #
	elif run == '3':
		makeReservation()
		run = menu()

# to view reservations #
	elif run == '4':
		viewReservations()
		run = menu()

	elif run == 'q':
		break

# any other input during the menu #
	else:
		print("not a valid selection, please choose again below")
		run = menu()

c.close()
conn.close()