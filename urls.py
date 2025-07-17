from django.urls import path

from myapp.views import *

# route
urlpatterns = [
    path('', home),
    path('students', students),
    path('students2', students2),
    path('info', info),
    path('data', data),
    path('pdf', pdf),
]
# winget install httpie