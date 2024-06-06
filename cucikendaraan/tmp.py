import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uas_cucikendaraan.settings")
django.setup()

from cucikendaraan.models import Price

def tambah_harga():
    pilihan_kendaraan = input("Jenis Kendaraan (motor/mobil): ").strip().lower()
    
    if pilihan_kendaraan not in ['motor', 'mobil']:
        print("Jenis kendaraan tidak valid. Pilih 'motor' atau 'mobil'.")
        return
    
    # Harga otomatis berdasarkan jenis kendaraan
    if pilihan_kendaraan == 'motor':
        harga = 9000.00
    elif pilihan_kendaraan == 'mobil':
        harga = 20000.00
    
    new_price = Price(jeniskendaraan=pilihan_kendaraan, harga=harga)
    new_price.save()
    
    print(f"Harga untuk kendaraan '{pilihan_kendaraan}' berhasil ditambahkan dengan harga {harga}.")

if __name__ == "__main__":
    tambah_harga()
