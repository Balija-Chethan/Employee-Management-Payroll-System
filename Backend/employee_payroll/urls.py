from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('api/', include('urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('index.html', TemplateView.as_view(template_name='index.html')),
    path('employees/', TemplateView.as_view(template_name='employees.html'), name='employees'),
    path('employees.html', TemplateView.as_view(template_name='employees.html')),
    path('departments/', TemplateView.as_view(template_name='departments.html'), name='departments'),
    path('departments.html', TemplateView.as_view(template_name='departments.html')),
    path('attendance/', TemplateView.as_view(template_name='attendance.html'), name='attendance'),
    path('attendance.html', TemplateView.as_view(template_name='attendance.html')),
    path('payroll/', TemplateView.as_view(template_name='payroll.html'), name='payroll'),
    path('payroll.html', TemplateView.as_view(template_name='payroll.html')),
    path('payslips/', TemplateView.as_view(template_name='payslips.html'), name='payslips'),
    path('payslips.html', TemplateView.as_view(template_name='payslips.html')),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('dashboard.html', TemplateView.as_view(template_name='dashboard.html')),
]
