from django.urls import path
from MainApp.views import upload_file

app_name = 'MainApp'

urlpatterns = [
    path('', upload_file, name='upload_file'),
]
