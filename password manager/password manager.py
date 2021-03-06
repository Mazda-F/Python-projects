from cryptography.fernet import Fernet
import sqlite3
import getpass
import string
import random
import pyperclip

master_password = '12345'


# Connects to database file (creates data.db if there isnt one)
conn = sqlite3.connect('data.db')

c = conn.cursor()

#Creates table if there isnt one
try:
    c.execute("""CREATE TABLE data (
                app text,
                username text,
                password text,
                key text            
                )""")
except:
    pass


# Login and master password
def login():
    for i in range (3):
        master_password_input = getpass.getpass('Password: ')
        if master_password_input == master_password:
            print('')
            menu()
        else:
            print('Incorrect password.\n')

    quit()


# Main menu of the program
def menu():
    print('--------MENU--------\n' + '--------------------')
    print('1. Add password')
    print('2. Retrieve password')
    print('3. Remove password')
    print('4. Exit')

    menu_choice = input('\nChoice: ').strip()
     
    if menu_choice == '1':
        add()
    elif menu_choice == '2':
        retrieve()
    elif menu_choice == '3':
        remove()
    elif menu_choice == '4':
        conn.close()
        quit()    
    else:
        print('Invalid input, please try again.\n')
        menu()


# Generates a password
def generate():
    generated_password = ''

    for i in range(20):
        x = random.randint(0, 92)
        generated_password += string.printable[x]

    return generated_password

# Adds new row of data
def add():
    print ('\n--------------------')

    # Gets user info
    app_name = input('\nEnter the URL or app name: ')
    username = input('Enter your username or email: ')
    print('\n1. Enter your own password\n2. Generate a password (more secure)')
    add_choice = input('Choice: ').strip()

    # Password as input or generate password, add to clipboard
    if add_choice == '1':
        password = input('Enter your password: ')
        pyperclip.copy(password)

        # Encrypt and convert password into bytes
        key = Fernet.generate_key()
        crypter = Fernet(key)
        password = password.encode('utf-8')
        password = crypter.encrypt(password)

    elif add_choice == '2':
        password = generate()
        pyperclip.copy(password)

        # Encrypt and convert password into bytes
        key = Fernet.generate_key()
        crypter = Fernet(key)
        password = password.encode('utf-8')
        password = crypter.encrypt(password)

    else:
        print('Invalid input, please try again.\n')
        add()

    # Insert info as a row in Database's table
    with conn:
        c.execute("INSERT INTO data VALUES (?, ?, ?, ?)", (app_name, username, password, key))

    print('\nYour password has been created and copied to your clipboard.')
    print('')
    menu()


# Retrieve all passwords with the selected app_name
def retrieve():
    print ('\n--------------------')
    
    app_name = input('\nEnter the URL or app name: ')
    print('')

    c.execute("SELECT * FROM data WHERE app = (?) ", (app_name,)) 
    retrieved = c.fetchall()

    for row in retrieved:
        key = row[3]
        password = row[2]        
        crypter = Fernet(key)
        decrypted_password = crypter.decrypt(password)
        decrypted_password = str(decrypted_password, 'utf-8')
        print('App:', row[0], '-- Username/Email:', row[1], '-- Password:', decrypted_password)

    print('')
    menu()



def remove():
    print ('\n--------------------')

    app_name = input('\nEnter the URL or app name: ')
    print('')

    with conn:
        c.execute("DELETE from data WHERE app = (?)", (app_name,))

    print('')
    menu()


login()