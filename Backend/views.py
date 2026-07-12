import json
from datetime import datetime
from bson import ObjectId
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from db import get_collection


def serialize_doc(doc):
    if doc is None:
        return None
    doc['_id'] = str(doc['_id'])
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
        elif isinstance(value, datetime):
            doc[key] = value.isoformat()
    return doc


# ─────────────────────────────────────────────
# MODULE 1: EMPLOYEE MANAGEMENT
# ─────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["POST"])
def add_employee(request):
    try:
        data = json.loads(request.body)
        required = ['full_name', 'email', 'phone', 'department', 'designation', 'joining_date', 'salary']
        for field in required:
            if field not in data:
                return JsonResponse({'error': f'{field} is required'}, status=400)

        collection = get_collection('employees')
        employee_id = collection.count_documents({}) + 101

        employee = {
            'employee_id': employee_id,
            'full_name': data['full_name'],
            'email': data['email'],
            'phone': data['phone'],
            'department': data['department'],
            'designation': data['designation'],
            'joining_date': data['joining_date'],
            'salary': data['salary'],
        }

        result = collection.insert_one(employee)
        employee['_id'] = str(result.inserted_id)

        return JsonResponse({'message': 'Employee added successfully', 'employee': employee}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_employees(request):
    try:
        collection = get_collection('employees')
        employees = []
        for emp in collection.find():
            employees.append(serialize_doc(emp))
        return JsonResponse({'employees': employees}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def update_employee(request, id):
    try:
        data = json.loads(request.body)
        collection = get_collection('employees')

        result = collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': data}
        )

        if result.matched_count == 0:
            return JsonResponse({'error': 'Employee not found'}, status=404)

        employee = collection.find_one({'_id': ObjectId(id)})
        return JsonResponse({'message': 'Employee updated successfully', 'employee': serialize_doc(employee)}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_employee(request, id):
    try:
        collection = get_collection('employees')
        result = collection.delete_one({'_id': ObjectId(id)})

        if result.deleted_count == 0:
            return JsonResponse({'error': 'Employee not found'}, status=404)

        return JsonResponse({'message': 'Employee deleted successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ─────────────────────────────────────────────
# MODULE 2: DEPARTMENT MANAGEMENT
# ─────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["POST"])
def add_department(request):
    try:
        data = json.loads(request.body)
        required = ['department_name', 'manager_name', 'total_employees', 'location']
        for field in required:
            if field not in data:
                return JsonResponse({'error': f'{field} is required'}, status=400)

        collection = get_collection('departments')
        department_id = collection.count_documents({}) + 201

        department = {
            'department_id': department_id,
            'department_name': data['department_name'],
            'manager_name': data['manager_name'],
            'total_employees': data['total_employees'],
            'location': data['location'],
        }

        result = collection.insert_one(department)
        department['_id'] = str(result.inserted_id)

        return JsonResponse({'message': 'Department added successfully', 'department': department}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_departments(request):
    try:
        collection = get_collection('departments')
        departments = []
        for dept in collection.find():
            departments.append(serialize_doc(dept))
        return JsonResponse({'departments': departments}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def update_department(request, id):
    try:
        data = json.loads(request.body)
        collection = get_collection('departments')

        result = collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': data}
        )

        if result.matched_count == 0:
            return JsonResponse({'error': 'Department not found'}, status=404)

        department = collection.find_one({'_id': ObjectId(id)})
        return JsonResponse({'message': 'Department updated successfully', 'department': serialize_doc(department)}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_department(request, id):
    try:
        collection = get_collection('departments')
        result = collection.delete_one({'_id': ObjectId(id)})

        if result.deleted_count == 0:
            return JsonResponse({'error': 'Department not found'}, status=404)

        return JsonResponse({'message': 'Department deleted successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ─────────────────────────────────────────────
# MODULE 3: ATTENDANCE MANAGEMENT
# ─────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["POST"])
def add_attendance(request):
    try:
        data = json.loads(request.body)
        required = ['employee_name', 'attendance_date', 'check_in', 'check_out', 'status']
        for field in required:
            if field not in data:
                return JsonResponse({'error': f'{field} is required'}, status=400)

        if data['status'] not in ['Present', 'Absent', 'Leave']:
            return JsonResponse({'error': 'Status must be Present, Absent, or Leave'}, status=400)

        collection = get_collection('attendance')
        attendance_id = collection.count_documents({}) + 301

        attendance = {
            'attendance_id': attendance_id,
            'employee_name': data['employee_name'],
            'attendance_date': data['attendance_date'],
            'check_in': data['check_in'],
            'check_out': data['check_out'],
            'status': data['status'],
        }

        result = collection.insert_one(attendance)
        attendance['_id'] = str(result.inserted_id)

        return JsonResponse({'message': 'Attendance added successfully', 'attendance': attendance}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_attendance(request):
    try:
        collection = get_collection('attendance')
        records = []
        for rec in collection.find():
            records.append(serialize_doc(rec))
        return JsonResponse({'attendance': records}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def update_attendance(request, id):
    try:
        data = json.loads(request.body)
        collection = get_collection('attendance')

        result = collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': data}
        )

        if result.matched_count == 0:
            return JsonResponse({'error': 'Attendance record not found'}, status=404)

        attendance = collection.find_one({'_id': ObjectId(id)})
        return JsonResponse({'message': 'Attendance updated successfully', 'attendance': serialize_doc(attendance)}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_attendance(request, id):
    try:
        collection = get_collection('attendance')
        result = collection.delete_one({'_id': ObjectId(id)})

        if result.deleted_count == 0:
            return JsonResponse({'error': 'Attendance record not found'}, status=404)

        return JsonResponse({'message': 'Attendance deleted successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ─────────────────────────────────────────────
# MODULE 4: PAYROLL MANAGEMENT
# ─────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["POST"])
def add_payroll(request):
    try:
        data = json.loads(request.body)
        required = ['employee_name', 'basic_salary', 'bonus', 'deductions', 'payment_month']
        for field in required:
            if field not in data:
                return JsonResponse({'error': f'{field} is required'}, status=400)

        net_salary = data['basic_salary'] + data['bonus'] - data['deductions']

        collection = get_collection('payroll')
        payroll_id = collection.count_documents({}) + 401

        payroll = {
            'payroll_id': payroll_id,
            'employee_name': data['employee_name'],
            'basic_salary': data['basic_salary'],
            'bonus': data['bonus'],
            'deductions': data['deductions'],
            'net_salary': net_salary,
            'payment_month': data['payment_month'],
        }

        result = collection.insert_one(payroll)
        payroll['_id'] = str(result.inserted_id)

        return JsonResponse({'message': 'Payroll added successfully', 'payroll': payroll}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_payroll(request):
    try:
        collection = get_collection('payroll')
        records = []
        for rec in collection.find():
            records.append(serialize_doc(rec))
        return JsonResponse({'payroll': records}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def update_payroll(request, id):
    try:
        data = json.loads(request.body)
        collection = get_collection('payroll')

        if 'basic_salary' in data and 'bonus' in data and 'deductions' in data:
            data['net_salary'] = data['basic_salary'] + data['bonus'] - data['deductions']

        result = collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': data}
        )

        if result.matched_count == 0:
            return JsonResponse({'error': 'Payroll record not found'}, status=404)

        payroll = collection.find_one({'_id': ObjectId(id)})
        return JsonResponse({'message': 'Payroll updated successfully', 'payroll': serialize_doc(payroll)}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_payroll(request, id):
    try:
        collection = get_collection('payroll')
        result = collection.delete_one({'_id': ObjectId(id)})

        if result.deleted_count == 0:
            return JsonResponse({'error': 'Payroll record not found'}, status=404)

        return JsonResponse({'message': 'Payroll deleted successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ─────────────────────────────────────────────
# MODULE 5: SALARY SLIP MANAGEMENT
# ─────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["POST"])
def add_payslip(request):
    try:
        data = json.loads(request.body)
        required = ['employee_name', 'payment_date', 'payment_method', 'payment_status', 'remarks']
        for field in required:
            if field not in data:
                return JsonResponse({'error': f'{field} is required'}, status=400)

        if data['payment_method'] not in ['Bank Transfer', 'UPI', 'Cash']:
            return JsonResponse({'error': 'Payment method must be Bank Transfer, UPI, or Cash'}, status=400)
        if data['payment_status'] not in ['Paid', 'Pending']:
            return JsonResponse({'error': 'Payment status must be Paid or Pending'}, status=400)

        collection = get_collection('payslips')
        payslip_id = collection.count_documents({}) + 501

        payslip = {
            'payslip_id': payslip_id,
            'employee_name': data['employee_name'],
            'payment_date': data['payment_date'],
            'payment_method': data['payment_method'],
            'payment_status': data['payment_status'],
            'remarks': data['remarks'],
        }

        result = collection.insert_one(payslip)
        payslip['_id'] = str(result.inserted_id)

        return JsonResponse({'message': 'Payslip added successfully', 'payslip': payslip}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_payslips(request):
    try:
        collection = get_collection('payslips')
        records = []
        for rec in collection.find():
            records.append(serialize_doc(rec))
        return JsonResponse({'payslips': records}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def update_payslip(request, id):
    try:
        data = json.loads(request.body)
        collection = get_collection('payslips')

        result = collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': data}
        )

        if result.matched_count == 0:
            return JsonResponse({'error': 'Payslip not found'}, status=404)

        payslip = collection.find_one({'_id': ObjectId(id)})
        return JsonResponse({'message': 'Payslip updated successfully', 'payslip': serialize_doc(payslip)}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_payslip(request, id):
    try:
        collection = get_collection('payslips')
        result = collection.delete_one({'_id': ObjectId(id)})

        if result.deleted_count == 0:
            return JsonResponse({'error': 'Payslip not found'}, status=404)

        return JsonResponse({'message': 'Payslip deleted successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ─────────────────────────────────────────────
# DASHBOARD SUMMARY
# ─────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["GET"])
def dashboard_summary(request):
    try:
        employees_count = get_collection('employees').count_documents({})
        departments_count = get_collection('departments').count_documents({})
        attendance_records = list(get_collection('attendance').find())
        payroll_records = list(get_collection('payroll').find())

        total_paid = sum(r.get('net_salary', 0) for r in payroll_records)
        present_count = sum(1 for r in attendance_records if r.get('status') == 'Present')
        absent_count = sum(1 for r in attendance_records if r.get('status') == 'Absent')
        leave_count = sum(1 for r in attendance_records if r.get('status') == 'Leave')
        total_attendance = len(attendance_records)

        payslip_records = list(get_collection('payslips').find())
        paid_count = sum(1 for p in payslip_records if p.get('payment_status') == 'Paid')
        pending_count = sum(1 for p in payslip_records if p.get('payment_status') == 'Pending')

        return JsonResponse({
            'total_employees': employees_count,
            'total_departments': departments_count,
            'attendance_summary': {
                'total': total_attendance,
                'present': present_count,
                'absent': absent_count,
                'leave': leave_count,
            },
            'payroll_summary': {
                'total_records': len(payroll_records),
                'total_paid': total_paid,
            },
            'salary_payments': {
                'total': len(payslip_records),
                'paid': paid_count,
                'pending': pending_count,
            }
        }, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ─────────────────────────────────────────────
# SEED SAMPLE DATA
# ─────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["POST"])
def seed_data(request):
    try:
        employees_col = get_collection('employees')
        departments_col = get_collection('departments')
        attendance_col = get_collection('attendance')
        payroll_col = get_collection('payroll')
        payslips_col = get_collection('payslips')

        employees_col.drop()
        departments_col.drop()
        attendance_col.drop()
        payroll_col.drop()
        payslips_col.drop()

        employees = [
            {
                'employee_id': 101, 'full_name': 'Rahul Sharma', 'email': 'rahul@gmail.com',
                'phone': '9876543210', 'department': 'Software Development', 'designation': 'Python Developer',
                'joining_date': '2026-01-15', 'salary': 60000,
            },
            {
                'employee_id': 102, 'full_name': 'Priya Patel', 'email': 'priya@gmail.com',
                'phone': '9876543211', 'department': 'Human Resources', 'designation': 'HR Manager',
                'joining_date': '2025-06-01', 'salary': 55000,
            },
            {
                'employee_id': 103, 'full_name': 'Amit Kumar', 'email': 'amit@gmail.com',
                'phone': '9876543212', 'department': 'Marketing', 'designation': 'Marketing Lead',
                'joining_date': '2025-09-10', 'salary': 50000,
            },
            {
                'employee_id': 104, 'full_name': 'Sneha Reddy', 'email': 'sneha@gmail.com',
                'phone': '9876543213', 'department': 'Finance', 'designation': 'Accountant',
                'joining_date': '2026-03-20', 'salary': 48000,
            },
            {
                'employee_id': 105, 'full_name': 'Vikram Singh', 'email': 'vikram@gmail.com',
                'phone': '9876543214', 'department': 'Software Development', 'designation': 'Frontend Developer',
                'joining_date': '2026-02-01', 'salary': 55000,
            },
        ]
        employees_col.insert_many(employees)

        departments = [
            {
                'department_id': 201, 'department_name': 'Software Development',
                'manager_name': 'Anjali Verma', 'total_employees': 15, 'location': 'Bangalore',
            },
            {
                'department_id': 202, 'department_name': 'Human Resources',
                'manager_name': 'Rajesh Gupta', 'total_employees': 5, 'location': 'Hyderabad',
            },
            {
                'department_id': 203, 'department_name': 'Marketing',
                'manager_name': 'Neha Joshi', 'total_employees': 8, 'location': 'Mumbai',
            },
            {
                'department_id': 204, 'department_name': 'Finance',
                'manager_name': 'Suresh Nair', 'total_employees': 6, 'location': 'Delhi',
            },
        ]
        departments_col.insert_many(departments)

        attendance = [
            {
                'attendance_id': 301, 'employee_name': 'Rahul Sharma', 'attendance_date': '2026-07-15',
                'check_in': '09:00', 'check_out': '18:00', 'status': 'Present',
            },
            {
                'attendance_id': 302, 'employee_name': 'Priya Patel', 'attendance_date': '2026-07-15',
                'check_in': '09:15', 'check_out': '18:10', 'status': 'Present',
            },
            {
                'attendance_id': 303, 'employee_name': 'Amit Kumar', 'attendance_date': '2026-07-15',
                'check_in': '', 'check_out': '', 'status': 'Absent',
            },
            {
                'attendance_id': 304, 'employee_name': 'Sneha Reddy', 'attendance_date': '2026-07-15',
                'check_in': '', 'check_out': '', 'status': 'Leave',
            },
            {
                'attendance_id': 305, 'employee_name': 'Vikram Singh', 'attendance_date': '2026-07-15',
                'check_in': '08:55', 'check_out': '17:50', 'status': 'Present',
            },
        ]
        attendance_col.insert_many(attendance)

        payroll = [
            {
                'payroll_id': 401, 'employee_name': 'Rahul Sharma', 'basic_salary': 60000,
                'bonus': 5000, 'deductions': 2000, 'net_salary': 63000, 'payment_month': 'July 2026',
            },
            {
                'payroll_id': 402, 'employee_name': 'Priya Patel', 'basic_salary': 55000,
                'bonus': 3000, 'deductions': 1500, 'net_salary': 56500, 'payment_month': 'July 2026',
            },
            {
                'payroll_id': 403, 'employee_name': 'Amit Kumar', 'basic_salary': 50000,
                'bonus': 2000, 'deductions': 1000, 'net_salary': 51000, 'payment_month': 'July 2026',
            },
            {
                'payroll_id': 404, 'employee_name': 'Sneha Reddy', 'basic_salary': 48000,
                'bonus': 1500, 'deductions': 1200, 'net_salary': 48300, 'payment_month': 'July 2026',
            },
            {
                'payroll_id': 405, 'employee_name': 'Vikram Singh', 'basic_salary': 55000,
                'bonus': 4000, 'deductions': 1800, 'net_salary': 57200, 'payment_month': 'July 2026',
            },
        ]
        payroll_col.insert_many(payroll)

        payslips = [
            {
                'payslip_id': 501, 'employee_name': 'Rahul Sharma', 'payment_date': '2026-07-31',
                'payment_method': 'Bank Transfer', 'payment_status': 'Paid',
                'remarks': 'Salary credited successfully',
            },
            {
                'payslip_id': 502, 'employee_name': 'Priya Patel', 'payment_date': '2026-07-31',
                'payment_method': 'Bank Transfer', 'payment_status': 'Paid',
                'remarks': 'Salary credited successfully',
            },
            {
                'payslip_id': 503, 'employee_name': 'Amit Kumar', 'payment_date': '2026-07-31',
                'payment_method': 'UPI', 'payment_status': 'Pending',
                'remarks': 'Awaiting UPI confirmation',
            },
            {
                'payslip_id': 504, 'employee_name': 'Sneha Reddy', 'payment_date': '2026-07-31',
                'payment_method': 'Cash', 'payment_status': 'Paid',
                'remarks': 'Cash payment handed over',
            },
            {
                'payslip_id': 505, 'employee_name': 'Vikram Singh', 'payment_date': '2026-07-31',
                'payment_method': 'Bank Transfer', 'payment_status': 'Paid',
                'remarks': 'Salary credited successfully',
            },
        ]
        payslips_col.insert_many(payslips)

        return JsonResponse({'message': 'Sample data seeded successfully'}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
