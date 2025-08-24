# 🏥 Hospital Management System (HMS)

A simple web-based hospital management system built with **Django** and **MySQL**.  
It provides role-based access for **Admin, Doctors, and Patients**.

## ✨ Features
- **Admin (Django superuser):** View/manage doctors, patients, and appointments (date-wise).  
- **Doctor:** Register/login, update details.  
- **Patient:** Register/login, book appointments.  

## 🛠 Tech Stack
- Python, Django  
- MySQL  
- HTML, CSS  

## ⚙️ Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/saikrishna-chary/hospital_management.git
   cd hospital_management


## Create a Virtual Environment
  - python -m venv venv
  - Activate on Windows
  - venv\Scripts\activate
  - Activate on Linux/Mac
  - source venv/bin/activate


## Install Dependencies
- pip install -r requirements.txt

## Configure Database
  - Open settings.py.
  - Update the DATABASES section with your MySQL username, password, and database name. Example:
  - DATABASES = {
  - 'default': {
       - 'ENGINE': 'django.db.backends.mysql',
       - 'NAME': 'hospital_db',
       - 'USER': 'root',
       - 'PASSWORD': 'yourpassword',
       - 'HOST': '127.0.0.1',
       - 'PORT': '3306',
     - }
   - }

## Apply Migrations
  - python manage.py makemigrations
  - python manage.py migrate

## Create Superuser (Admin)
  - python manage.py createsuperuser

## Run the Development Server
  - python manage.py runserver




