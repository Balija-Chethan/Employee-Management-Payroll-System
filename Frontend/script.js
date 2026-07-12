const API_BASE = '/api';

function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// ─── Employee Functions ───

async function loadEmployees() {
    try {
        const res = await fetch(`${API_BASE}/employees/`);
        const data = await res.json();
        const tbody = document.getElementById('employeeTableBody');
        if (!tbody) return;
        tbody.innerHTML = '';
        data.employees.forEach(emp => {
            tbody.innerHTML += `
                <tr>
                    <td>${emp.employee_id}</td>
                    <td>${emp.full_name}</td>
                    <td>${emp.email}</td>
                    <td>${emp.phone}</td>
                    <td>${emp.department}</td>
                    <td>${emp.designation}</td>
                    <td>${emp.joining_date}</td>
                    <td>₹${Number(emp.salary).toLocaleString()}</td>
                    <td class="action-buttons">
                        <button class="btn btn-edit" onclick="editEmployee('${emp._id}')">Edit</button>
                        <button class="btn btn-delete" onclick="deleteEmployee('${emp._id}')">Delete</button>
                    </td>
                </tr>
            `;
        });
    } catch (err) {
        showToast('Error loading employees', 'error');
    }
}

function toggleEmployeeForm() {
    const container = document.getElementById('employeeFormContainer');
    container.classList.toggle('hidden');
    if (!container.classList.contains('hidden')) {
        container.scrollIntoView({ behavior: 'smooth' });
    }
}

