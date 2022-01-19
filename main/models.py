from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta

# Create your models here.

def numeric_validator(value):
    if not value.isnumeric():
        raise ValidationError(_("The phone number is not a number"))
    if len(value) != 11:
        raise ValidationError(_("The phone number should be 11 digits"))
    phone_start_number = ['081','080','090','091','070']
    if value[:3]  in phone_start_number:
        pass
    else:
        raise ValidationError(_("Enter a valid nigerian number"))

class BaseManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class ActiveManager(models.Manager):
    def recent(self,location = None):
        if location:
            return self.filter(active=True,location=location).order_by("-date_uploaded")[:6]
        return self.filter(active=True).order_by("-date_uploaded")[:6]
    # def unexpired(self):
    #     return


class User(AbstractUser):
    username = None
    email = models.EmailField(
        _('Email'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    phone_number = models.CharField(
        _('Phone Number'),
        max_length=11,
        validators = [numeric_validator],
        help_text=_('Required. 11 Nigeria Phone Numbers.'),
        error_messages={
            'max_length': _("11 Numbers required."),
        },
    )
    objects = BaseManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class ProductTag(models.Model):
    name = models.CharField(max_length= 30)
    description = models.TextField(max_length = 300,blank = True)
    def __str__(self):
        return self.name


class Product(models.Model):
    CHOICES = (("UNN","UNN"),("UNEC","UNEC"))
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    tag = models.ManyToManyField(ProductTag, blank = True)
    description = models.TextField(max_length= 3000)
    price = models.IntegerField()
    phone_number = models.CharField(_('Phone Number'),
        max_length=11,
        blank= True,
        validators = [numeric_validator],
        help_text=_('11 Nigeria Phone Numbers.'),
        error_messages={
            'max_length': _("11 Numbers required."),
        },
    )
    negotiable = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    available = models.BooleanField(default=True)
    location = models.CharField(max_length = 5,choices = CHOICES)
    date_uploaded = models.DateTimeField(auto_now_add = True)
    expiring_date = models.DateTimeField(default=datetime.now() + timedelta(weeks= 1))

    objects = ActiveManager()
    def first_image(self):
        try:
            image = self.productimage_set.all()[0]
        except:
            image = None
        return image
    def adjusted_phone_number(self):
        return "+234"+str(self.phone_number[1:])
    def __str__(self):
        return self.name
class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField()
    def _str_(self):
        return self.product.name

class SavedProduct(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

