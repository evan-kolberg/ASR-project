from django.shortcuts import render
from django.http import JsonResponse
from rsa import newkeys, encrypt
from .models import data

# Generate RSA key pair (outside of the function)
public_key, private_key = newkeys(2048)


def handle(request):
    return render(request, 'index.html', {'table_data': data.objects.all()})


def process_number(request):
    if request.method == 'POST':
        number = request.POST.get('number')

        # Convert number to bytes
        number_bytes = number.encode()  # Assuming number is a string

        # Encrypt number using RSA public key
        encrypted_number = encrypt(number_bytes, public_key)

        # Store the encrypted hash in the database
        data.objects.create(number=number, encrypted_hash=encrypted_number.hex())

        # Sends encrypted number as response (raw bytes)
        return JsonResponse({'response': encrypted_number.hex()})
