from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import data
from django.utils import timezone


# gives html file and most recent 20 items in db
def handle(request):
    return render(request, 'index.html', {'table_data': data.objects.order_by('-id')[:20]})


@csrf_exempt
def process_hash(request):
    if request.method == 'POST':
        hash = request.POST.get('hash')
        number = timezone.now

        # Store the encrypted hash in the database
        data.objects.create(number=number, encrypted_hash=hash)

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})  # Add a response for non-POST requests

