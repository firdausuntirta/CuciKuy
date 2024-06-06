from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class UserCuciKuy(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    nama = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nama']  # Assuming 'nama' is a required field for superuser creation.

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(UserCuciKuy, self).save(*args, **kwargs)

# class Price(models.Model):
#     jeniskendaraan = models.CharField(max_length=50, choices=[('motor', 'Motor'), ('mobil', 'Mobil')])
#     harga = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f'{self.jeniskendaraan} - {self.harga}'

class Price(models.Model):
    jeniskendaraan = models.CharField(max_length=50, choices=[('motor', 'Motor'), ('mobil', 'Mobil')], unique=True)
    harga = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.jeniskendaraan} - {self.harga}'


class Transaction(models.Model):
    transaction_date = models.DateField()
    pelanggan = models.CharField(max_length=100)
    jeniskendaraan = models.CharField(max_length=50, choices=[('motor', 'Motor'), ('mobil', 'Mobil')])
    idtransaction = models.AutoField(primary_key=True)
    price = models.ForeignKey(Price, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.idtransaction} - {self.transaction_date} - {self.pelanggan} - {self.jeniskendaraan} - {self.price.harga if self.price else "No Price"}'