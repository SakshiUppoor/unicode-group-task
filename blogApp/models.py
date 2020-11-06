from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
# Create your models here.


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    dob = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='image', blank=True)
    date_joined = models.DateField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def save(self, *args, **kwargs):
        self.username = self.email
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

class Blogs(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_on=models.DateField()
    last_updated=models.DateField()
    picture=models.ImageField(upload_to='image')
    caption=models.CharField(max_length=500,blank=True)

    

class Comment(models.Model):
    blog = models.ForeignKey(Blogs,on_delete=models.CASCADE)
    comment_by = models.ForeignKey(User,on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.blog)+'_'+str(self.comment_by)
    
    class Meta:
        ordering = ['-last_updated']
    
    @property
    def replies(self):
        return self.reply_set.all()

class Reply(models.Model):
    reply_by = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
    reply_text = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.comment)+'_'+str(self.reply_by)
    
    class Meta:
        ordering = ['-last_updated']
        verbose_name_plural = 'Replies'
    