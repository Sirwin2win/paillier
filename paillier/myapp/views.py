from django.shortcuts import render, redirect
from .forms import NumberForm
from .models import EncryptedNumber
from .crypto import public_key, private_key
from phe import paillier

def home(request):
    if request.method == "POST":
        form = NumberForm(request.POST)

        if form.is_valid():
            number = form.cleaned_data["number"]

            # 🔐 Encrypt
            encrypted = public_key.encrypt(number)

            # 💾 Store
            EncryptedNumber.objects.create(
                encrypted_value=str(encrypted.ciphertext()),
                exponent=encrypted.exponent
            )

            return redirect("tally")

    else:
        form = NumberForm()

    return render(request, "myapp/home.html", {"form": form})

def tally_view(request):
    records = EncryptedNumber.objects.all()

    encrypted_total = None

    for r in records:
        enc = paillier.EncryptedNumber(
        public_key,
        int(r.encrypted_value),
        r.exponent
    )

    if encrypted_total is None:
        encrypted_total = enc
    else:
        encrypted_total += enc

        encrypted_total = enc if encrypted_total is None else encrypted_total + enc

    return render(request, "myapp/tally.html", {
        "encrypted_total": str(encrypted_total.ciphertext()) if encrypted_total else 0
    })



def decrypt_total(request):
    records = EncryptedNumber.objects.all()

    encrypted_total = None

    for r in records:
        enc = paillier.EncryptedNumber(
            public_key,
            int(r.encrypted_value),
            r.exponent
        )

        encrypted_total = enc if encrypted_total is None else encrypted_total + enc

    total = private_key.decrypt(encrypted_total) if encrypted_total else 0

    return render(request, "myapp/tally.html", {
        "decrypted_total": total
    })