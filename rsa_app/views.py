from django.shortcuts import render, redirect
from .models import RSAHistory
from .rsa_engine import generate_rsa_keys

def home_view(request):
    error_msg = None
    
    if request.method == 'POST':
        try:
            # 1. Grab custom primes and the secret number from the user's form
            p = int(request.POST.get('p'))
            q = int(request.POST.get('q'))
            number = int(request.POST.get('number'))
            
            # 2. Generate the keys based on the user's chosen primes
            keys = generate_rsa_keys(p, q)
            
            # 3. Encrypt the number using the generated public keys
            encrypted_num = pow(number, keys['public_e'], keys['public_n'])
            
            # 4. Save exactly to your custom model layout
            record = RSAHistory.objects.create(
                public_key_n=keys['public_n'],
                public_key_e=keys['public_e'],
                private_key_d=keys['private_d'],
                original_number=number,
                encrypted_number=encrypted_num
            )
            
            # 5. Save the database ID to session and move to the next page
            request.session['current_record_id'] = record.id
            return redirect('encrypt_view')
            
        except ValueError as e:
            # If they enter non-primes, this catches the error from your engine!
            error_msg = str(e)

    # We pass the error_msg to the template so the user knows what went wrong
    return render(request, 'rsa_app/home.html', {'error_msg': error_msg})

def encrypt_view(request):
    record_id = request.session.get('current_record_id')
    if not record_id:
        return redirect('home_view')
        
    record = RSAHistory.objects.get(id=record_id)
    
    if request.method == 'POST':
        return redirect('decrypt_view')
        
    return render(request, 'rsa_app/encrypt.html', {'record': record})

def decrypt_view(request):
    record_id = request.session.get('current_record_id')
    if not record_id:
        return redirect('home_view')
        
    record = RSAHistory.objects.get(id=record_id)
    
    # Decrypt using the private key: M = (C^d) % n
    decrypted_num = pow(record.encrypted_number, record.private_key_d, record.public_key_n)
    
    if request.method == 'POST':
        request.session.flush()
        return redirect('home_view')
        
    return render(request, 'rsa_app/decrypt.html', {
        'record': record, 
        'decrypted_num': decrypted_num
    })