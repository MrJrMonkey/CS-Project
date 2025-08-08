import mysql.connector
from datetime import datetime

# Connect to the MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # Replace with your MySQL username
        password="your_password",  # Replace with your MySQL password
        database="dental_clinic"
    )

# Add a new patient
def add_patient():
    conn = connect_db()
    cursor = conn.cursor()
    name = input("Enter patient's name: ")
    age = int(input("Enter patient's age: "))
    gender = input("Enter patient's gender (Male/Female/Other): ")
    contact_number = input("Enter patient's contact number: ")
    address = input("Enter patient's address: ")

    cursor.execute("""
        INSERT INTO patients (name, age, gender, contact_number, address)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, age, gender, contact_number, address))
    conn.commit()
    print("Patient added successfully!")
    conn.close()

# Add a new appointment
def add_appointment():
    conn = connect_db()
    cursor = conn.cursor()
    patient_id = int(input("Enter patient ID: "))
    appointment_date = input("Enter appointment date (YYYY-MM-DD): ")
    service = input("Enter service (e.g., Cleaning, Filling, Root Canal): ")

    cursor.execute("""
        INSERT INTO appointments (patient_id, appointment_date, service)
        VALUES (%s, %s, %s)
    """, (patient_id, appointment_date, service))
    conn.commit()
    print("Appointment added successfully!")
    conn.close()

# View all patients
def view_patients():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()

    print("\n=== Patient Records ===")
    print("ID | Name | Age | Gender | Contact | Address")
    print("-----------------------------------------------")
    for patient in patients:
        print(f"{patient[0]} | {patient[1]} | {patient[2]} | {patient[3]} | {patient[4]} | {patient[5]}")
    conn.close()

# View all appointments
def view_appointments():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.appointment_id, p.name, a.appointment_date, a.service
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
    """)
    appointments = cursor.fetchall()

    print("\n=== Appointments ===")
    print("ID | Patient Name | Date | Service")
    print("-------------------------------------")
    for appointment in appointments:
        print(f"{appointment[0]} | {appointment[1]} | {appointment[2]} | {appointment[3]}")
    conn.close()

# Update patient details
def update_patient():
    conn = connect_db()
    cursor = conn.cursor()
    patient_id = int(input("Enter patient ID to update: "))
    print("What do you want to update?")
    print("1. Name")
    print("2. Age")
    print("3. Gender")
    print("4. Contact Number")
    print("5. Address")
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        new_value = input("Enter new name: ")
        column = "name"
    elif choice == 2:
        new_value = int(input("Enter new age: "))
        column = "age"
    elif choice == 3:
        new_value = input("Enter new gender: ")
        column = "gender"
    elif choice == 4:
        new_value = input("Enter new contact number: ")
        column = "contact_number"
    elif choice == 5:
        new_value = input("Enter new address: ")
        column = "address"
    else:
        print("Invalid choice!")
        return
    
    cursor.execute(f"""
        UPDATE patients
        SET {column} = %s
        WHERE patient_id = %s
    """, (new_value, patient_id))
    conn.commit()
    print("Patient details updated successfully!")
    conn.close()

# Delete a patient record
def delete_patient():
    conn = connect_db()
    cursor = conn.cursor()
    patient_id = int(input("Enter patient ID to delete: "))
    cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
    conn.commit()
    print("Patient record deleted successfully!")
    conn.close()

# Main menu
def main():
    while True:
        print("\n=== Dental Management System ===")
        print("1. Add a New Patient")
        print("2. Add a New Appointment")
        print("3. View All Patients")
        print("4. View All Appointments")
        print("5. Update Patient Details")
        print("6. Delete Patient Record")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_patient()
        elif choice == '2':
            add_appointment()
        elif choice == '3':
            view_patients()
        elif choice == '4':
            view_appointments()
        elif choice == '5':
            update_patient()
        elif choice == '6':
            delete_patient()
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()