import time
from datetime import datetime

# ------------ Mall Data -----
malls = {
    "1": {"name": "Gateway", "capacity": 250, "type": "flat"},
    "2": {"name": "Pavilion", "capacity": 180, "type": "hourly"},
    "3": {"name": "La Lucia", "capacity": 150, "type": "capped"}
}

# ------------ File Handling ------------

def load_file(filename):
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []

def save_file(filename, data):
    with open(filename, "w") as f:
        for line in data:
            f.write(line + "\n")


# ----------- Login System ------------------

def register():
    username = input("Username: ")
    password = input("Password: ")
    role = input("Role (customer/admin/owner): ")

    mall = "none"
    if role == "admin":
        print("\nAssign admin to mall:")
        print("1 - Gateway (Flat Rate R15, Capacity 250)")
        print("2 - Pavilion (R10/hour, Capacity 180)")
        print("3 - La Lucia (R12/hour capped at R60, Capacity 150)")
        mall = input("Mall: ")

    users = load_file("users.txt")
    users.append(f"{username},{password},{role},{mall}")
    save_file("users.txt", users)

    print("Registered successfully!")

def login():
    username = input("Username: ")
    password = input("Password: ")

    users = load_file("users.txt")

    for user in users:
        u, p, r, m = user.split(",")
        if u == username and p == password:
            return username, r, m

    print("Login failed")
    return None, None, None


# ---------- Rates ------------------

def calculate_fee(mall_name, hours):
    if mall_name == "Gateway":
        return 15
    elif mall_name == "Pavilion":
        return hours * 10
    elif mall_name == "La Lucia":
        return min(hours * 12, 60)
    else:
        return 0


# ---------- Parking ------------------

def park_vehicle(username, mall):
    records = load_file("parking.txt")

    current = [r for r in records if r.split(",")[1] == mall and r.split(",")[4] == "no"]
    if len(current) >= malls[mall]["capacity"]:
        print("Parking full!")
        return

    entry_time = time.time()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    records.append(f"{username},{mall},{entry_time},0,no,{date_str}")
    save_file("parking.txt", records)

    print(f"Vehicle parked at {malls[mall]['name']}.")

def exit_vehicle(username):
    records = load_file("parking.txt")

    for i in range(len(records)):
        parts = records[i].split(",")
        u, mall, entry, exit_t, paid, date_str = parts

        if u == username and paid == "no":
            exit_time = time.time()
            duration = (exit_time - float(entry)) / 3600
            hours = int(duration) + 1

            mall_name = malls[mall]["name"]
            fee = calculate_fee(mall_name, hours)

            print(f"\nMall: {mall_name}")
            print(f"Hours: {hours}")
            print(f"Fee: R{fee}")

            if input("Pay? (y/n): ") == "y":
                records[i] = f"{u},{mall},{entry},{exit_time},yes,{date_str}"
                save_file("parking.txt", records)

                payments = load_file("payments.txt")
                payments.append(f"{u},{fee},{mall_name},{hours}")
                save_file("payments.txt", payments)

                print("Paid successfully!")
            return

    print("No active parking.")

def view_history(username):
    records = load_file("parking.txt")
    print("\n--- Your Parking History ---")
    for r in records:
        u, mall, entry, exit_t, paid, date_str = r.split(",")
        if u == username:
            print(f"Mall: {malls[mall]['name']}, Date: {date_str}, Paid: {paid}")


# ------------ Admin ------------------

def admin_menu(admin_mall):
    records = load_file("parking.txt")

    print(f"\n--- Admin Dashboard ({malls[admin_mall]['name']}) ---")

    for r in records:
        u, mall, entry, exit_t, paid, date_str = r.split(",")
        if mall == admin_mall and paid == "no":
            print(f"User: {u}, Entry: {date_str}")

    current = [r for r in records if r.split(",")[1] == admin_mall and r.split(",")[4] == "no"]
    capacity = malls[admin_mall]["capacity"]

    print(f"\nCurrent Vehicles: {len(current)}")
    print(f"Remaining Capacity: {capacity - len(current)}")

    today = datetime.now().strftime("%Y-%m-%d")
    count = 0
    for r in records:
        if admin_mall == r.split(",")[1] and today in r:
            count += 1

    print(f"Entries Today: {count}")


# ---------- Owner ------------------
def owner_menu():
    records = load_file("parking.txt")
    payments = load_file("payments.txt")

    total_revenue = {}
    total_vehicles = {}
    total_hours = {}

    for m in malls:
        name = malls[m]["name"]
        total_revenue[name] = 0
        total_vehicles[name] = 0
        total_hours[name] = 0

    for p in payments:
        u, amount, mall, hours = p.split(",")
        total_revenue[mall] += float(amount)
        total_hours[mall] += float(hours)

    for r in records:
        mall = malls[r.split(",")[1]]["name"]
        total_vehicles[mall] += 1

    print("\n--- Owner Report ---")
    for mall in total_revenue:
        vehicles = total_vehicles[mall]
        hours = total_hours[mall]
        avg = hours / vehicles if vehicles > 0 else 0

        print(f"\n{mall}")
        print(f"Revenue: R{total_revenue[mall]}")
        print(f"Vehicles: {vehicles}")
        print(f"Average Duration: {round(avg,2)} hrs")

# ---------- Main ------------------

def main():
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose: ")

        if choice == "1":
            register()

        elif choice == "2":
            username, role, mall = login()

            if username is None:
                continue

            if role == "customer":
                while True:
                    print("\n1. Park\n2. Exit Parking\n3. History\n4. Logout")
                    _choose = input("Choose: ")

                    if _choose == "1":
                        print("\nSelect Mall:")
                        print("1 - Gateway (Flat Rate R15, Capacity 250)")
                        print("2 - Pavilion (R10/hour, Capacity 180)")
                        print("3 - La Lucia (R12/hour capped at R60, Capacity 150)")

                        _mall = input("Mall: ")

                        if _mall not in malls:
                            print("Invalid selection")
                            continue

                        park_vehicle(username, _mall)

                    elif _choose == "2":
                        exit_vehicle(username)

                    elif _choose == "3":
                        view_history(username)

                    else:
                        break

            elif role == "admin":
                admin_menu(mall)

            elif role == "owner":
                owner_menu()

        else:
            break

main()