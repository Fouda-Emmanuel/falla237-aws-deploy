from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, full_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        if not full_name:
            raise ValueError("Users must provide full name")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, full_name, password):
        user = self.create_user(email, username, full_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150,)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return self.email 


class Item(models.Model):

    STATUS_CHOICES = [

        ('lost', 'Lost'), ('found', 'Found')

    ]


    CATEGORY_CHOICES = [

        ('identity', 'Identity Documents'),         # ID cards, student cards, passports, etc.
        ('documents', 'Official Documents'),        # Certificates, land papers, etc.
        ('electronics', 'Electronics'),             # Phones, laptops, tablets, etc.
        ('clothing', 'Clothing & Accessories'),     # Shoes, clothes, hats, watches, jewelry
        ('personal_items', 'Personal Items'),       # Wallets, bags, keys, glasses
        ('transport', 'Transport Items'),           # Vehicle plates, helmets, etc.
        ('pets', 'Pets'),                           # Lost or found animals
        ('other', 'Other'),                         # Anything that doesn't fit above
]
    

    LOCATION_CHOICES = [

        ('yaounde', 'Yaoundé'),
        ('douala', 'Douala'),
        ('garoua', 'Garoua'),
        ('maroua', 'Maroua'),
        ('ngoundere', 'Ngaoundéré'),
        ('bamenda', 'Bamenda'),
        ('buea', 'Buea'),
        ('bertoua', 'Bertoua'),
        ('bafoussam', 'Bafoussam'),
        ('ebolowa', 'Ebolowa'),
        ('other', 'Other'),
        
    ]


    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES)
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    img = CloudinaryField('image')
    reward = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    contact_info = models.CharField(max_length=100)
    date_lost_or_found = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
        