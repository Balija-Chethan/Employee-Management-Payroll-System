from django.urls import path
from views import (
    add_employee, get_employees, update_employee, delete_employee,
    add_department, get_departments, update_department, delete_department,
    add_attendance, get_attendance, update_attendance, delete_attendance,
    add_payroll, get_payroll, update_payroll, delete_payroll,
    add_payslip, get_payslips, update_payslip, delete_payslip,
    dashboard_summary, seed_data,
)

urlpatterns = [
    # Employee APIs
    path('employees/add/', add_employee, name='add_employee'),
    path('employees/', get_employees, name='get_employees'),
    path('employees/update/<str:id>/', update_employee, name='update_employee'),
    path('employees/delete/<str:id>/', delete_employee, name='delete_employee'),

    # Department APIs
    path('departments/add/', add_department, name='add_department'),
    path('departments/', get_departments, name='get_departments'),
    path('departments/update/<str:id>/', update_department, name='update_department'),
    path('departments/delete/<str:id>/', delete_department, name='delete_department'),

    # Attendance APIs
    path('attendance/add/', add_attendance, name='add_attendance'),
    path('attendance/', get_attendance, name='get_attendance'),
    path('attendance/update/<str:id>/', update_attendance, name='update_attendance'),
    path('attendance/delete/<str:id>/', delete_attendance, name='delete_attendance'),

    # Payroll APIs
    path('payroll/add/', add_payroll, name='add_payroll'),
    path('payroll/', get_payroll, name='get_payroll'),
    path('payroll/update/<str:id>/', update_payroll, name='update_payroll'),
    path('payroll/delete/<str:id>/', delete_payroll, name='delete_payroll'),

    # Payslip APIs
    path('payslips/add/', add_payslip, name='add_payslip'),
    path('payslips/', get_payslips, name='get_payslips'),
    path('payslips/update/<str:id>/', update_payslip, name='update_payslip'),
    path('payslips/delete/<str:id>/', delete_payslip, name='delete_payslip'),

    # Dashboard & Seed
    path('dashboard/', dashboard_summary, name='dashboard_summary'),
    path('seed/', seed_data, name='seed_data'),
]
