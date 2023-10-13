import sqlite3
import uuid

# Create an SQLite database and a users table
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    uuid TEXT PRIMARY KEY,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL)''')
conn.commit()


# Function to get or generate UUID based on email or phone number
def get_or_generate_uuid(email, phone):
    cursor.execute("SELECT uuid FROM users WHERE email=? OR phone=?", (email, phone))
    existing_uuid = cursor.fetchone()

    if existing_uuid:
        return existing_uuid[0]
    else:
        new_uuid = str(uuid.uuid4())
        cursor.execute("INSERT INTO users (uuid, email, phone) VALUES (?, ?, ?)", (new_uuid, email, phone))
        conn.commit()
        return new_uuid


# Main function
def main():
    while True:
        choice = input("Enter '1' to identify a user or '2' to quit: ")

        if choice == '1':
            email = input("Enter the user's email: ")
            phone = input("Enter the user's phone number: ")

            user_uuid = get_or_generate_uuid(email, phone)
            print(f"User UUID: {user_uuid}")
        elif choice == '2':
            conn.close()
            break
        else:
            print("Invalid input. Please try again.")


from flask import Flask, request, jsonify
import sqlite3
import uuid

app = Flask(__name)

# Create a connection to the SQLite database
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()


create_table_sql = """
CREATE TABLE IF NOT EXISTS users (
    uuid TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    phone TEXT NOT NULL
)
"""
cursor.execute(create_table_sql)
conn.commit()


# Function to get or generate UUID based on email or phone number
def get_or_generate_uuid(email, phone):
    cursor.execute("SELECT uuid FROM users WHERE email=? OR phone=?", (email, phone))
    existing_uuid = cursor.fetchone()

    if existing_uuid:
        return existing_uuid[0]
    else:
        new_uuid = str(uuid.uuid4())
        cursor.execute("INSERT INTO users (uuid, email, phone) VALUES (?, ?, ?)", (new_uuid, email, phone))
        conn.commit()
        return new_uuid



@app.route('/user', methods=['POST'])
def create_or_get_user():
    data = request.json  # Expecting JSON data with 'email' and 'phone' fields

    if 'email' not in data or 'phone' not in data:
        return jsonify({'error': 'Email and phone number are required.'}), 400

    email = data['email']
    phone = data['phone']

    user_uuid = get_or_generate_uuid(email, phone)
    return jsonify({'uuid': user_uuid})


if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    main()