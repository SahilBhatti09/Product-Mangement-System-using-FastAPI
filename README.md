# Product Management System

**Date:** 2026-01-12

---

## Overview
This project is a **Product Management System** developed using **Python** and **FastAPI**.  
It allows users to **perform full CRUD operations** (Create, Read, Update, Delete) on products using a simple web interface.  

The project focuses on easy data management, validation, and a responsive front-end interface.

---

## Features

### Backend (FastAPI)
- **Add Products**: Users can add new products with details like name, description, price, discount, rating, category, tags, stock, seller information, and dimensions.
- **View Products**: Users can list all products stored in the system.
- **Update Products**: Users can update the entire product or individual fields using the product UUID.
- **Delete Products**: Users can delete a product by its UUID.
- **Data Validation**: FastAPI validates data types and required fields automatically.
- **Database**: Products are stored in a simple **JSON file**, acting as a lightweight database.

### Frontend (HTML, CSS, JS)
- Interactive and responsive forms for **Add**, **Update**, **Delete** operations.
- Input validation before submission.
- Modern UI enhancements using **CSS variables**, **hover effects**, **card-style layout**, and **responsive design**.
- Dynamic updates using **JavaScript Fetch API** for real-time communication with FastAPI endpoints.

---

## File Structure

# Product Management System

**Date:** 2026-01-12

---

## Overview
This project is a **Product Management System** developed using **Python** and **FastAPI**.  
It allows users to **perform full CRUD operations** (Create, Read, Update, Delete) on products using a simple web interface.  

The project focuses on easy data management, validation, and a responsive front-end interface.

---

## Features

### Backend (FastAPI)
- **Add Products**: Users can add new products with details like name, description, price, discount, rating, category, tags, stock, seller information, and dimensions.
- **View Products**: Users can list all products stored in the system.
- **Update Products**: Users can update the entire product or individual fields using the product UUID.
- **Delete Products**: Users can delete a product by its UUID.
- **Data Validation**: FastAPI validates data types and required fields automatically.
- **Database**: Products are stored in a simple **JSON file**, acting as a lightweight database.

### Frontend (HTML, CSS, JS)
- Interactive and responsive forms for **Add**, **Update**, **Delete** operations.
- Input validation before submission.
- Modern UI enhancements using **CSS variables**, **hover effects**, **card-style layout**, and **responsive design**.
- Dynamic updates using **JavaScript Fetch API** for real-time communication with FastAPI endpoints.

---

## File Structure
project-root/
│
├─ main.py # FastAPI main app
├─ service/
│ ├─ products.py # Product CRUD logic
├─ schema/
│ ├─ product.py # Pydantic models for validation
├─ data/
│ ├─ products.json # JSON database
├─ static/
│ ├─ style.css # Frontend styling
│ ├─ main.webp # Hero image
├─ templates/
│ ├─ add.html
│ ├─ update.html
│ ├─ list.html
│ ├─ delete.html
└─ README.md


---

## Technology Stack
- **Backend:** Python, FastAPI
- **Frontend:** HTML, CSS, JavaScript
- **Database:** JSON file
- **Validation:** Pydantic (built-in with FastAPI)
- **Server:** Uvicorn (FastAPI ASGI server)

---

## Usage
1. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
2. Open the frontend pages in the browser:
* add.html → Add a product
* list.html → View all products
* update.html → Update products
* delete.html → Delete products

4. All CRUD operations will reflect in the products.json file automatically.

---

Project Author: Sahil Bhatti
Date: 2026-01-12
