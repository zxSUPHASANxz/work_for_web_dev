import io
import sys
from datetime import date
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas

from myapp.models import Student

# Create your views here.
def home(request):
    response = HttpResponse('Welcome to Thailand')
    return response

def students(request):
    context = {}
    context['students'] = Student.objects.all()
    context['students'] = Student.objects.filter(name='Anna Aaaaa')  # Example filter
    context['students'] = Student.objects.filter(name__contains='Aaaaa')  # Example filter
    context['students'] = Student.objects.filter(name__icontains='Aaaaa')  # Example filter
    context['students'] = Student.objects.filter(name__startswith='Aaaaa')  # Example filter
    context['students'] = Student.objects.filter(name__endswith='Aaaaa')  # Example filter
    context['students'] = Student.objects.filter(name__in=['Anna Aaaaa', 'Benedict Bbbbbbb'])  # Example filter
    context['students'] = Student.objects.filter(name__regex=r'^A.*')  # Example filter using regex     
    context['students'] = Student.objects.filter(name__iregex=r'^A.*')  # Example filter using case-insensitive regex
    context['students'] = Student.objects.filter(name__icontains='Aaaaa', dob__year__gte=2000)  # Example filter with multiple conditions
    context['students'] = Student.objects.filter(name__icontains='Aaaaa').order_by('dob')  # Example filter with ordering
    context['students'] = Student.objects.filter(dob__range=(date(2000,1,1), date(2002,2,3))).order_by('-dob')  # Example filter with descending order
    context['students'] = Student.objects.filter(dob__year=2000).order_by('dob')  # Example filter by year
    context['students'] = Student.objects.filter(dob__month=1).order_by('dob')  # Example filter by month
    context['students'] = Student.objects.filter(dob__day=1).order_by('dob')  # Example filter by day
    context['students'] = Student.objects.filter(dob=date(2000,1,1))  # Example filter by year, month, and day
    context['students'] = Student.objects.exclude(dob__year=2000)   # Example exclude filter out by year
    context['students'] = Student.objects.exclude(name__icontains='ก').order_by('-dob')  # Example exclude filter out by name containing 'ก' and order by dob descending
    return render(request, 'myapp/students.html', context)

def students2(request):
    context = {}
    context['students'] = Student.objects.all()
    return render(request, 'myapp/students2.html', context)

def info(request):
    r = HttpResponse(sys.version)
    return r

def data(request):
    d = {
        '67000000': { 
            'first_name': 'Anna',
            'last_name': 'Aaaaa'
        },
        '67000001': {
            'first_name': 'Benedict',
            'last_name': 'Bbbbbbb'
        }
    }
    return JsonResponse(d)

def pdf(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "I am a PDF.")
    
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="hello.pdf")