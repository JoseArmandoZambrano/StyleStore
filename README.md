# StyleStore

StyleStore is a desktop retail management application developed in Python using PyQt5 and SQLite.

The application was created as a university project for courses related to Software Engineering and Software Quality. Its purpose was to apply software development principles to a practical business management scenario.

## Overview

StyleStore simulates a retail management system for a clothing store. It provides a graphical interface for managing products, clients, suppliers, sales, promotions, reports, and database backups.

The application runs locally as a desktop application and uses SQLite for data persistence.

## Features

- Product management
- Client management
- Supplier management
- Sales management
- Promotion management
- Inventory management
- Reports
- Database backup and restore
- SQLite database
- Sample data generation for demonstrations
- Graphical user interface built with PyQt5

## Technologies

- **Python 3**
- **PyQt5**
- **SQLite**
- **Git / GitHub**

## Project Structure

```text
StyleStore/
│
├── database/
│   └── Database configuration and connection logic
│
├── models/
│   └── Business logic and database operations
│
├── ui/
│   └── Graphical user interface components
│
├── FirstBackup/
│   └── Database backup files
│
├── main.py
├── seed_data.py
├── .gitignore
└── README.md
```

## Requirements

Before running the application, make sure you have:

- Python 3.x
- pip
- Git

## Installation

Clone the repository:

```bash
git clone https://github.com/JoseArmandoZambrano/StyleStore.git
```

Move into the project directory:

```bash
cd StyleStore
```

## Virtual Environment

It is recommended to use a virtual environment.

Create one with:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

## Install Dependencies

Install the required Python packages:

```bash
pip install PyQt5
```

If a `requirements.txt` file is available, dependencies can instead be installed with:

```bash
pip install -r requirements.txt
```

## Database Setup

The application uses SQLite as its local database.

When the application starts, the database initialization function creates the required tables if they do not already exist.

The database file is generated locally and is not included in version control.

## Sample Data

The project includes `seed_data.py`, which can be used to populate the database with sample information for demonstrations and testing.

Run:

```bash
python seed_data.py
```

The script creates sample data including:

- Categories
- Suppliers
- Products
- Clients
- Promotions
- Sales

> Run the seed script only when you want to populate the database with demonstration data.

## Running the Application

After installing the dependencies, run:

```bash
python main.py
```

The StyleStore desktop application will open locally.

## Main Modules

### Products

Allows the management of products, including information such as:

- Name
- Category
- Size
- Color
- Purchase price
- Sale price
- Stock
- Supplier
- Description

### Clients

Provides functionality for registering and managing customers.

### Suppliers

Allows supplier information to be stored and managed.

### Sales

Provides a sales workflow with products, quantities, customers, payment methods, and totals.

### Promotions

Allows the creation and management of promotional campaigns.

### Reports

Provides access to reports generated from the application's data.

### Backup and Restore

The application includes functionality for backing up and restoring the SQLite database.

## Database

StyleStore uses SQLite as its database engine.

The database is stored locally because the application is designed as a desktop application.

The database file is intentionally excluded from Git using `.gitignore`:

```gitignore
stylestore.db
```

This prevents local database files from being committed to the repository.

## Academic Context

This project was developed as part of university coursework related to:

- Software Engineering
- Software Quality
- Application development
- Database management

The project was designed to practice the development of a modular desktop application while applying concepts related to software organization, data management, validation, testing, and maintainability.

## Learning Outcomes

Through this project, I gained practical experience with:

- Python application development
- GUI development with PyQt5
- SQLite database integration
- CRUD operations
- Modular project organization
- Separation between UI, models, and database logic
- Data validation
- Inventory and sales management
- Database backup and restoration
- Debugging and testing
- Git and GitHub

## Screenshots

Screenshots of the application can be added here to show the main interface and its different modules.

Example:

```text
screenshots/
├── home.png
├── products.png
├── sales.png
├── reports.png
└── backup.png
```

## Project Status

Completed academic project.

The application is currently intended to run locally as a desktop application.

## Author

**José Armando Zambrano Muñoz**

Computer Engineering Student  
Universidad de Guadalajara — CUCEI

GitHub:  
https://github.com/JoseArmandoZambrano
