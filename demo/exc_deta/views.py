from django.shortcuts import render,redirect
import pandas as pa
from exc_deta.forms import *
from exc_deta.models import *
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def home(request):
    return render(request, 'exc_deta/home.html')

# Import Data

def import_students(request):
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pa.read_excel(file)

            for _, row in df.iterrows():
                Student.objects.create(
                    name=row['name'],
                    age=row['age'],
                    roll_number=row['roll_number'],
                )

            return redirect('home')
            
    else:
        form = ImportForm()
    return render(request, 'exc_deta/import_students.html', {'form' : form})

# Export Data

def export_students(request):
    if request.method == 'POST':
        form = ExportForm(request.POST)
        if form.is_valid():
            students = Student.objects.all()

            df = pa.DataFrame(list(students.values()))
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="students.xlsx"'
            df.to_excel(response, index=False)

            return response
    else:

        form = ExportForm()

    return render(request, 'exc_deta/export_students.html', {'form' : form})

# List Data

def list_student(request):
    students = Student.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(students, 30)
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    return render(request, 'exc_deta/list_students.html', {'students' : students})
