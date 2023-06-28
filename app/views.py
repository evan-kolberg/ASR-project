from django.shortcuts import render
from django.http import JsonResponse
from rsa import newkeys, encrypt
from django.views.decorators.csrf import csrf_exempt
from .models import data


# gens RSA key pair (outside of the function)
public_key, private_key = newkeys(2048)


def handle(request):
    return render(request, 'index.html', {'table_data': data.objects.order_by('-id')[:20]})


@csrf_exempt
def process_number(request):
    if request.method == 'POST':
        number = request.POST.get('number')

        # encrypt number using RSA public key
        encrypted_number = encrypt(number.encode(), public_key)

        # stores encrypted hash in the database
        data.objects.create(number=number, encrypted_hash=encrypted_number.hex())

        # sends encrypted number as response (raw bytes)
        return JsonResponse({'hash': encrypted_number.hex()})

