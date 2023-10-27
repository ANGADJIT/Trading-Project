from django.shortcuts import render
from MainApp.forms import UploadFileForm
from io import TextIOWrapper
import csv
from MainApp.models import Candle
from django.http import JsonResponse

# all functions for for file operations


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            timeframe = form.cleaned_data['timeframe']
            uploaded_file = form.cleaned_data['file']
            uploaded_data = []

            # write file here
            with open('media/' + uploaded_file.name, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # read file after storing from server
            with TextIOWrapper(uploaded_file, encoding='utf-8') as text_file:
                reader = csv.DictReader(text_file)
                for row in reader:
                    candle = Candle(
                        open=row['OPEN'],
                        high=row['HIGH'],
                        low=row['LOW'],
                        close=row['CLOSE'],
                        date=row['DATE']
                    )
                    uploaded_data.append(candle)

            return JsonResponse({'message': f'check data {uploaded_data[0].open}'})
    else:
        return render(request, 'MainApp/index.html')
