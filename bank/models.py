from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.core.validators import RegexValidator
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class UserManager(BaseUserManager):
    def create_user(self,name,email,username,password,cell_no,aadhar_id,PAN_no):
        if not email:
            raise ValueError('User must have an email')
        if not username:
            raise ValueError('user must have an username')

        user = self.model(
                name=name,
                email = self.normalize_email(email),
                username = username,
                password=password,
                cell_no=cell_no,
                PAN_no=PAN_no,
                aadhar_id=aadhar_id,
                )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,name,email,username,password,cell_no,aadhar_id,PAN_no,**kwargs):
        kwargs.setdefault('role','ADMIN')
        user = self.create_user(
                name=name,
                email = self.normalize_email(email),
                username = username,
                password=password, 
                cell_no=cell_no,
                PAN_no=PAN_no,
                aadhar_id=aadhar_id,
                )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    ROLE_CHOICE = (
                    ('Admin','ADMIN'),
                    ('Agent','AGENT'),
                    ('User','USER'),
            )
    CHOICE = (
                ('ACTIVE','Active'),
                ('InACTIVE','InActive'),
            )
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=30,unique=True)
    username = models.CharField(max_length=20)
    status = models.CharField(max_length=20,choices=CHOICE,default='ACTIVE')
    cell_regex = RegexValidator(regex=r'^\+?\d{9,12}$')
    cell_no = models.CharField(max_length=12,validators=[cell_regex])
    role = models.CharField(max_length=20,choices=ROLE_CHOICE,default='Admin')
    aadhar_regex = RegexValidator(regex=r'^\+?\d{12}$')
    aadhar_id = models.CharField(max_length=12, validators=[aadhar_regex],blank=True)
    PAN_regex = RegexValidator(regex=r'^[A-Z]{5}[0-9]{4}[A-Z]$')
    PAN_no = models.CharField(max_length=10,validators=[PAN_regex])
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','username','cell_no','aadhar_id','PAN_no']

    objects = UserManager()

    def __str__(self):
        return self.name

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True
    
    class Meta:
        verbose_name_plural = 'Users'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Requests(models.Model):
    CHOICE = (
        ('NEW','New'),
        ('APPROVED','Approved'),
        ('NOT_APPROVED','Not_Approved'),
            )
    user_name = models.ForeignKey(Users,on_delete=models.DO_NOTHING,related_name='user')
    agent_name = models.ForeignKey(Users,on_delete=models.DO_NOTHING,related_name='agent')
    loan_amt = models.IntegerField()
    interest_rate = models.IntegerField()
    EMI = models.IntegerField()
    total_months = models.IntegerField()
    status = models.CharField(max_length=30,choices = CHOICE,default='NEW')
    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        req = [self.agent_name,self.user_name]
        return ':'.join(req)

    class Meta:
        verbose_name_plural = 'Requests'

