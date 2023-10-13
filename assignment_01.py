import uuid
import json

# Load existing user data from a JSON file
def load_user_data():
    try:
        with open('user_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save user data to a JSON file
def save_user_data(data):
    with open('user_data.json', 'w') as file:
        json.dump(data, file, indent=4)


# Function to get or generate UUID based on email or phone number
def get_or_generate_uuid(user_data, email, phone):
    for uuid_str, user_info in user_data.items():
        if user_info['email'] == email or user_info['phone'] == phone:
            return uuid_str

    # If user is not recognized, generate a new UUID
    new_uuid = str(uuid.uuid4())
    user_data[new_uuid] = {'email': email, 'phone': phone}
    save_user_data(user_data)
    return new_uuid
import uuid

def generate_v4_uuid():
    return str(uuid.uuid4())

# Example usage:
uuid_v4 = generate_v4_uuid()
print(uuid_v4)

# Main function
def main():
    user_data = load_user_data()

    while True:
        choice = input("Enter '1' to identify a user or '2' to quit: ")

        if choice == '1':
            email = input("Enter the user's email: ")
            phone = input("Enter the user's phone number: ")

            user_uuid = get_or_generate_uuid(user_data, email, phone)
            print(f"User UUID: {user_uuid}")
        elif choice == '2':
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == '__main__':
    main()
