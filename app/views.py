from django.shortcuts import render
from django.http import JsonResponse
import rsa

def handle(request):
    return render(request, 'index.html')

def process_number(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        
        # Generate RSA key pair
        public_key, private_key = rsa.newkeys(2048)

        # Encrypt the number using RSA public key
        encrypted_number = rsa.encrypt(number.encode(), public_key)

        # Convert the encrypted number to hexadecimal representation for JSON serialization
        encrypted_hash = encrypted_number.hex()
        
        # Send the encrypted hash as a response
        return JsonResponse({'response': encrypted_hash})

