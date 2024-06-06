from django.urls import path
from .views import index, login_view, logout_view, transaksi, edit_transaction, delete_transaction, cetak_nota, get_transaction_data, datamaster

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('transaksi/', transaksi, name='transaksi'),
    path('transaksi/edit/<int:idtransaction>/', edit_transaction, name='edit_transaction'),
    path('transaksi/delete/<int:idtransaction>/', delete_transaction, name='delete_transaction'),
    path('transaksi/cetak/<int:idtransaction>/', cetak_nota, name='cetak_nota'),
    path('transaksi/data/<int:month>/', get_transaction_data, name='get_transaction_data'),
    path('datamaster/', datamaster, name='datamaster'),
]
