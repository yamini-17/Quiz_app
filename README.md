
# **Quiz Application**

This is an online Quiz Application developed to efficiently manage users, quizzes, questions, results, and admin operations.

---

## **Project Description**

The Quiz Application helps users to:

* Register and log in securely
* Attempt quizzes with multiple questions
* View real-time scores and results
* Compete in leaderboards
* Admin can add/manage quizzes and questions

This application provides an intuitive interface for users to take quizzes and for admins to manage everything easily.

---
## **Project Features**

**Landing Page:** Clean introduction with overview, key statistics, and navigation to Login, Create Account, and Dashboard

**User Authentication:** Create account, login, and secure password handling

**Dashboard:** View quiz options, track progress, and access quiz-related pages

**About Page:** Provides platform purpose, learning benefits, and details about quiz categories

**Quiz & Results:** Attempt quizzes and instantly view auto-calculated scores and answers



---

## **Technology Used**

* **Frontend:** HTML, CSS, JavaScript (Templates)
* **Backend:** Flask (Python)
* **Database:** MySQL
* **Other Tools:** Git, GitHub, JWT, Bcrypt

---

## **Screenshots**

### **Dashboard**
![Dashboard](https://github.com/yamini-17/Quiz_app/blob/main/Screenshot%202025-11-18%20001132.png?raw=true)

The Dashboard gives users access to quiz categories, shows progress, and acts as the main navigation area for starting quizzes or viewing results.

### **Login / Register Pages**
![Login page](https://github.com/yamini-17/Quiz_app/blob/main/login%20page.jpg?raw=true)

These pages allow users to securely create an account or log in using their email and password, with proper validation and backend hashing.

### **About Page**
![About](https://github.com/yamini-17/Quiz_app/blob/main/Screenshot%202025-11-18%20001204.png?raw=true)

The About Page explains the purpose of the platform, learning benefits, and available quiz categories, helping users understand what the app offers.

### **Landing Page**
![Landing Page](https://github.com/yamini-17/Quiz_app/blob/main/Screenshot%202025-11-18%20001228.png?raw=true)

The Landing Page provides a clean introduction to the Quiz App, showing an overview, platform purpose, and quick navigation to Login, Create Account, and Dashboard.

### **Quiz & Results**
![Results](https://github.com/yamini-17/Quiz_app/blob/main/Screenshot%202025-11-18%20223654.png?raw=true)

Users can take quizzes and receive instantly calculated results, including score, correct answers, and performance summary.

---

## **How to Run**

### **Step 1: Clone the Repository**

Clone the project using Git or download the ZIP file:

```
git clone https://github.com/yamini-17/Quiz_app.git
cd Quiz_app
```

---

### **Step 2: Install Dependencies**

Install the required Python packages:

```
pip install -r backend/requirements.txt
```

---

### **Step 3: Set Up the Database**

Import the SQL schema:

1. Open MySQL
2. Run:

```
source database/schema.sql;
```

Update your `.env` file with MySQL credentials.

---

### **Step 4: Run the Application**

Start the Flask backend:

``
python backend/app.py
``

---

### **Step 5: Access the Application**

Once the server is running, open your browser and go to:

```
http://127.0.0.1:5000/
