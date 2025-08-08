import mysql.connector

# Connect to the MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # Replace with your MySQL username
        password="your_password",  # Replace with your MySQL password
        database="parking_lot"
    )

# Add a vehicle to a parking slot
def park_vehicle(slot_id, vehicle_number, vehicle_type):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Check if slot is available
    cursor.execute("SELECT is_occupied FROM parking_slots WHERE slot_id = %s", (slot_id,))
    result = cursor.fetchone()
    if result and result[0] == 1:
        print(f"Slot {slot_id} is already occupied.")
    else:
        # Update the slot with vehicle details and mark as occupied
        cursor.execute('''
            INSERT INTO parking_slots (slot_id, vehicle_number, vehicle_type, is_occupied)
            VALUES (%s, %s, %s, 1) 
            ON DUPLICATE KEY UPDATE vehicle_number=%s, vehicle_type=%s, is_occupied=1
        ''', (slot_id, vehicle_number, vehicle_type, vehicle_number, vehicle_type))
        conn.commit()
        print(f"Vehicle {vehicle_number} parked in slot {slot_id}.")
    
    conn.close()

# Remove a vehicle from a parking slot
def remove_vehicle(slot_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Check if slot is occupied
    cursor.execute("SELECT is_occupied FROM parking_slots WHERE slot_id = %s", (slot_id,))
    result = cursor.fetchone()
    if result and result[0] == 0:
        print(f"Slot {slot_id} is already empty.")
    else:
        # Update the slot to mark it as unoccupied
        cursor.execute('''
            UPDATE parking_slots SET vehicle_number = NULL, vehicle_type = NULL, is_occupied = 0
            WHERE slot_id = %s
        ''', (slot_id,))
        conn.commit()
        print(f"Vehicle removed from slot {slot_id}.")

    conn.close()

# View all slots
def view_slots():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM parking_slots ORDER BY slot_id")
    slots = cursor.fetchall()
    print("Slot ID | Vehicle Number | Vehicle Type | Occupied")
    print("-------------------------------------------")
    for slot in slots:
        slot_id, vehicle_number, vehicle_type, is_occupied = slot
        occupied_status = "Yes" if is_occupied else "No"
        print(f"{slot_id} | {vehicle_number or 'N/A'} | {vehicle_type or 'N/A'} | {occupied_status}")
    
    conn.close()

# View specific slot details
def view_slot(slot_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM parking_slots WHERE slot_id = %s", (slot_id,))
    slot = cursor.fetchone()
    
    if slot:
        slot_id, vehicle_number, vehicle_type, is_occupied = slot
        occupied_status = "Yes" if is_occupied else "No"
        print(f"Slot ID: {slot_id}")
        print(f"Vehicle Number: {vehicle_number or 'N/A'}")
        print(f"Vehicle Type: {vehicle_type or 'N/A'}")
        print(f"Occupied: {occupied_status}")
    else:
        print(f"Slot {slot_id} does not exist.")

    conn.close()

def main():
    while True:
        print("\n=== Parking Slot Management System ===")
        print("1. Park a Vehicle")
        print("2. Remove a Vehicle")
        print("3. View All Slots")
        print("4. View Slot Details")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            slot_id = int(input("Enter slot ID: "))
            vehicle_number = input("Enter vehicle number: ")
            vehicle_type = input("Enter vehicle type (car/bike/etc.): ")
            park_vehicle(slot_id, vehicle_number, vehicle_type)

        elif choice == '2':
            slot_id = int(input("Enter slot ID to remove vehicle: "))
            remove_vehicle(slot_id)

        elif choice == '3':
            view_slots()

        elif choice == '4':
            slot_id = int(input("Enter slot ID to view details: "))
            view_slot(slot_id)

        elif choice == '5':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
