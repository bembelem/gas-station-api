import psycopg2
import random
from datetime import datetime, timedelta
from faker import Faker
from database.database import get_postgres_settings

fake = Faker('ru_RU')
Faker.seed(42)  # Для воспроизводимости результатов

conn = psycopg2.connect(dsn=get_postgres_settings().psycopg_url)
cursor = conn.cursor()

# Helper function to insert data and return inserted IDs
def insert_data(table_name, data):
    inserted_ids = []

    for item in data:
        columns = ", ".join(k.lower() for k in item.keys())
        placeholders = ", ".join(["%s"] * len(item))

        sql = f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({placeholders})
            RETURNING id
        """

        cursor.execute(sql, list(item.values()))
        inserted_ids.append(cursor.fetchone()[0])

    conn.commit()
    return inserted_ids


# Generate random date within range
def random_date(start_date, end_date):
    time_delta = end_date - start_date
    random_days = random.randint(0, time_delta.days)
    return start_date + timedelta(days=random_days)


# Generate random datetime within range
def random_datetime(start_date, end_date):
    random_date_val = random_date(start_date, end_date)
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)
    return datetime(random_date_val.year, random_date_val.month, random_date_val.day,
                    random_hour, random_minute, random_second)
def seed():
    # 1. Insert fuel types
    fuel_types_data = [
        {"ID": 1, "Name": "Gasoline 92", "Price_Per_Unit": 0.85},
        {"ID": 2, "Name": "Gasoline 95", "Price_Per_Unit": 0.95},
        {"ID": 3, "Name": "Gasoline 98", "Price_Per_Unit": 1.05},
        {"ID": 4, "Name": "Diesel", "Price_Per_Unit": 0.80},
        {"ID": 5, "Name": "Premium Diesel", "Price_Per_Unit": 0.90}
    ]
    insert_data("fuel_types", fuel_types_data)
    print("Fuel types inserted.")

    # 2. Insert refineries
    refineries_data = [
        {"ID": 1, "Name": "North Refinery", "Address_Line": "123 Industrial Ave, North City"},
        {"ID": 2, "Name": "South Refinery", "Address_Line": "456 Production Blvd, South City"},
        {"ID": 3, "Name": "East Refinery", "Address_Line": "789 Factory Rd, East City"}
    ]
    insert_data("refineries", refineries_data)
    print("Refineries inserted.")

    # 3. Insert refinery tanks
    refinery_tanks_data = []
    for refinery_id in range(1, 4):
        for fuel_type_id in range(1, 6):
            capacity = random.uniform(500000, 1000000)
            current_volume = capacity * random.uniform(0.3, 0.9)
            refinery_tanks_data.append({
                "Refinery_ID": refinery_id,
                "Fuel_Type_ID": fuel_type_id,
                "Capacity": capacity,
                "Current_Volume": current_volume
            })
    refinery_tank_ids = insert_data("refinery_tanks", refinery_tanks_data)
    print("Refinery tanks inserted.")

    # 4. Insert stations
    stations_data = [
        {"ID": 1, "Name": "Downtown Station", "Address": "101 Main St, Downtown", "Contact_Number": "555-1001"},
        {"ID": 2, "Name": "Uptown Station", "Address": "202 High St, Uptown", "Contact_Number": "555-2002"},
        {"ID": 3, "Name": "Westside Station", "Address": "303 West Ave, Westside", "Contact_Number": "555-3003"},
        {"ID": 4, "Name": "Eastside Station", "Address": "404 East Blvd, Eastside", "Contact_Number": "555-4004"},
        {"ID": 5, "Name": "Northside Station", "Address": "505 North Rd, Northside", "Contact_Number": "555-5005"}
    ]
    insert_data("stations", stations_data)
    print("Stations inserted.")

    # 5. Insert station tanks
    station_tanks_data = []
    for station_id in range(1, 6):
        for fuel_type_id in range(1, 6):
            capacity = random.uniform(10000, 50000)
            current_volume = capacity * random.uniform(0.2, 0.8)
            station_tanks_data.append({
                "Station_ID": station_id,
                "Fuel_Type_ID": fuel_type_id,
                "Capacity": capacity,
                "Current_Volume": current_volume
            })
    station_tank_ids = insert_data("station_tanks", station_tanks_data)
    print("Station tanks inserted.")

    # 6. Insert providers
    providers_data = [
        {"ID": 1, "Name": "CreditCard Co.", "Details": "Credit card payment processor"},
        {"ID": 2, "Name": "MobilePayment Inc.", "Details": "Mobile payment solution"},
        {"ID": 3, "Name": "Cash Register Ltd.", "Details": "Cash handling services"}
    ]
    insert_data("providers", providers_data)
    print("Providers inserted.")

    # 7. Insert payment methods
    payment_methods_data = [
        {"ID": 1, "Name": "Credit Card", "Slug": "credit-card", "Type": "card", "Is_Active": True,
         "Requires_Authorization": True, "Provider_ID": 1},
        {"ID": 2, "Name": "Debit Card", "Slug": "debit-card", "Type": "card", "Is_Active": True,
         "Requires_Authorization": True, "Provider_ID": 1},
        {"ID": 3, "Name": "Mobile Payment", "Slug": "mobile-payment", "Type": "electronic", "Is_Active": True,
         "Requires_Authorization": True, "Provider_ID": 2},
        {"ID": 4, "Name": "Cash", "Slug": "cash", "Type": "physical", "Is_Active": True, "Requires_Authorization": False,
         "Provider_ID": 3},
        {"ID": 5, "Name": "Loyalty Points", "Slug": "loyalty-points", "Type": "loyalty", "Is_Active": True,
         "Requires_Authorization": True, "Provider_ID": None}
    ]
    insert_data("payment_methods", payment_methods_data)
    print("Payment methods inserted.")

    # 8. Insert sale transaction statuses
    sale_transaction_statuses_data = [
        {"ID": 1, "Name": "Pending"},
        {"ID": 2, "Name": "Authorized"},
        {"ID": 3, "Name": "Completed"},
        {"ID": 4, "Name": "Failed"},
        {"ID": 5, "Name": "Refunded"},
        {"ID": 6, "Name": "Cancelled"}
    ]
    insert_data("sale_transaction_statuses", sale_transaction_statuses_data)
    print("Sale transaction statuses inserted.")

    # 9. Insert client tiers
    client_tiers_data = [
        {"ID": 1, "Name": "Standard", "Description": "Standard customer tier"},
        {"ID": 2, "Name": "Silver", "Description": "Silver customer tier with small discounts"},
        {"ID": 3, "Name": "Gold", "Description": "Gold customer tier with medium discounts"},
        {"ID": 4, "Name": "Platinum", "Description": "Platinum customer tier with large discounts"}
    ]
    insert_data("client_tiers", client_tiers_data)
    print("Client tiers inserted.")

    # 10. Insert customers
    customers_data = []
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2024, 12, 31)

    for i in range(1, 21):
        registration_date = random_date(start_date, end_date)
        last_visit_date = random_date(registration_date, end_date) if random.random() > 0.1 else None

        customers_data.append({
            "Phone_Number": f"555-{1000 + i}",
            "Registration_Date": registration_date.strftime("%Y-%m-%d"),
            "Bonus_Points": random.randint(0, 10000),
            "Client_Tier_ID": random.randint(1, 4),
            "Total_Purchases": random.uniform(100, 50000),
            "Last_Visit_Date": last_visit_date.strftime("%Y-%m-%d") if last_visit_date else None
        })
    customer_ids = insert_data("customers", customers_data)
    print("Customers inserted.")

    # 11. Insert operator statuses
    operator_statuses_data = [
        {"ID": 1, "Name": "Active"},
        {"ID": 2, "Name": "Inactive"},
        {"ID": 3, "Name": "On Leave"},
        {"ID": 4, "Name": "Terminated"}
    ]
    insert_data("operator_statuses", operator_statuses_data)
    print("Operator statuses inserted.")

    # 12. Insert operator roles
    operator_roles_data = [
        {"ID": 1, "Name": "Station Manager", "Descryption": "Manages entire station operations"},
        {"ID": 2, "Name": "Cashier", "Descryption": "Processes payments and assists customers"},
        {"ID": 3, "Name": "Maintenance Staff", "Descryption": "Maintains equipment and facilities"},
        {"ID": 4, "Name": "Administrator", "Descryption": "System administrator"}
    ]
    insert_data("operator_roles", operator_roles_data)
    print("Operator roles inserted.")

    # 13. Insert operators
    operators_data = [
        {"ID": 1, "First_Name": "John", "Last_Name": "Smith", "Phone_Number": "555-1111", "Email": "john.smith@example.com",
         "Status_ID": 1, "Role_ID": 1, "Password_Hash": "hashed_password_1"},
        {"ID": 2, "First_Name": "Jane", "Last_Name": "Doe", "Phone_Number": "555-2222", "Email": "jane.doe@example.com",
         "Status_ID": 1, "Role_ID": 2, "Password_Hash": "hashed_password_2"},
        {"ID": 3, "First_Name": "Mike", "Last_Name": "Johnson", "Phone_Number": "555-3333",
         "Email": "mike.johnson@example.com", "Status_ID": 1, "Role_ID": 2, "Password_Hash": "hashed_password_3"},
        {"ID": 4, "First_Name": "Sarah", "Last_Name": "Brown", "Phone_Number": "555-4444",
         "Email": "sarah.brown@example.com", "Status_ID": 1, "Role_ID": 3, "Password_Hash": "hashed_password_4"},
        {"ID": 5, "First_Name": "David", "Last_Name": "Williams", "Phone_Number": "555-5555",
         "Email": "david.williams@example.com", "Status_ID": 1, "Role_ID": 4, "Password_Hash": "hashed_password_5"}
    ]
    insert_data("operators", operators_data)
    print("Operators inserted.")

    # 14. Insert refueling session statuses
    refueling_session_statuses_data = [
        {"ID": 1, "Name": "Pending"},
        {"ID": 2, "Name": "In Progress"},
        {"ID": 3, "Name": "Completed"},
        {"ID": 4, "Name": "Cancelled"},
        {"ID": 5, "Name": "Failed"}
    ]
    insert_data("refueling_session_statuses", refueling_session_statuses_data)
    print("Refueling session statuses inserted.")

    # 15. Insert fuel dispensers
    fuel_dispensers_data = []
    for station_id in range(1, 6):
        for dispenser_id in range(1, 5):  # 4 dispensers per station
            fuel_dispensers_data.append({
                "Station_ID": station_id,
                "Is_Active": True if random.random() > 0.1 else False
            })
    fuel_dispenser_ids = insert_data("fuel_dispensers", fuel_dispensers_data)
    print("Fuel dispensers inserted.")

    # 16. Insert fuel pumps
    fuel_pumps_data = []
    for i, dispenser_id in enumerate(fuel_dispenser_ids):
        # Each dispenser has multiple pumps for different fuel types
        for nozzle in range(1, 4):  # 3 nozzles per dispenser
            fuel_type_id = random.randint(1, 5)  # Random fuel type
            fuel_pumps_data.append({
                "Fuel_Type_ID": fuel_type_id,
                "Fuel_Dispenser_ID": dispenser_id,
                "Nozzle_Number": nozzle,
                "Is_Active": True if random.random() > 0.05 else False
            })
    fuel_pump_ids = insert_data("fuel_pumps", fuel_pumps_data)
    print("Fuel pumps inserted.")

    # 17. Insert production unit statuses
    production_unit_statuses_data = [
        {"ID": 1, "Name": "Operational"},
        {"ID": 2, "Name": "Maintenance"},
        {"ID": 3, "Name": "Shutdown"},
        {"ID": 4, "Name": "Standby"}
    ]
    insert_data("production_unit_statuses", production_unit_statuses_data)
    print("Production unit statuses inserted.")

    # 18. Insert production units
    production_units_data = []
    last_year = datetime.now() - timedelta(days=365)
    for refinery_id in range(1, 4):
        for unit_id in range(1, 4):  # 3 units per refinery
            production_units_data.append({
                "Refinery_ID": refinery_id,
                "Name": f"Unit {unit_id} - Refinery {refinery_id}",
                "Capacity_Per_Day": random.uniform(50000, 200000),
                "Last_Maintenance": random_date(last_year, datetime.now()).strftime("%Y-%m-%d"),
                "Status_ID": random.randint(1, 4)
            })
    production_unit_ids = insert_data("production_units", production_units_data)
    print("Production units inserted.")

    # 19. Insert order statuses
    order_statuses_data = [
        {"ID": 1, "Name": "Created"},
        {"ID": 2, "Name": "Processing"},
        {"ID": 3, "Name": "In Transit"},
        {"ID": 4, "Name": "Delivered"},
        {"ID": 5, "Name": "Cancelled"}
    ]
    insert_data("order_statuses", order_statuses_data)
    print("Order statuses inserted.")

    # 20. Insert batch statuses
    batch_statuses_data = [
        {"ID": 1, "Name": "Planned"},
        {"ID": 2, "Name": "In Progress"},
        {"ID": 3, "Name": "Completed"},
        {"ID": 4, "Name": "Failed"},
        {"ID": 5, "Name": "Cancelled"}
    ]
    insert_data("batch_statuses", batch_statuses_data)
    print("Batch statuses inserted.")

    # 21. Insert storage locations
    storage_locations_data = []
    for refinery_id in range(1, 4):
        for location_id in range(1, 4):
            storage_locations_data.append({
                "Refinery_ID": refinery_id,
                "Name": f"Storage {location_id} - Refinery {refinery_id}"
            })
    storage_location_ids = insert_data("storage_locations", storage_locations_data)
    print("Storage locations inserted.")

    # 22. Insert tank types
    tank_types_data = [
        {"ID": 1, "Name": "Refinery Tank", "Description": "Tank located at refinery"},
        {"ID": 2, "Name": "Terminal Tank", "Description": "Tank located at terminal"},
        {"ID": 3, "Name": "Station Tank", "Description": "Tank located at station"}
    ]
    insert_data("tank_types", tank_types_data)
    print("Tank types inserted.")

    # 23. Insert transfer statuses
    transfer_statuses_data = [
        {"ID": 1, "Name": "Scheduled"},
        {"ID": 2, "Name": "In Transit"},
        {"ID": 3, "Name": "Delivered"},
        {"ID": 4, "Name": "Cancelled"}
    ]
    insert_data("transfer_statuses", transfer_statuses_data)
    print("Transfer statuses inserted.")

    # 24. Insert order types
    order_types_data = [
        {"ID": 1, "Name": "Production Order", "Description": "Order for fuel production"},
        {"ID": 2, "Name": "Supply Order", "Description": "Order for fuel supply to stations"}
    ]
    insert_data("order_types", order_types_data)
    print("Order types inserted.")

    # 25. Insert transport statuses
    transport_statuses_data = [
        {"ID": 1, "Name": "Available"},
        {"ID": 2, "Name": "In Transit"},
        {"ID": 3, "Name": "Maintenance"},
        {"ID": 4, "Name": "Out of Service"}
    ]
    insert_data("transport_statuses", transport_statuses_data)
    print("Transport statuses inserted.")

    # 26. Insert transports
    transports_data = []
    for i in range(1, 11):
        transport_type = random.choice(["Truck", "Rail", "Ship"])
        capacity = random.uniform(5000, 50000)
        status = random.randint(1, 4)

        transports_data.append({
            "Transport_Number": f"TR-{1000 + i}",
            "Transport_Type": transport_type,
            "Capacity": capacity,
            "Status": status,
            "Current_Location": random.choice(["North City", "South City", "East City", "West City", "Central Hub"])
        })
    transport_ids = insert_data("transports", transports_data)
    print("Transports inserted.")

    # 27. Insert terminals
    terminals_data = [
        {"ID": 1, "Name": "North Terminal", "Address_Line": "111 Terminal Rd, North City"},
        {"ID": 2, "Name": "South Terminal", "Address_Line": "222 Terminal Rd, South City"},
        {"ID": 3, "Name": "East Terminal", "Address_Line": "333 Terminal Rd, East City"}
    ]
    insert_data("terminals", terminals_data)
    print("Terminals inserted.")

    # 28. Insert terminal tanks
    terminal_tanks_data = []
    for terminal_id in range(1, 4):
        for fuel_type_id in range(1, 6):
            capacity = random.uniform(100000, 500000)
            current_volume = capacity * random.uniform(0.3, 0.9)
            terminal_tanks_data.append({
                "Terminal_ID": terminal_id,
                "Fuel_Type_ID": fuel_type_id,
                "Capacity": capacity,
                "Current_Volume": current_volume
            })
    terminal_tank_ids = insert_data("terminal_tanks", terminal_tanks_data)
    print("Terminal tanks inserted.")

    # 29. Insert suppliers
    suppliers_data = [
        {"ID": 1, "Name": "Crude Oil Supplier A", "Type": "Crude Oil"},
        {"ID": 2, "Name": "Crude Oil Supplier B", "Type": "Crude Oil"},
        {"ID": 3, "Name": "Chemical Supplier A", "Type": "Chemical"},
        {"ID": 4, "Name": "Additive Supplier A", "Type": "Additive"}
    ]
    insert_data("suppliers", suppliers_data)
    print("Suppliers inserted.")

    # 30. Insert raw materials
    raw_materials_data = [
        {"ID": 1, "Name": "Crude Oil - Light", "Type": "Oil", "Quality_Parameter": "API Gravity", "Price_Per_Unit": 50.0,
         "Unit": "Barrel"},
        {"ID": 2, "Name": "Crude Oil - Medium", "Type": "Oil", "Quality_Parameter": "API Gravity", "Price_Per_Unit": 45.0,
         "Unit": "Barrel"},
        {"ID": 3, "Name": "Crude Oil - Heavy", "Type": "Oil", "Quality_Parameter": "API Gravity", "Price_Per_Unit": 40.0,
         "Unit": "Barrel"},
        {"ID": 4, "Name": "Ethanol", "Type": "Additive", "Quality_Parameter": "Purity", "Price_Per_Unit": 2.0,
         "Unit": "Liter"},
        {"ID": 5, "Name": "Octane Booster", "Type": "Additive", "Quality_Parameter": "Concentration", "Price_Per_Unit": 5.0,
         "Unit": "Liter"}
    ]
    insert_data("raw_materials", raw_materials_data)
    print("Raw materials inserted.")

    # 31. Generate some production batches
    production_batches_data = []
    last_month = datetime.now() - timedelta(days=30)
    for i in range(10):
        start_time = random_datetime(last_month, datetime.now())
        # Some batches are completed, some still in progress
        end_time = None
        status_id = 2  # In Progress

        if random.random() > 0.3:  # 70% chance to be completed
            end_time = start_time + timedelta(hours=random.randint(4, 48))
            status_id = 3  # Completed

        production_batches_data.append({
            "Start_Time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "End_Time": end_time.strftime("%Y-%m-%d %H:%M:%S") if end_time else None,
            "Expected_Output_Volume": random.uniform(10000, 100000),
            "Status_ID": status_id
        })
    production_batch_ids = insert_data("production_batches", production_batches_data)
    print("Production batches inserted.")

    # 32. Insert raw materials supply
    raw_materials_supply_data = []
    last_year = datetime.now() - timedelta(days=365)
    for i in range(20):
        created_at = random_datetime(last_year, datetime.now())
        delivery_date = created_at + timedelta(days=random.randint(1, 30))

        raw_materials_supply_data.append({
            "Supplier_ID": random.randint(1, 4),
            "Raw_Material_ID": random.randint(1, 5),
            "Refinery_ID": random.randint(1, 3),
            "Delivery_Date": delivery_date.strftime("%Y-%m-%d"),
            "Created_At": created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "Quantity": random.uniform(1000, 50000),
            "Quality_Check_Passed": random.choice([True, False, None]),
            "Status_ID": random.randint(1, 5)
        })
    raw_materials_supply_ids = insert_data("raw_materials_supply", raw_materials_supply_data)
    print("Raw materials supply inserted.")

    # 33. Insert raw materials deliveries
    raw_materials_deliveries_data = []
    for supply_id in raw_materials_supply_ids:
        # Only create deliveries for some supplies (status 4 - Delivered)
        if random.random() > 0.3:
            # Get the supply record to determine a realistic received date
            cursor.execute("SELECT Created_At, Delivery_Date FROM raw_materials_supply WHERE ID = %s", (supply_id,))
            result = cursor.fetchone()
            created_at = result[0]  # datetime
            delivery_date = result[1]  # date

            delivery_dt = datetime.combine(delivery_date, datetime.min.time())

            received_at = random_datetime(
                created_at,
                delivery_dt + timedelta(days=3)
            )

            raw_materials_deliveries_data.append({
                "Supply_ID": supply_id,
                "Received_At": received_at.strftime("%Y-%m-%d %H:%M:%S")
            })
    raw_materials_deliveries_ids = insert_data("raw_materials_deliveries", raw_materials_deliveries_data)
    print("Raw materials deliveries inserted.")

    # 34. Insert delivery items
    delivery_items_data = []
    for delivery_id in raw_materials_deliveries_ids:
        # Get the delivery info to determine supply and related info
        cursor.execute("""
            SELECT d.Received_At, s.Raw_Material_ID, s.Refinery_ID 
            FROM raw_materials_deliveries d
            JOIN raw_materials_supply s ON d.Supply_ID = s.ID
            WHERE d.ID = %s
        """, (delivery_id,))
        result = cursor.fetchone()
        received_at = result[0]
        raw_material_id = result[1]
        refinery_id = result[2]

        # Get storage locations for this refinery
        cursor.execute("SELECT ID FROM storage_locations WHERE Refinery_ID = %s", (refinery_id,))
        storage_locations = cursor.fetchall()

        if storage_locations:
            # Create 1-3 delivery items for each delivery
            for _ in range(random.randint(1, 3)):
                storage_location_id = random.choice(storage_locations)[0]

                delivery_items_data.append({
                    "Delivery_ID": delivery_id,
                    "Storage_Location_ID": storage_location_id,
                    "Raw_Material_ID": raw_material_id,
                    "Deliveried_At": received_at
                })
    delivery_item_ids = insert_data("delivery_items", delivery_items_data)
    print("Delivery items inserted.")

    # 35. Insert production batch raw materials
    production_batch_raw_materials_data = []
    for batch_id in production_batch_ids:
        # Each batch uses 2-5 raw materials
        for _ in range(random.randint(2, 5)):
            if delivery_item_ids:  # Make sure we have delivery items
                delivery_item_id = random.choice(delivery_item_ids)

                production_batch_raw_materials_data.append({
                    "Production_Batch_ID": batch_id,
                    "Delivery_Item_ID": delivery_item_id,
                    "Volume": random.uniform(100, 5000)
                })
    cursor.executemany(
        """
        INSERT INTO production_batch_raw_materials
        (production_batch_id, delivery_item_id, volume)
        VALUES (%s, %s, %s)
        ON CONFLICT (production_batch_id, delivery_item_id) DO NOTHING
        """,
        [
            (d["Production_Batch_ID"], d["Delivery_Item_ID"], d["Volume"])
            for d in production_batch_raw_materials_data
        ]
    )

    conn.commit()
    print("Production batch raw materials inserted.")

    # 36. Insert production batch units
    production_batch_units_data = []
    for batch_id in production_batch_ids:
        # Get batch information
        cursor.execute("SELECT Start_Time, End_Time, Status_ID FROM production_batches WHERE ID = %s", (batch_id,))
        result = cursor.fetchone()
        start_time = result[0]
        end_time = result[1]
        batch_status = result[2]

        # Assign 1-3 production units to each batch
        for _ in range(random.randint(1, 3)):
            # Get a random production unit
            cursor.execute("SELECT ID FROM production_units ORDER BY RANDOM() LIMIT 1")
            production_unit_id = cursor.fetchone()[0]

            unit_start_time = start_time + timedelta(minutes=random.randint(0, 120))
            unit_end_time = None

            if end_time and batch_status == 3:  # If batch is completed
                unit_end_time = unit_start_time + timedelta(
                    minutes=random.randint(60, int((end_time - unit_start_time).total_seconds() / 60)))

            production_batch_units_data.append({
                "Production_Batch_ID": batch_id,
                "Production_Unit_ID": production_unit_id,
                "Start_Time": unit_start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "End_Time": unit_end_time.strftime("%Y-%m-%d %H:%M:%S") if unit_end_time else None
            })
    cursor.executemany(
        """
        INSERT INTO production_batch_units 
        (Production_Batch_ID, Production_Unit_ID, Start_Time, End_Time) 
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (production_batch_id, production_unit_id) DO NOTHING
        """,
        [(d["Production_Batch_ID"], d["Production_Unit_ID"], d["Start_Time"], d["End_Time"]) for d in
         production_batch_units_data]
    )
    conn.commit()
    print("Production batch units inserted.")

    # 37. Insert production batch tank refineries
    production_batch_tank_refineries_data = []
    for batch_id in production_batch_ids:
        # Each batch is connected to 1-2 refinery tanks
        for _ in range(random.randint(1, 2)):
            # Get a random refinery tank
            cursor.execute("SELECT ID FROM refinery_tanks ORDER BY RANDOM() LIMIT 1")
            refinery_tank_id = cursor.fetchone()[0]

            production_batch_tank_refineries_data.append({
                "Production_Batch_ID": batch_id,
                "Refinery_Tank_ID": refinery_tank_id
            })
    cursor.executemany(
        """
        INSERT INTO production_batch_tank_refineries 
        (Production_Batch_ID, Refinery_Tank_ID) 
        VALUES (%s, %s)
        ON CONFLICT (Production_Batch_ID, Refinery_Tank_ID) DO NOTHING
        """,
        [(d["Production_Batch_ID"], d["Refinery_Tank_ID"]) for d in production_batch_tank_refineries_data]
    )
    conn.commit()
    print("Production batch tank refineries inserted.")

    # Continuing from where the script was cut off...

    # 38. Insert supply orders
    supply_orders_data = []
    last_month = datetime.now() - timedelta(days=30)
    for _ in range(20):
        created_at = random_datetime(last_month, datetime.now())
        supply_date = created_at.date() + timedelta(days=random.randint(1, 14))

        supply_orders_data.append({
            "Fuel_Type_ID": random.randint(1, 5),
            "Created_At": created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "Supply_Date": supply_date.strftime("%Y-%m-%d"),
            "Station_ID": random.randint(1, 5),
            "Status_ID": random.randint(1, 5)
        })
    supply_order_ids = insert_data("supply_orders", supply_orders_data)
    print("Supply orders inserted.")

    # 39. Insert production orders
    production_orders_data = []
    last_month = datetime.now() - timedelta(days=30)
    for _ in range(15):
        created_at = random_datetime(last_month, datetime.now())
        required_by_date = created_at.date() + timedelta(days=random.randint(5, 30))

        production_orders_data.append({
            "Terminal_ID": random.randint(1, 3),
            "Fuel_Type_ID": random.randint(1, 5),
            "Refinery_ID": random.randint(1, 3),
            "Volume_Requested": random.uniform(50000, 500000),
            "Created_At": created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "Required_By_Date": required_by_date.strftime("%Y-%m-%d"),
            "Priority": random.randint(1, 3),
            "Status_ID": random.randint(1, 5)
        })
    production_order_ids = insert_data("production_orders", production_orders_data)
    print("Production orders inserted.")

    # 40. Insert fuel transfers
    fuel_transfers_data = []
    last_month = datetime.now() - timedelta(days=30)

    # Create transfers for production orders (refinery to terminal)
    for order_id in production_order_ids:
        if random.random() > 0.3:  # Only create transfers for some orders
            # Get order details
            cursor.execute("""
                SELECT Terminal_ID, Fuel_Type_ID, Refinery_ID, Volume_Requested
                FROM production_orders
                WHERE ID = %s
            """, (order_id,))
            result = cursor.fetchone()
            terminal_id, fuel_type_id, refinery_id, volume = result

            # Find source refinery tank
            cursor.execute("""
                SELECT ID FROM refinery_tanks 
                WHERE Refinery_ID = %s AND Fuel_Type_ID = %s
            """, (refinery_id, fuel_type_id))
            refinery_tank_ids = cursor.fetchall()

            # Find destination terminal tank
            cursor.execute("""
                SELECT ID FROM terminal_tanks 
                WHERE Terminal_ID = %s AND Fuel_Type_ID = %s
            """, (terminal_id, fuel_type_id))
            terminal_tank_ids = cursor.fetchall()

            if refinery_tank_ids and terminal_tank_ids:
                source_id = refinery_tank_ids[0][0]
                destination_id = terminal_tank_ids[0][0]

                dispatched_at = random_datetime(last_month, datetime.now())
                received_at = None
                status_id = 2  # In Transit

                if random.random() > 0.5:  # 50% chance to be delivered
                    received_at = dispatched_at + timedelta(hours=random.randint(6, 72))
                    status_id = 3  # Delivered

                fuel_transfers_data.append({
                    "Source_Type_ID": 1,  # Refinery Tank
                    "Source_ID": source_id,
                    "Destination_Type_ID": 2,  # Terminal Tank
                    "Destination_ID": destination_id,
                    "Order_Type_ID": 1,  # Production Order
                    "Order_ID": order_id,
                    "Volume": float(volume) * random.uniform(0.9, 1.0),  # Slight variance in volume
                    "Dispatched_At": dispatched_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "Received_At": received_at.strftime("%Y-%m-%d %H:%M:%S") if received_at else None,
                    "Status_ID": status_id
                })

    # Create transfers for supply orders (terminal to station)
    for order_id in supply_order_ids:
        if random.random() > 0.3:  # Only create transfers for some orders
            # Get order details
            cursor.execute("""
                SELECT Station_ID, Fuel_Type_ID
                FROM supply_orders
                WHERE ID = %s
            """, (order_id,))
            result = cursor.fetchone()
            station_id, fuel_type_id = result

            # Find source terminal tank (randomly choose a terminal)
            terminal_id = random.randint(1, 3)
            cursor.execute("""
                SELECT ID FROM terminal_tanks 
                WHERE Terminal_ID = %s AND Fuel_Type_ID = %s
            """, (terminal_id, fuel_type_id))
            terminal_tank_ids = cursor.fetchall()

            # Find destination station tank
            cursor.execute("""
                SELECT ID FROM station_tanks 
                WHERE Station_ID = %s AND Fuel_Type_ID = %s
            """, (station_id, fuel_type_id))
            station_tank_ids = cursor.fetchall()

            if terminal_tank_ids and station_tank_ids:
                source_id = terminal_tank_ids[0][0]
                destination_id = station_tank_ids[0][0]

                # For volume, get the capacity and current volume of the station tank
                cursor.execute("""
                    SELECT Capacity, Current_Volume
                    FROM station_tanks
                    WHERE ID = %s
                """, (destination_id,))
                tank_result = cursor.fetchone()
                capacity, current_volume = tank_result
                transfer_volume = min((float(capacity) - float(current_volume)) * random.uniform(0.5, 0.9),
                                      random.uniform(5000, 15000))

                dispatched_at = random_datetime(last_month, datetime.now())
                received_at = None
                status_id = 2  # In Transit

                if random.random() > 0.5:  # 50% chance to be delivered
                    received_at = dispatched_at + timedelta(hours=random.randint(2, 24))
                    status_id = 3  # Delivered

                fuel_transfers_data.append({
                    "Source_Type_ID": 2,  # Terminal Tank
                    "Source_ID": source_id,
                    "Destination_Type_ID": 3,  # Station Tank
                    "Destination_ID": destination_id,
                    "Order_Type_ID": 2,  # Supply Order
                    "Order_ID": order_id,
                    "Volume": transfer_volume,
                    "Dispatched_At": dispatched_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "Received_At": received_at.strftime("%Y-%m-%d %H:%M:%S") if received_at else None,
                    "Status_ID": status_id
                })

    fuel_transfer_ids = insert_data("fuel_transfers", fuel_transfers_data)
    print("Fuel transfers inserted.")

    # 41. Insert transfer transports
    transfer_transports_data = []
    for transfer_id in fuel_transfer_ids:
        # Get transfer volume
        cursor.execute("SELECT Volume FROM fuel_transfers WHERE ID = %s", (transfer_id,))
        transfer_volume = cursor.fetchone()[0]

        # Assign 1-2 transports for each transfer
        transports_needed = random.randint(1, 2)
        remaining_volume = float(transfer_volume)

        for _ in range(transports_needed):
            # Select a random available transport
            cursor.execute("""
                SELECT ID, Capacity FROM transports 
                WHERE Status = 1 OR Status = 2
                ORDER BY RANDOM() LIMIT 1
            """)
            result = cursor.fetchone()

            if result:
                transport_id, capacity = result

                # Calculate volume for this transport
                if transports_needed == 1 or _ == transports_needed - 1:
                    volume = remaining_volume
                else:
                    volume = min(float(remaining_volume) * random.uniform(0.4, 0.7), float(capacity))
                    remaining_volume -= volume

                transfer_transports_data.append({
                    "Transfer_ID": transfer_id,
                    "Transport_ID": transport_id,
                    "Volume": volume
                })

                # Update transport status to in transit if not already
                cursor.execute("UPDATE transports SET Status = 2 WHERE ID = %s", (transport_id,))
                conn.commit()

    cursor.executemany(
        """
        INSERT INTO transfer_transports 
        (Transfer_ID, Transport_ID, Volume) 
        VALUES (%s, %s, %s)
        ON CONFLICT (Transfer_ID, Transport_ID) DO NOTHING
        """,
        [(d["Transfer_ID"], d["Transport_ID"], d["Volume"]) for d in transfer_transports_data]
    )
    conn.commit()
    print("Transfer transports inserted.")

    # 42. Insert sale transactions and refueling sessions
    sale_transactions_data = []
    refueling_sessions_data = []

    # Generate for the past 3 months
    three_months_ago = datetime.now() - timedelta(days=90)

    # Generate 100 sales transactions
    for _ in range(100):
        transaction_datetime = random_datetime(three_months_ago, datetime.now())

        # Randomly decide if there's a customer or not
        customer_id = random.choice([None] + customer_ids) if random.random() > 0.3 else None

        # Select random operator
        operator_id = random.randint(1, 5)

        # Select payment method
        payment_method_id = random.randint(1, 5)

        # Determine volume and amount
        volume = random.uniform(5, 80)

        # Get a random fuel type and its price
        fuel_type_id = random.randint(1, 5)
        cursor.execute("SELECT Price_Per_Unit FROM fuel_types WHERE ID = %s", (fuel_type_id,))
        price_per_unit = cursor.fetchone()[0]

        total_amount = volume * float(price_per_unit)

        # Determine if bonus points were used
        bonus_used = 0
        if customer_id and random.random() > 0.8:  # 20% chance to use bonus
            # Get customer's bonus points
            cursor.execute("SELECT Bonus_Points FROM customers WHERE ID = %s", (customer_id,))
            available_bonus = cursor.fetchone()[0]
            if available_bonus > 0:
                bonus_used = min(int(available_bonus), int(total_amount * 100))  # 1 bonus = 0.01 currency
                # Update customer's bonus points
                cursor.execute(
                    "UPDATE customers SET Bonus_Points = Bonus_Points - %s WHERE ID = %s",
                    (bonus_used, customer_id)
                )
                conn.commit()

        # Adjust total amount based on bonus usage
        total_amount -= (bonus_used * 0.01)

        # Transaction status (mostly completed)
        status_id = 3  # Completed
        if random.random() > 0.95:  # 5% chance for other statuses
            status_id = random.choice([1, 2, 4, 5, 6])

        # Insert transaction
        sale_transaction = {
            "Customer_ID": customer_id,
            "Operator_ID": operator_id,
            "Payment_Method_ID": payment_method_id,
            "Total_Amount": total_amount,
            "Transaction_Date_Time": transaction_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "Bonus_Used": bonus_used,
            "Volume": volume,
            "Currency": "USD",
            "Status_ID": status_id
        }

        sale_transaction_id = insert_data("sale_transactions", [sale_transaction])[0]

        # If transaction is completed, also create refueling session
        if status_id == 3:
            # Get a random fuel pump for this fuel type
            cursor.execute("""
                SELECT fp.ID, fp.Fuel_Dispenser_ID 
                FROM fuel_pumps fp
                JOIN fuel_dispensers fd ON fp.Fuel_Dispenser_ID = fd.ID
                WHERE fp.Fuel_Type_ID = %s AND fp.Is_Active = True
                ORDER BY RANDOM() LIMIT 1
            """, (fuel_type_id,))
            pump_result = cursor.fetchone()

            if pump_result:
                fuel_pump_id, dispenser_id = pump_result

                # Create refueling session
                started_at = transaction_datetime
                finished_at = started_at + timedelta(minutes=random.randint(5, 15))

                refueling_session = {
                    "Fuel_Pump_ID": fuel_pump_id,
                    "Fuel_Type_ID": fuel_type_id,
                    "Volume": volume,
                    "Authorized_Volume": volume * 1.2,  # A bit more than actual volume
                    "Started_At": started_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "Finished_At": finished_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "Status_ID": 3,  # Completed
                    "Sale_Transaction_ID": sale_transaction_id
                }

                insert_data("refueling_sessions", [refueling_session])

                # If there's a customer, update their stats
                if customer_id:
                    cursor.execute(
                        """
                        UPDATE customers 
                        SET Total_Purchases = Total_Purchases + %s,
                            Last_Visit_Date = %s,
                            Bonus_Points = Bonus_Points + %s
                        WHERE ID = %s
                        """,
                        (total_amount,
                         transaction_datetime.strftime("%Y-%m-%d"),
                         int(total_amount * 10),  # 10 bonus points per currency unit
                         customer_id)
                    )
                    conn.commit()

    print("Sale transactions and refueling sessions inserted.")

    # 43. Insert sale transaction audits
    # For some transactions, add audit records
    for sale_transaction_id in range(1, 101):
        # Only create audits for some transactions
        if random.random() > 0.7:  # 30% chance
            # Get current status
            cursor.execute("SELECT Status_ID FROM sale_transactions WHERE ID = %s", (sale_transaction_id,))
            result = cursor.fetchone()

            if result:
                current_status = result[0]

                # Create 1-3 audit records
                for _ in range(random.randint(1, 3)):
                    old_status = random.randint(1, 6)
                    new_status = current_status

                    # Make sure old and new are different
                    while old_status == new_status:
                        old_status = random.randint(1, 6)

                    changed_at = random_datetime(three_months_ago, datetime.now())

                    cursor.execute(
                        """
                        INSERT INTO sale_transaction_audit 
                        (Sale_Transaction_ID, Changed_At, Old_Status_ID, New_Status_ID, Comments)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (sale_transaction_id,
                         changed_at.strftime("%Y-%m-%d %H:%M:%S"),
                         old_status,
                         new_status,
                         f"Status changed from {old_status} to {new_status}")
                    )
                    conn.commit()

    print("Sale transaction audits inserted.")

    print("All data inserted successfully.")

    # Close the connection
    conn.close()

