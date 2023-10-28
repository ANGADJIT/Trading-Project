from django.shortcuts import render
from MainApp.forms import UploadFileForm
from datetime import datetime, timedelta
import csv
from MainApp.models import Candle
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
import asyncio
import json


# all functions for for file operations


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            timeframe = form.cleaned_data['timeframe']
            uploaded_file = form.files['file']

            # check for file formats
            if not uploaded_file.name.endswith(('.txt', '.csv')):
                return JsonResponse({'error': 'Only Text and Csv files are allowed'})

            uploaded_data = []

            # store file on server
            storage = FileSystemStorage()

            filename = storage.save(uploaded_file.name, uploaded_file)

            # list for time
            times: list[str] = []

            # read file after storing from server
            with open(storage.path(filename), encoding='utf-8') as file:
                try:
                    reader = csv.DictReader(file)
                except:
                    return JsonResponse({'error':'Unable to parse file'})

                for row in reader:
                    # check in file for columns
                    try:
                        row['OPEN'] 
                        row['HIGH']
                        row['LOW']
                        row['CLOSE']
                        row['DATE']
                    except (KeyError):
                        return JsonResponse({'error' : 'File column(s) missing please check file and try again'})

                    # save time also
                    times.append(row['TIME'])

                    candle = Candle(
                        open=row['OPEN'],
                        high=row['HIGH'],
                        low=row['LOW'],
                        close=row['CLOSE'],
                        date=row['DATE']
                    )
                    uploaded_data.append(candle)

            return asyncio.run(process_candels(
                candels=uploaded_data, time_in_minutes=timeframe, times=times))

    else:
        return render(request, 'MainApp/index.html')


async def process_candels(candels: list[Candle], time_in_minutes: int, times: list[str]):

    processed_candels: list[Candle] = []

    current_interval_start = None

    for index, candel in enumerate(candels):
        date_str = f'{candel.date} {times[index]}'

        # split the format for datetime convertion
        year = date_str[:4]
        month = date_str[4:6]
        day = date_str[6:8]

        hour, minute = times[index].split(':')

        current_datetime = datetime(int(year), int(
            month), int(day), int(hour), int(minute))

        # Initialize the current_interval_start if it's None (first iteration)
        if current_interval_start is None:
            current_interval_start = current_datetime
            current_candle = {
                'open': float(candel.open),
                'high': float(candel.open),
                'low': float(candel.low),
                'close': float(candel.close),
            }
        elif current_datetime - current_interval_start >= timedelta(minutes=float(time_in_minutes)):
            # If the current interval has exceeded the desired timeframe, save the completed candle
            processed_candels.append(candel)

            # Initialize a new 10-minute interval
            current_interval_start = current_datetime
            current_candle = {
                'open': float(candel.open),
                'high': float(candel.high),
                'low': float(candel.low),
                'close': float(candel.close),
            }
        else:
            # Update the current candle with new price information
            current_candle['high'] = max(
                current_candle['high'], float(candel.high))
            current_candle['low'] = min(
                current_candle['low'], float(candel.low))
            current_candle['close'] = float(candel.close)

    candel_json: list[dict] = []

    # after cover the candels in json
    for p_candel in processed_candels:
        candel_json.append({
            'open': float(candel.open),
            'high': float(candel.high),
            'low': float(candel.low),
            'close': float(candel.close),
            'date': candel.date
        })

    # cover objects in json
    jsn: str = json.dumps(candel_json, indent=4)

    response = HttpResponse(jsn, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="candles.json"'

    return response
