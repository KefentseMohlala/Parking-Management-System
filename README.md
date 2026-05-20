# Parking-Management-System

Overview:

This project is a Python-based Parking Management System developed for multiple shopping malls in KwaZulu-Natal, South Africa. The system standardises parking operations across malls while supporting different pricing structures, parking capacities, and user access levels.

The application allows customers to park and pay for vehicles, administrators to monitor parking activity at specific malls, and owners/shareholders to view reports across all malls.

Features:
User Authentication:
- User registration
- User login
- Role-based access control

Customer Features:
- Select a shopping mall
- Register vehicle entry and exit
- View parking fees before payment
- Make parking payments
- View parking history

Parking Administrator Features:
- View vehicles currently parked
- Monitor parking capacity
- View daily parking activity

Owner / Shareholder Features:
- View mall revenue reports
- Compare parking activity across malls
- View average parking duration statistics

Shopping Malls Included:

Gateway Theatre of Shopping:
Flat rate pricing
Fee: R15 per visit
Capacity: 250 vehicles

Pavilion Shopping Centre:
Hourly pricing
Fee: R10 per hour
Capacity: 180 vehicles

La Lucia Mall:
Hourly pricing with daily cap
Fee: R12 per hour
Maximum daily charge: R60
Capacity: 150 vehicles

Technologies Used:
Python
Text file storage (.txt)

Files Included:
ParkingManagementSystem.py → Main Python application
users.txt → Stores user account information
parking.txt → Stores parking records
payments.txt → Stores payment records

How to Run the Program:
Open the project folder.
Ensure Python is installed on your computer.
Run the ParkingManagementSystem.py file.
Register a user account.
Login and use the system according to your role.

Data Persistence:
The system uses text files to store:
User accounts
Parking records
Payment information

This allows data to remain available between program executions.