document.getElementById('employeeForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const editId = document.getElementById('emp_edit_id').value;
    const body = {
        full_name: document.getElementById('emp_name').value,
        email: document.getElementById('emp_email').value,
        phone: document.getElementById('emp_phone').value,
        department: document.getElementById('emp_department').value,
        designation: document.getElementById('emp_designation').value,
        joining_date: document.getElementById('emp_joining_date').value,
        salary: Number(document.getElementById('emp_salary').value),
    };

    try {
        if (editId) {
            await fetch(`${API_BASE}/employees/update/${editId}/`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            showToast('Employee updated successfully');
        } else {
            await fetch(`${API_BASE}/employees/add/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            showToast('Employee added successfully');
        }
        document.getElementById('employeeForm').reset();
        document.getElementById('emp_edit_id').value = '';
        document.getElementById('formTitle').textContent = 'Add Employee';
        document.getElementById('employeeFormContainer').classList.add('hidden');
        loadEmployees();
    } catch (err) {
        showToast('Error saving employee', 'error');
    }
});

async function editEmployee(id) {
    try {
        const res = await fetch(`${API_BASE}/employees/`);
        const data = await res.json();
        const emp = data.employees.find(e => e._id === id);
        if (!emp) return;

        document.getElementById('emp_edit_id').value = id;
        document.getElementById('emp_name').value = emp.full_name;
        document.getElementById('emp_email').value = emp.email;
        document.getElementById('emp_phone').value = emp.phone;
        document.getElementById('emp_department').value = emp.department;
        document.getElementById('emp_designation').value = emp.designation;
        document.getElementById('emp_joining_date').value = emp.joining_date;
        document.getElementById('emp_salary').value = emp.salary;
        document.getElementById('formTitle').textContent = 'Edit Employee';
        document.getElementById('employeeFormContainer').classList.remove('hidden');
        document.getElementById('employeeFormContainer').scrollIntoView({ behavior: 'smooth' });
    } catch (err) {
        showToast('Error loading employee data', 'error');
    }
}

function cancelEdit() {
    document.getElementById('employeeForm').reset();
    document.getElementById('emp_edit_id').value = '';
    document.getElementById('formTitle').textContent = 'Add Employee';
    document.getElementById('employeeFormContainer').classList.add('hidden');
}

async function deleteEmployee(id) {
    if (!confirm('Are you sure you want to delete this employee?')) return;
    try {
        await fetch(`${API_BASE}/employees/delete/${id}/`, { method: 'DELETE' });
        showToast('Employee deleted');
        loadEmployees();
    } catch (err) {
        showToast('Error deleting employee', 'error');
    }
}

// ─── Department Functions ───

async function loadDepartments() {
    try {
        const res = await fetch(`${API_BASE}/departments/`);
        const data = await res.json();
        const tbody = document.getElementById('departmentTableBody');
        if (!tbody) return;
        tbody.innerHTML = '';
        data.departments.forEach(dept => {
            tbody.innerHTML += `
                <tr>
                    <td>${dept.department_id}</td>
                    <td>${dept.department_name}</td>
                    <td>${dept.manager_name}</td>
                    <td>${dept.total_employees}</td>
                    <td>${dept.location}</td>
                    <td class="action-buttons">
                        <button class="btn btn-edit" onclick="editDepartment('${dept._id}')">Edit</button>
                        <button class="btn btn-delete" onclick="deleteDepartment('${dept._id}')">Delete</button>
                    </td>
                </tr>
            `;
        });
    } catch (err) {
        showToast('Error loading departments', 'error');
    }
}

function toggleDepartmentForm() {
    const container = document.getElementById('departmentFormContainer');
    container.classList.toggle('hidden');
    if (!container.classList.contains('hidden')) {
        container.scrollIntoView({ behavior: 'smooth' });
    }
}

document.getElementById('departmentForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const editId = document.getElementById('dept_edit_id').value;
    const body = {
        department_name: document.getElementById('dept_name').value,
        manager_name: document.getElementById('dept_manager').value,
        total_employees: Number(document.getElementById('dept_total').value),
        location: document.getElementById('dept_location').value,
    };

    try {
        if (editId) {
            await fetch(`${API_BASE}/departments/update/${editId}/`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            showToast('Department updated');
        } else {
            await fetch(`${API_BASE}/departments/add/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            showToast('Department added');
        }
        document.getElementById('departmentForm').reset();
        document.getElementById('dept_edit_id').value = '';
        document.getElementById('deptFormTitle').textContent = 'Add Department';
        document.getElementById('departmentFormContainer').classList.add('hidden');
        loadDepartments();
    } catch (err) {
        showToast('Error saving department', 'error');
    }
});

async function editDepartment(id) {
    try {
        const res = await fetch(`${API_BASE}/departments/`);
        const data = await res.json();
        const dept = data.departments.find(d => d._id === id);
        if (!dept) return;

        document.getElementById('dept_edit_id').value = id;
        document.getElementById('dept_name').value = dept.department_name;
        document.getElementById('dept_manager').value = dept.manager_name;
        document.getElementById('dept_total').value = dept.total_employees;
        document.getElementById('dept_location').value = dept.location;
        document.getElementById('deptFormTitle').textContent = 'Edit Department';
        document.getElementById('departmentFormContainer').classList.remove('hidden');
        document.getElementById('departmentFormContainer').scrollIntoView({ behavior: 'smooth' });
    } catch (err) {
        showToast('Error loading department data', 'error');
    }
}

function cancelDeptEdit() {
    document.getElementById('departmentForm').reset();
    document.getElementById('dept_edit_id').value = '';
    document.getElementById('deptFormTitle').textContent = 'Add Department';
    document.getElementById('departmentFormContainer').classList.add('hidden');
}

async function deleteDepartment(id) {
    if (!confirm('Are you sure you want to delete this department?')) return;
    try {
        await fetch(`${API_BASE}/departments/delete/${id}/`, { method: 'DELETE' });
        showToast('Department deleted');
        loadDepartments();
    } catch (err) {
        showToast('Error deleting department', 'error');
    }
}

// ─── Attendance Functions ───

async function loadAttendance() {
    try {
        const res = await fetch(`${API_BASE}/attendance/`);
        const data = await res.json();
        const tbody = document.getElementById('attendanceTableBody');
        if (!tbody) return;
        tbody.innerHTML = '';

        // Populate employee dropdown
        const empRes = await fetch(`${API_BASE}/employees/`);
        const empData = await empRes.json();
        const empSelect = document.getElementById('att_employee_name');
        if (empSelect && empSelect.options.length <= 1) {
            empData.employees.forEach(emp => {
                const opt = document.createElement('option');
                opt.value = emp.full_name;
                opt.textContent = emp.full_name;
                empSelect.appendChild(opt);
            });
        }

        data.attendance.forEach(att => {
            const statusClass = att.status === 'Present' ? 'badge-present' :
                                att.status === 'Absent' ? 'badge-absent' : 'badge-leave';
            tbody.innerHTML += `
                <tr>
                    <td>${att.attendance_id}</td>
                    <td>${att.employee_name}</td>
                    <td>${att.attendance_date}</td>
                    <td>${att.check_in || '-'}</td>
                    <td>${att.check_out || '-'}</td>
                    <td><span class="badge ${statusClass}">${att.status}</span></td>
                    <td class="action-buttons">
                        <button class="btn btn-edit" onclick="editAttendance('${att._id}')">Edit</button>
                        <button class="btn btn-delete" onclick="deleteAttendance('${att._id}')">Delete</button>
                    </td>
                </tr>
            `;
        });
    } catch (err) {
        showToast('Error loading attendance', 'error');
    }
}

function toggleAttendanceForm() {
    const container = document.getElementById('attendanceFormContainer');
    container.classList.toggle('hidden');
    if (!container.classList.contains('hidden')) {
        container.scrollIntoView({ behavior: 'smooth' });
    }
}

document.getElementById('attendanceForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const editId = document.getElementById('att_edit_id').value;
    const body = {
        employee_name: document.getElementById('att_employee_name').value,
        attendance_date: document.getElementById('att_date').value,
        check_in: document.getElementById('att_check_in').value,
        check_out: document.getElementById('att_check_out').value,
        status: document.getElementById('att_status').value,
    };

    try {
        if (editId) {
            await fetch(`${API_BASE}/attendance/update/${editId}/`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            showToast('Attendance updated');
        } else {
            await fetch(`${API_BASE}/attendance/add/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            showToast('Attendance marked');
        }
        document.getElementById('attendanceForm').reset();
        document.getElementById('att_edit_id').value = '';
        document.getElementById('attFormTitle').textContent = 'Mark Attendance';
        document.getElementById('attendanceFormContainer').classList.add('hidden');
        loadAttendance();
    } catch (err) {
        showToast('Error saving attendance', 'error');
    }
});

async function editAttendance(id) {
    try {
        const res = await fetch(`${API_BASE}/attendance/`);
        const data = await res.json();
        const att = data.attendance.find(a => a._id === id);
        if (!att) return;

        document.getElementById('att_edit_id').value = id;
        document.getElementById('att_employee_name').value = att.employee_name;
        document.getElementById('att_date').value = att.attendance_date;
        document.getElementById('att_check_in').value = att.check_in || '';
        document.getElementById('att_check_out').value = att.check_out || '';
        document.getElementById('att_status').value = att.status;
        document.getElementById('attFormTitle').textContent = 'Edit Attendance';
        document.getElementById('attendanceFormContainer').classList.remove('hidden');
        document.getElementById('attendanceFormContainer').scrollIntoView({ behavior: 'smooth' });
    } catch (err) {
        showToast('Error loading attendance data', 'error');
    }
}

function cancelAttEdit() {
    document.getElementById('attendanceForm').reset();
    document.getElementById('att_edit_id').value = '';
    document.getElementById('attFormTitle').textContent = 'Mark Attendance';
    document.getElementById('attendanceFormContainer').classList.add('hidden');
}

async function deleteAttendance(id) {
    if (!confirm('Delete this attendance record?')) return;
    try {
        await fetch(`${API_BASE}/attendance/delete/${id}/`, { method: 'DELETE' });
        showToast('Attendance deleted');
        loadAttendance();
    } catch (err) {
        showToast('Error deleting attendance', 'error');
    }
}

// ─── Payroll Functions ───

async function loadPayroll() {
    try {
        const res = await fetch(`${API_BASE}/payroll/`);
        const data = await res.json();
        const tbody = document.getElementById('payrollTableBody');
        if (!tbody) return;
        tbody.innerHTML = '';

        const empRes = await fetch(`${API_BASE}/employees/`);
        const empData = await empRes.json();
        const empSelect = document.getElementById('pay_employee_name');
        if (empSelect && empSelect.options.length <= 1) {
            empData.employees.forEach(emp => {
                const opt = document.createElement('option');
                opt.value = emp.full_name;
                opt.textContent = emp.full_name;
                empSelect.appendChild(opt);
            });
        }

        data.payroll.forEach(pay => {
            tbody.innerHTML += `
                <tr>
                    <td>${pay.payroll_id}</td>
                    <td>${pay.employee_name}</td>
                    <td>₹${Number(pay.basic_salary).toLocaleString()}</td>
                    <td>₹${Number(pay.bonus).toLocaleString()}</td>
                    <td>₹${Number(pay.deductions).toLocaleString()}</td>
                    <td><strong>₹${Number(pay.net_salary).toLocaleString()}</strong></td>
                    <td>${pay.payment_month}</td>
                    <td class="action-buttons">
                        <button class="btn btn-edit" onclick="editPayroll('${pay._id}')">Edit</button>
                        <button class="btn btn-delete" onclick="deletePayroll('${pay._id}')">Delete</button>
                    </td>
                </tr>
            `;
        });
    } catch (err) {
        showToast('Error loading payroll', 'error');
    }
}

function togglePayrollForm() {
    const container = document.getElementById('payrollFormContainer');
    container.classList.toggle('hidden');
    if (!container.classList.contains('hidden')) {
        container.scrollIntoView({ behavior: 'smooth' });
    }
}

document.getElementById('payrollForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const editId = document.getElementById('pay_edit_id').value;
    const body = {
        employee_name: document.getElementById('pay_employee_name').value,
        basic_salary: Number(document.getElementById('pay_basic_salary').value),
        bonus: Number(document.getElementById('pay_bonus').value),
        deductions: Number(document.getElementById('pay_deductions').value),
        payment_month: document.getElementById('pay_month').value,
    };

    try {
        if (editId) {
            await fetch(`${API_BASE}/payroll/update/${editId}/`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            showToast('Payroll updated');
        } else {
            await fetch(`${API_BASE}/payroll/add/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            showToast('Payroll added');
        }
        document.getElementById('payrollForm').reset();
        document.getElementById('pay_edit_id').value = '';
        document.getElementById('payFormTitle').textContent = 'Add Payroll Record';
        document.getElementById('payrollFormContainer').classList.add('hidden');
        loadPayroll();
    } catch (err) {
        showToast('Error saving payroll', 'error');
    }
});

async function editPayroll(id) {
    try {
        const res = await fetch(`${API_BASE}/payroll/`);
        const data = await res.json();
        const pay = data.payroll.find(p => p._id === id);
        if (!pay) return;

        document.getElementById('pay_edit_id').value = id;
        document.getElementById('pay_employee_name').value = pay.employee_name;
        document.getElementById('pay_basic_salary').value = pay.basic_salary;
        document.getElementById('pay_bonus').value = pay.bonus;
        document.getElementById('pay_deductions').value = pay.deductions;
        document.getElementById('pay_month').value = pay.payment_month;
        document.getElementById('payFormTitle').textContent = 'Edit Payroll Record';
        document.getElementById('payrollFormContainer').classList.remove('hidden');
        document.getElementById('payrollFormContainer').scrollIntoView({ behavior: 'smooth' });
    } catch (err) {
        showToast('Error loading payroll data', 'error');
    }
}

function cancelPayEdit() {
    document.getElementById('payrollForm').reset();
    document.getElementById('pay_edit_id').value = '';
    document.getElementById('payFormTitle').textContent = 'Add Payroll Record';
    document.getElementById('payrollFormContainer').classList.add('hidden');
}

async function deletePayroll(id) {
    if (!confirm('Delete this payroll record?')) return;
    try {
        await fetch(`${API_BASE}/payroll/delete/${id}/`, { method: 'DELETE' });
        showToast('Payroll deleted');
        loadPayroll();
    } catch (err) {
        showToast('Error deleting payroll', 'error');
    }
}

// ─── Payslip Functions ───

async function loadPayslips() {
    try {
        const res = await fetch(`${API_BASE}/payslips/`);
        const data = await res.json();
        const tbody = document.getElementById('payslipTableBody');
        if (!tbody) return;
        tbody.innerHTML = '';

        const empRes = await fetch(`${API_BASE}/employees/`);
        const empData = await empRes.json();
        const empSelect = document.getElementById('slip_employee_name');
        if (empSelect && empSelect.options.length <= 1) {
            empData.employees.forEach(emp => {
                const opt = document.createElement('option');
                opt.value = emp.full_name;
                opt.textContent = emp.full_name;
                empSelect.appendChild(opt);
            });
        }

        data.payslips.forEach(slip => {
            const statusClass = slip.payment_status === 'Paid' ? 'badge-paid' : 'badge-pending';
            tbody.innerHTML += `
                <tr>
                    <td>${slip.payslip_id}</td>
                    <td>${slip.employee_name}</td>
                    <td>${slip.payment_date}</td>
                    <td>${slip.payment_method}</td>
                    <td><span class="badge ${statusClass}">${slip.payment_status}</span></td>
                    <td>${slip.remarks}</td>
                    <td class="action-buttons">
                        <button class="btn btn-edit" onclick="editPayslip('${slip._id}')">Edit</button>
                        <button class="btn btn-delete" onclick="deletePayslip('${slip._id}')">Delete</button>
                    </td>
                </tr>
            `;
        });
    } catch (err) {
        showToast('Error loading payslips', 'error');
    }
}

function togglePayslipForm() {
    const container = document.getElementById('payslipFormContainer');
    container.classList.toggle('hidden');
    if (!container.classList.contains('hidden')) {
        container.scrollIntoView({ behavior: 'smooth' });
    }
}

document.getElementById('payslipForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const editId = document.getElementById('slip_edit_id').value;
    const body = {
        employee_name: document.getElementById('slip_employee_name').value,
        payment_date: document.getElementById('slip_payment_date').value,
        payment_method: document.getElementById('slip_payment_method').value,
        payment_status: document.getElementById('slip_payment_status').value,
        remarks: document.getElementById('slip_remarks').value,
    };

    try {
        if (editId) {
            await fetch(`${API_BASE}/payslips/update/${editId}/`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            showToast('Payslip updated');
        } else {
            await fetch(`${API_BASE}/payslips/add/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            showToast('Payslip added');
        }
        document.getElementById('payslipForm').reset();
        document.getElementById('slip_edit_id').value = '';
        document.getElementById('slipFormTitle').textContent = 'Add Salary Slip';
        document.getElementById('payslipFormContainer').classList.add('hidden');
        loadPayslips();
    } catch (err) {
        showToast('Error saving payslip', 'error');
    }
});

async function editPayslip(id) {
    try {
        const res = await fetch(`${API_BASE}/payslips/`);
        const data = await res.json();
        const slip = data.payslips.find(s => s._id === id);
        if (!slip) return;

        document.getElementById('slip_edit_id').value = id;
        document.getElementById('slip_employee_name').value = slip.employee_name;
        document.getElementById('slip_payment_date').value = slip.payment_date;
        document.getElementById('slip_payment_method').value = slip.payment_method;
        document.getElementById('slip_payment_status').value = slip.payment_status;
        document.getElementById('slip_remarks').value = slip.remarks;
        document.getElementById('slipFormTitle').textContent = 'Edit Salary Slip';
        document.getElementById('payslipFormContainer').classList.remove('hidden');
        document.getElementById('payslipFormContainer').scrollIntoView({ behavior: 'smooth' });
    } catch (err) {
        showToast('Error loading payslip data', 'error');
    }
}

function cancelSlipEdit() {
    document.getElementById('payslipForm').reset();
    document.getElementById('slip_edit_id').value = '';
    document.getElementById('slipFormTitle').textContent = 'Add Salary Slip';
    document.getElementById('payslipFormContainer').classList.add('hidden');
}

async function deletePayslip(id) {
    if (!confirm('Delete this payslip?')) return;
    try {
        await fetch(`${API_BASE}/payslips/delete/${id}/`, { method: 'DELETE' });
        showToast('Payslip deleted');
        loadPayslips();
    } catch (err) {
        showToast('Error deleting payslip', 'error');
    }
}

// ─── Dashboard ───

async function loadDashboard() {
    try {
        const res = await fetch(`${API_BASE}/dashboard/`);
        const data = await res.json();

        document.getElementById('dashTotalEmployees').textContent = data.total_employees;
        document.getElementById('dashTotalDepartments').textContent = data.total_departments;
        document.getElementById('dashPresent').textContent = data.attendance_summary.present;
        document.getElementById('dashAbsent').textContent = data.attendance_summary.absent;
        document.getElementById('dashLeave').textContent = data.attendance_summary.leave;
        document.getElementById('dashTotalPaid').textContent = '₹' + Number(data.payroll_summary.total_paid).toLocaleString();
        document.getElementById('dashPaid').textContent = data.salary_payments.paid;
        document.getElementById('dashPending').textContent = data.salary_payments.pending;
    } catch (err) {
        showToast('Error loading dashboard', 'error');
    }
}

async function seedData() {
    if (!confirm('Load sample data? This will replace all existing data.')) return;
    try {
        await fetch(`${API_BASE}/seed/`, { method: 'POST' });
        showToast('Sample data loaded successfully');
        loadDashboard();
    } catch (err) {
        showToast('Error loading sample data', 'error');
    }
}

// ─── Registration ───

document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const body = {
        full_name: document.getElementById('reg_name').value,
        email: document.getElementById('reg_email').value,
        phone: document.getElementById('reg_phone').value,
        department: document.getElementById('reg_department').value,
        designation: document.getElementById('reg_designation').value,
        joining_date: document.getElementById('reg_joining_date').value,
        salary: Number(document.getElementById('reg_salary').value),
    };

    try {
        const res = await fetch(`${API_BASE}/employees/add/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
        if (res.ok) {
            showToast('Registration successful!');
            document.getElementById('registerForm').reset();
        } else {
            const err = await res.json();
            showToast(err.error || 'Registration failed', 'error');
        }
    } catch (err) {
        showToast('Error during registration', 'error');
    }
});

// Load departments for registration dropdown
async function loadDepartmentsForReg() {
    try {
        const res = await fetch(`${API_BASE}/departments/`);
        const data = await res.json();
        const select = document.getElementById('reg_department');
        if (!select) return;
        data.departments.forEach(dept => {
            const opt = document.createElement('option');
            opt.value = dept.department_name;
            opt.textContent = dept.department_name;
            select.appendChild(opt);
        });
    } catch (err) {
        // Silently fail if backend not running
    }
}

loadDepartmentsForReg();
