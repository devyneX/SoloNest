# SoloNest

## Table of Contents
- [SoloNest](#solonest)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Features](#features)
  - [Instructions](#instructions)

## About
In today's fast-paced world, convenience and efficiency are paramount. Recognizing the challenges faced by bachelors in managing their accommodations, SoloNest emerges as a modern solution that seamlessly integrates room booking, service management, and communication all under one platform.

SoloNest's primary objective is to provide a streamlined platform for bachelors seeking accommodation, while also enabling efficient management for home managers. It aims to digitize the conventional systems, eliminating manual processes and enhancing the overall experience for both tenants and managers.


## Features

- The system allows the Users to register/login  
- The system allows the Users to update their account info (name, username, email etc)
- The system allows the Users to update their password
- The system allows the Users to update their Profile (birth certificate, nid, phone_no, blood group, emergency contact) 
- The system allows the registered Users to send Room Requests if their Profile is complete. 
- The system allows the Manager to approve/reject Room Requests 
- The system sends an email to the User once their request is approved/rejected.
- The system allows the Users to pay Booking Fee (security deposit) online after their Room Request is approved and become a Tenant
- If the Tenant doesn’t pay the Booking Fee within the 3 days, the system will mark their Room Request as expired.
- The system allows the Tenant to send Leave Request [must send before 5th of the month to leave the next month]
- The system allows Tenants to set a default mode for their lunch and dinner Meals (either ON or OFF)
- The system allows the Tenants to turn the Meal ON or OFF for particular day outside of their default mode
- The system ensures that the Tenant cannot update Lunch after 11 AM and Dinner after 5PM.
- The system allows the Tenants to track how many meals they have taken and how much it cost in the current month
- The system allows the Manager to view the list of Meals for Lunch and Dinner for the current day 
- The system allows the Manager to create and view meal menu
- The system allows the Tenant to view the current meal menu
- The system allows the Tenants to send Feedback of the services.
- The system allows the Manager to view Tenant Feedbacks.
- The system allows the Tenants to request Cleaning for their room by selecting a cleaning slot 
- The system ensures that the cleaning requests are at least one day in advance 
- The system ensures that only one cleaning request is sent a day per room
- The system ensures that cleaning slot is not maxed out
- The system allows the Manager to view the Cleaning Requests for today
- The systems allows the Manager to search for and view the Cleaning Requests for a particular date
- The system allows the Manager to mark the Cleaning Requests as Complete once they’re done
- The system allows the Tenants to send Repair Requests 
- The system allows the Manager to mark the Repair Requests as Complete once they’re done
- The system allows the Tenants to send Laundry Requests and add laundry items.
- The system ensures that the Tenant cannot request Laundry Service until the previous Laundry is returned
- The system allows the Manager to view the Laundry requests according to their Status.
- The system allows the Manager to Update the status of the Laundry Request (Pending, Received, Washing, Drying, Ready, Returned)
- The system allows the Tenants to track their Laundry Service cost for the current month
- The system allows the Tenants to report Laundry Items as Missing
- The system allows the Manager to mark Missing Laundry Items as Found/Returned once they’re found and returned. 
- The system allows the tenant to view the status of the missing laundry 
- The system allows the Manager to edit branch details such as Meal Price, Room Base Rent, Maximum Number of Rooms Cleaned per Slot etc.
- The system allows the Manager to send out monthly Bills (Rent, Meals, Laundry).
- The system ensures that bills are not sent out to leaving tenants
- The system allows the Tenants to pay monthly Bills online.



## Instructions

- Clone this repo using 
```bash
git clone https://github.com/devyneX/SoloNest.git
```
- Create a virtual environment using 
```bash
conda create -n SoloNest python=3.9
```
- Activate the virtual environment using 
```bash
conda activate SoloNest
```
- Install the requirements using 
```bash
pip install -r requirements.txt
```
- Run the command to set up tailwindcss
```bash
python manage.py tailwind install
```
- Create a .env file in the root directory and add the following variables
```bash
DB_NAME=YourDatabaseName
DB_USER=YoutDatabaseUser
DB_PASS=YourDatabasePassword
DB_HOST=YoutDatabaseHost
DB_PORT=YourDatabasePort
NPM_PATH=path/to/npm
STORE_ID=YourSSLCommerzStoreID
STORE_PASSWD=YourSSLCommerzStorePassword
IS_SANDBOX=TRUE
```
- Run the following commands to migrate the database
```bash
python manage.py makemigrations
python manage.py migrate
```
- Run the following command to start the server
```bash
python manage.py runserver
```