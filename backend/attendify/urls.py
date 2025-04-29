from django.urls import path
from .views import login_employee, add_employee, recognize_face, attendance_report

urlpatterns = [
    path('api/login', login_employee),  # Endpoint untuk login karyawan
    path('api/add-employee', add_employee),  # Endpoint untuk pendaftaran wajah karyawan
    path('api/recognize-face', recognize_face),  # Endpoint untuk absensi karyawan
    path('api/attendance-report', attendance_report),  # Endpoint untuk laporan absensi admin
]