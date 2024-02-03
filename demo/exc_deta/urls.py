from django.urls import path
from exc_deta import views
urlpatterns = [
    path('', views.home, name='home'),

    # Import and Export Data

    path('import_student/', views.import_students, name='import_student'),
    path('export_student/', views.export_students, name='export_student'),

    # List Data

    path('students_list/', views.list_student, name='students_list'),
]   
