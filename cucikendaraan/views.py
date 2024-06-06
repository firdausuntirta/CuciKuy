from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import UserCuciKuy, Transaction, Price
from .forms import TransactionForm, UserCuciKuyCreationForm, PriceForm
from django.http import HttpResponse, JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import calendar

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    else:
        return render(request, 'login.html')

@login_required
def transaksi(request):
    transactions = Transaction.objects.all()
    bulan = request.GET.get('bulan')
    hari = request.GET.get('hari')

    if bulan and hari:
        transactions = transactions.filter(transaction_date__month=bulan, transaction_date__day=hari)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            jeniskendaraan = form.cleaned_data['jeniskendaraan']
            prices = Price.objects.filter(jeniskendaraan=jeniskendaraan)
            if prices.exists():
                transaction.price = prices.first()  # Choose the first Price object found
            else:
                transaction.price = None  # or handle the case where price is not found
            transaction.save()
            return redirect('transaksi')
    else:
        form = TransactionForm()

    return render(request, 'transaksi.html', {'form': form, 'transactions': transactions})

@login_required
def edit_transaction(request, idtransaction):
    transaction = get_object_or_404(Transaction, idtransaction=idtransaction)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaksi')
        else:
            return redirect('transaksi')
    return redirect('transaksi')

@login_required
def delete_transaction(request, idtransaction):
    transaction = get_object_or_404(Transaction, idtransaction=idtransaction)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaksi')
    return redirect('transaksi')


@login_required
def cetak_nota(request, idtransaction):
    transaction = get_object_or_404(Transaction, idtransaction=idtransaction)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setTitle("Nota Transaksi")

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "CuciKUY!")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, 730, "Alamat: Jl. Testing")
    
    # Transaction details
    p.setFont("Helvetica", 12)
    p.drawString(100, 700, f"Nota Transaksi #{transaction.idtransaction}")
    p.drawString(100, 680, f"Nama Pelanggan: {transaction.pelanggan}")
    p.drawString(100, 660, f"Jenis Kendaraan: {transaction.jeniskendaraan}")
    p.drawString(100, 640, f"Harga: {transaction.price.harga if transaction.price else 'Harga tidak tersedia'}")
    p.drawString(100, 620, f"Tanggal Transaksi: {transaction.transaction_date.strftime('%B %d, %Y')}")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

@login_required
def get_transaction_data(request, month):
    month = int(month)
    transactions = Transaction.objects.filter(transaction_date__month=month)
    days_in_month = calendar.monthrange(2024, month)[1]

    data = [0] * days_in_month
    for transaction in transactions:
        day = transaction.transaction_date.day
        data[day - 1] += 1

    return JsonResponse(data, safe=False)

@login_required
def datamaster(request):
    user_form = UserCuciKuyCreationForm()
    price_form = PriceForm()

    if request.method == 'POST':
        if 'username' in request.POST:
            user_form = UserCuciKuyCreationForm(request.POST)
            if user_form.is_valid():
                user_form.save()
                return redirect('datamaster')
        elif 'jeniskendaraan' in request.POST:
            price_form = PriceForm(request.POST)
            if price_form.is_valid():
                price_form.save()
                return redirect('datamaster')
        elif 'edit_username' in request.POST:
            user_id = request.POST.get('user_id')
            user = get_object_or_404(UserCuciKuy, id=user_id)
            user.username = request.POST.get('edit_username')
            user.nama = request.POST.get('edit_nama')
            user.save()
            return redirect('datamaster')
        elif 'edit_jeniskendaraan' in request.POST:
            price_id = request.POST.get('price_id')
            price = get_object_or_404(Price, id=price_id)
            price.jeniskendaraan = request.POST.get('edit_jeniskendaraan')
            price.harga = request.POST.get('edit_harga')
            price.save()
            return redirect('datamaster')
        elif 'delete_user_id' in request.POST:
            user_id = request.POST.get('delete_user_id')
            user = get_object_or_404(UserCuciKuy, id=user_id)
            user.delete()
            return redirect('datamaster')
        elif 'delete_price_id' in request.POST:
            price_id = request.POST.get('delete_price_id')
            price = get_object_or_404(Price, id=price_id)
            price.delete()
            return redirect('datamaster')
    
    users = UserCuciKuy.objects.all()
    prices = Price.objects.all()
    return render(request, 'datamaster.html', {'user_form': user_form, 'price_form': price_form, 'users': users, 'prices': prices})

