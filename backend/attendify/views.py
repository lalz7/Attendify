from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
from .models import Employee, Attendance
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Matikan log TensorFlow
import tensorflow as tf
import tensorflow_hub as hub


@csrf_exempt
def login_employee(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validasi email dan password
        user = authenticate(username=email, password=password)
        if user is not None:
            return JsonResponse({'message': 'Login successful', 'user_id': user.id})
        else:
            return JsonResponse({'error': 'Invalid email or password'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def add_employee(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')  # Pastikan user_id dikirim dari frontend
        name = request.POST.get('name')
        email = request.POST.get('email')
        image_file = request.FILES.get('image')

        if not user_id or not User.objects.filter(id=user_id).exists():
            return JsonResponse({'error': 'User not authenticated'}, status=403)

        if not image_file:
            return JsonResponse({'error': 'No image provided'}, status=400)

        # Baca gambar
        image_data = tf.io.decode_image(image_file.read(), channels=3)
        image_data = tf.image.resize(image_data, (300, 300))
        image_data = tf.expand_dims(image_data, axis=0)  # Tambahkan batch dimension

        # Deteksi wajah
        result = detector(image_data)
        boxes = result["detection_boxes"].numpy()
        scores = result["detection_scores"].numpy()

        # Ambil wajah dengan skor tertinggi
        if len(scores[0]) == 0 or scores[0][0] < 0.5:
            return JsonResponse({'error': 'No face detected'}, status=400)

        # Simpan encoding wajah ke database
        face_encoding = tf.reduce_mean(image_data, axis=[1, 2]).numpy()  # Contoh encoding sederhana
        employee = Employee(
            name=name,
            email=email,
            face_encoding=face_encoding.tobytes()
        )
        employee.save()

        return JsonResponse({'message': 'Employee added successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def recognize_face(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')

        if not image_file:
            return JsonResponse({'error': 'No image provided'}, status=400)

        # Baca gambar
        image_data = tf.io.decode_image(image_file.read(), channels=3)
        image_data = tf.image.resize(image_data, (300, 300))
        image_data = tf.expand_dims(image_data, axis=0)  # Tambahkan batch dimension

        # Deteksi wajah
        result = detector(image_data)
        boxes = result["detection_boxes"].numpy()
        scores = result["detection_scores"].numpy()

        # Ambil wajah dengan skor tertinggi
        if len(scores[0]) == 0 or scores[0][0] < 0.5:
            return JsonResponse({'error': 'No face detected'}, status=400)

        # Buat encoding wajah
        face_encoding = tf.reduce_mean(image_data, axis=[1, 2]).numpy()  # Contoh encoding sederhana

        # Bandingkan dengan data wajah di database
        employees = Employee.objects.all()
        for employee in employees:
            known_encoding = np.frombuffer(employee.face_encoding, dtype=np.float32)
            distance = np.linalg.norm(known_encoding - face_encoding)
            if distance < 0.6:  # Threshold untuk pengenalan wajah
                # Catat absensi
                Attendance.objects.create(
                    employee=employee,
                    timestamp=datetime.now()
                )
                return JsonResponse({'message': f'Face recognized: {employee.name}, attendance recorded'})

        return JsonResponse({'error': 'Face not recognized'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def attendance_report(request):
    if request.method == 'GET':
        # Ambil semua data absensi
        attendance = Attendance.objects.select_related('employee').all()
        data = [
            {
                'employee_name': record.employee.name,
                'timestamp': record.timestamp
            }
            for record in attendance
        ]
        return JsonResponse({'attendance': data})

    return JsonResponse({'error': 'Invalid request method'}, status=405)