# Employee Management & Payroll System

A full-stack web application for managing employee records, departments, attendance, payroll, and salary slips.

## Technology Stack

- **Frontend:** HTML5, CSS3, JavaScript (ES6), Fetch API
- **Backend:** Django (Function-Based Views), REST APIs
- **Database:** MongoDB Atlas (PyMongo)
- **Communication:** REST API with JSON

## Project Structure

```
EmployeePayrollSystem/
├── Backend/
│   ├── manage.py
│   ├── .env
│   ├── requirements.txt
│   ├── db.py
│   ├── views.py
│   ├── urls.py
│   └── employee_payroll/
│       ├── __init__.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── Frontend/
│   ├── index.html
│   ├── employees.html
│   ├── departments.html
│   ├── attendance.html
│   ├── payroll.html
│   ├── payslips.html
│   ├── dashboard.html
│   ├── style.css
│   └── script.js
└── README.md
```

## Setup Instructions

### Backend

```bash
cd EmployeePayrollSystem/Backend
pip install -r requirements.txt
python manage.py runserver
```

The backend runs at `http://127.0.0.1:8000`

### Frontend

Open `Frontend/index.html` in a browser, or serve using:

```bash
cd EmployeePayrollSystem/Frontend
python -m http.server 8080
```

## API Endpoints (20 Total)

### Employee APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/employees/add/` | Add new employee |
| GET | `/api/employees/` | Get all employees |
| PUT | `/api/employees/update/<id>/` | Update employee |
| DELETE | `/api/employees/delete/<id>/` | Delete employee |

### Department APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/departments/add/` | Add new department |
| GET | `/api/departments/` | Get all departments |
| PUT | `/api/departments/update/<id>/` | Update department |
| DELETE | `/api/departments/delete/<id>/` | Delete department |

### Attendance APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/attendance/add/` | Mark attendance |
| GET | `/api/attendance/` | Get all attendance |
| PUT | `/api/attendance/update/<id>/` | Update attendance |
| DELETE | `/api/attendance/delete/<id>/` | Delete attendance |

### Payroll APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/payroll/add/` | Add payroll record |
| GET | `/api/payroll/` | Get all payroll records |
| PUT | `/api/payroll/update/<id>/` | Update payroll |
| DELETE | `/api/payroll/delete/<id>/` | Delete payroll |

### Salary Slip APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/payslips/add/` | Add salary slip |
| GET | `/api/payslips/` | Get all salary slips |
| PUT | `/api/payslips/update/<id>/` | Update salary slip |
| DELETE | `/api/payslips/delete/<id>/` | Delete salary slip |

### Utility APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/` | Dashboard summary |
| POST | `/api/seed/` | Load sample data |

## Frontend Pages

- **Home** (`index.html`) - Landing page with registration form
- **Employees** (`employees.html`) - Employee CRUD management
- **Departments** (`departments.html`) - Department CRUD management
- **Attendance** (`attendance.html`) - Attendance tracking
- **Payroll** (`payroll.html`) - Payroll processing
- **Salary Slips** (`payslips.html`) - Salary slip management
- **Dashboard** (`dashboard.html`) - Admin dashboard with analytics

## Sample Data

Click "Load Sample Data" on the dashboard to seed:
- 5 Employees
- 4 Departments
- 5 Attendance records
- 5 Payroll records
- 5 Salary slips

## Environment Variables (.env)

```
DJANGO_SECRET_KEY=your-secret-key
MONGODB_URI=mongodb+srv://...
MONGODB_DB_NAME=EmployeePayrollDB
```
