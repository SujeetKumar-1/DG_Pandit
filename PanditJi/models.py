from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email or len(email)<=0:
            raise ValueError("email is required!")
        if not password:
            raise ValueError("password is required!")
        
        user=self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password):
        user=self.create_user(
            email=self.normalize_email(email), 
            password=password
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self.db)

        return user

class UserAccount(AbstractBaseUser):
    class Types(models.TextChoices):
        SUPERUSER="SUPERUSER", "superuser"
        PEOPLE="PEOPLE", "people"
        PANDIT="PANDIT", "pandit"

    user_type=models.CharField(max_length=10,choices=Types.choices, default=Types.SUPERUSER)
    UID=models.AutoField(unique=True, primary_key=True)
    email=models.EmailField(max_length=150, unique=True)
    name=models.CharField(max_length=72)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    is_people=models.BooleanField(default=False)
    is_pandit=models.BooleanField(default=False)

    USERNAME_FIELD="email"

    objects=UserAccountManager()

    def __str__(self):
        return str(self.email)
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    def save(self, *args, **kwargs):
        if not self.user_type or self.user_type==None:
            self.user_type=UserAccount.Types.SUPERUSER
        return super().save(*args, **kwargs)
    
class PeopleManager(models.Manager):
    def create_user(self, email, password=None):
        if not email or len(email)<=0:
            raise ValueError("email is reuired")
        if not password:
            raise ValueError("password is required")
        
        email=email.lower()
        user=self.model(email=email)
        user.set_password(password)
        user.save(using=self.db)

        return user
    
    def get_queryset(self, *args, **kwargs):
        queryset=super().get_queryset(*args, **kwargs)
        queryset=queryset.filter(user_type=UserAccount.Types.PEOPLE)
        return queryset
    
class People(UserAccount):
    # name=models.CharField(max_length=72)
    objects=PeopleManager()
    def save(self, *args, **kwargs):
        self.user_type=UserAccount.Types.PEOPLE
        self.is_people=True
        return super().save(*args, **kwargs)

class PanditManager(models.Manager):
    def create_user(self, email, password=None):
        if not email or len(email)<=0:
            raise ValueError("Email Required")
        if not password:
            raise ValueError("Password Required")
        email=email.lower()
        user=self.model(email=email)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def get_queryset(self, *args, **kwargs):
        queryset=super().get_queryset(*args, **kwargs)
        queryset=queryset.filter(user_type=UserAccount.Types.PANDIT)
        return queryset

class Pandit(UserAccount):
    # phone=models.IntegerField(max_length=10)
    objects=PanditManager()

    def save(self, *args, **kwargs):
        self.user_type=UserAccount.Types.PANDIT
        self.is_pandit=True
        return super().save(*args, **kwargs)

class panditProfileData(models.Model):
    user=models.OneToOneField(Pandit, on_delete=models.CASCADE, primary_key=True, blank=False)
    pname=models.CharField(max_length=155, blank=True)
    gender=models.CharField(max_length=55, blank=True)
    high_edu=models.CharField(max_length=55, blank=True)
    supp_docs=models.FileField(upload_to='userImages/', max_length=2048, default="userImages/profile.png")
    photo=models.ImageField(upload_to='userImages/', max_length=2048, default="userImages/profile.png")
    phone=models.IntegerField(blank=True, default=0000000000)
    whatsapp=models.IntegerField(blank=True, default=0000000000)
    country=models.CharField(max_length=155, blank=True)
    state=models.CharField(max_length=155, blank=True)
    city=models.CharField(max_length=155, blank=True)
    pincode=models.IntegerField(blank=True, default=000000)
    faddress=models.TextField(max_length=500, blank=True)
    role=models.CharField(max_length=255, blank=False)
    experience=models.IntegerField(blank=True, default=0)
    lang=models.TextField(max_length=155, blank=True)
    skill=models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.name
    
class serviceData(models.Model):
    user=models.ForeignKey(Pandit, on_delete=models.PROTECT, blank=False)
    title=models.CharField(max_length=255, blank=False, unique=True)
    description=models.TextField(max_length=700, blank=False)
    fee=models.IntegerField(blank=False)
    service_img=models.ImageField(upload_to='serviceImages/', max_length=2048, blank=False)

    def __str__(self):
        return self.title


class Bookings(models.Model):
    id=models.AutoField(unique=True, primary_key=True)
    P_user=models.ForeignKey(Pandit, on_delete=models.PROTECT, blank=False)
    N_user=models.ForeignKey(People, on_delete=models.PROTECT, blank=False)
    ritual=models.ForeignKey(serviceData, on_delete=models.CASCADE, blank=False)
    ritual_name=models.TextField(max_length=255, blank=False)
    name=models.TextField(max_length=255, blank=False)
    email=models.EmailField(max_length=255, blank=False)
    phone=models.IntegerField(blank=False)
    ritual_date=models.DateField(blank=False)
    ritual_time=models.TimeField(blank=False)
    destination=models.TextField(max_length=255, blank=False)
    additional=models.TextField(max_length=500, blank=True, default=None)
    charge=models.IntegerField(blank=False)
    is_accepted=models.BooleanField(default=False)

    def __str___(self):
        return self.ritual


