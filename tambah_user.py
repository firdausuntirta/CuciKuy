import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uas_cucikendaraan.settings")
django.setup()

from cucikendaraan.models import UserCuciKuy

def tambah_user():
    nama = input("Nama: ")
    username = input("Username: ")
    password = input("Password: ")

    new_user = UserCuciKuy(nama=nama, username=username, password=password)
    new_user.save()

    print(f"User {username} berhasil ditambahkan.")

if __name__ == "__main__":
    tambah_user()
