import mysql.connector
from faker import Faker
import random
import time

fake = Faker()

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root", # Update this
    database="fraud_engine"
)
cursor = db.cursor()

def insert_user():
    while True:
        try:
            sql = """INSERT INTO users (first_name, last_name, date_of_birth, email, phone_number) 
                     VALUES (%s, %s, %s, %s, %s)"""
            
            # Using standard fake.email() and fake.phone_number()
            val = (
                fake.first_name(), 
                fake.last_name(), 
                fake.date_of_birth(minimum_age=18, maximum_age=80), 
                fake.email(), 
                fake.phone_number()[:20]
            )
            
            cursor.execute(sql, val)
            return cursor.lastrowid
            
        except mysql.connector.errors.IntegrityError:
            # A duplicate email or phone was generated. 
            # The exception is caught, and the loop instantly retries with new fake data.
            continue
def insert_device():
    sql = "INSERT INTO devices (ip_address, device_fingerprint) VALUES (%s, %s)"
    val = (fake.ipv4(), fake.sha256())
    cursor.execute(sql, val)
    return cursor.lastrowid

def create_transaction(user_id, device_id, amount, status, payment_status):
    # Insert Order
    order_sql = "INSERT INTO orders (user_id, device_id, order_amount, order_status) VALUES (%s, %s, %s, %s)"
    cursor.execute(order_sql, (user_id, device_id, amount, status))
    order_id = cursor.lastrowid
    
    # Insert Payment
    pay_sql = """INSERT INTO payments (order_id, payment_method, card_last_four, payment_status) 
                 VALUES (%s, %s, %s, %s)"""
    card_last_four = str(random.randint(1000, 9999))
    cursor.execute(pay_sql, (order_id, 'credit_card', card_last_four, payment_status))
    db.commit()

def normal_traffic():
    user_id = insert_user()
    device_id = insert_device()
    create_transaction(user_id, device_id, round(random.uniform(10.0, 150.0), 2), 'completed', 'success')
    print(f"[NORMAL] Processed legitimate order for User {user_id}")

def fraud_attack():
    user_id = insert_user()
    device_id = insert_device()
    print(f"[WARNING] Card testing attack initiated from Device {device_id} (IP: {fake.ipv4()})")
    
    # Fraudster attempts 5 rapid transactions with different cards
    for _ in range(5):
        create_transaction(user_id, device_id, round(random.uniform(500.0, 2000.0), 2), 'pending', 'failed')
        time.sleep(0.2)

if __name__ == "__main__":
    print("Starting Ingestion Engine... Press Ctrl+C to stop.")
    try:
        while True:
            if random.random() < 0.85:
                normal_traffic()
            else:
                fraud_attack()
            time.sleep(random.uniform(0.05, 0.15))
    except KeyboardInterrupt:
        print("\nIngestion stopped.")
        cursor.close()
        db.close()