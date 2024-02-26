import mysql.connector

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="lab9"
)
db_cursor = db_connection.cursor()

# Function to search current contact information by last name
def search_by_last_name(last_name):
    query = "SELECT * FROM people_master JOIN people_address ON people_master.person_id = people_address.person_id JOIN addresses ON people_address.address_id = addresses.address_id WHERE SUBSTRING_INDEX(person_name, ' ', -1) = %s AND end_date IS NULL"
    db_cursor.execute(query, (last_name,))
    result = db_cursor.fetchall()
    if result:
        print('============================================')
        print("Contact Information for", last_name)
        for row in result:
            print("Name:", row[1])
            print("Date of Birth:", row[2])
            print("Phone Number:", row[3])
            print("Address:", row[6], row[7], row[8], row[9])
    else:
        print('============================================')
        print("No contact found with last name", last_name)

# Function to search current contact information by prefix
def search_by_prefix(prefix):
    query = "SELECT * FROM people_master JOIN people_address ON people_master.person_id = people_address.person_id JOIN addresses ON people_address.address_id = addresses.address_id WHERE person_name LIKE %s AND end_date IS NULL"
    db_cursor.execute(query, (prefix + '%',))
    result = db_cursor.fetchall()
    if result:
        print('============================================')
        print("Contact Information with Name Prefix", prefix)
        for row in result:
            print("Name:", row[1])
            print("Date of Birth:", row[2])
            print("Phone Number:", row[3])
            print("Address:", row[6], row[7], row[8], row[9])
    else:
        print('============================================')
        print("No contact found with name prefix", prefix)

# Function to create a new contact
def create_new_contact(name, dob, phone_number, street_address, city, state, zip_code):
    # Check if contact name already exists
    query = "SELECT person_id, active_phone_number FROM people_master WHERE person_name = %s"
    db_cursor.execute(query, (name,))
    result = db_cursor.fetchone()
    if result:
        # Update existing contact
        person_id = result[0]
        existing_phone_number = result[1]
        if existing_phone_number != phone_number:
            query = "UPDATE people_master SET active_phone_number = %s,person_DOB=%s WHERE person_id = %s"
            db_cursor.execute(query, (phone_number,dob, person_id))
        query = "UPDATE people_address SET end_date = CURRENT_DATE() WHERE person_id = %s AND end_date IS NULL"
        db_cursor.execute(query, (person_id,))
    else:
        # Create new contact
        query = "INSERT INTO people_master (person_name, person_DOB, active_phone_number) VALUES (%s, %s, %s)"
        db_cursor.execute(query, (name, dob, phone_number))
        person_id = db_cursor.lastrowid
    # Insert new address
    query = "INSERT INTO addresses (street_address, city, state, zip_code) VALUES (%s, %s, %s, %s)"
    db_cursor.execute(query, (street_address, city, state, zip_code))
    address_id = db_cursor.lastrowid
    # Associate address with the contact
    query = "INSERT INTO people_address (person_id, address_id, start_date) VALUES (%s, %s, CURRENT_DATE())"
    db_cursor.execute(query, (person_id, address_id))
    # Commit changes
    db_connection.commit()
    if result:
        print("Contact updated successfully")
    else:
        print("Contact created successfully")

# Function to search active contact information by age range
def search_by_age_range(min_age, max_age):
    query = "SELECT * FROM people_master JOIN people_address ON people_master.person_id = people_address.person_id JOIN addresses ON people_address.address_id = addresses.address_id WHERE TIMESTAMPDIFF(YEAR, person_DOB, CURDATE()) BETWEEN %s AND %s AND end_date IS NULL"
    db_cursor.execute(query, (min_age, max_age))
    result = db_cursor.fetchall()
    if result:
        print("Contact Information for Age Range", min_age, "-", max_age)
        for row in result:
            print("Name:", row[1])
            print("Date of Birth:", row[2])
            print("Phone Number:", row[3])
            print("Address:", row[6], row[7], row[8], row[9])
    else:
        print("No contacts found in the age range", min_age, "-", max_age)

# Main program loop
while True:
    print("\nAddress Book Tool Menu:")
    print("1. Search by Last Name")
    print("2. Search by Prefix")
    print("3. Create New Contact")
    print("4. Search by Age Range")
    print("5. Quit")

    choice = input("Enter your choice: ")

    if choice == '1':
        last_name = input("Enter last name: ")
        search_by_last_name(last_name)
    elif choice == '2':
        prefix = input("Enter name prefix: ")
        search_by_prefix(prefix)
    elif choice == '3':
        name = input("Enter name: ")
        dob = input("Enter date of birth (YYYY-MM-DD): ")
        phone_number = input("Enter phone number: ")
        street_address = input("Enter street address: ")
        city = input("Enter city: ")
        state = input("Enter state: ")
        zip_code = input("Enter zip code: ")
        create_new_contact(name, dob, phone_number, street_address, city, state, zip_code)
    elif choice == '4':
        min_age = int(input("Enter minimum age: "))
        max_age = int(input("Enter maximum age: "))
        search_by_age_range(min_age, max_age)
    elif choice == '5':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please enter a number from 1 to 5.")
