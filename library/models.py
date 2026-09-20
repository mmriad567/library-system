from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    name=models.CharField(max_length=100)
    bio=models.TextField(blank=True,null=True)
    birth_date=models.DateField(blank=True,null=True)
    nationality=models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title=models.CharField(max_length=200)
    isbn=models.CharField(max_length=20,unique=True)
    publisher=models.CharField(max_length=100,blank=True,null=True)
    published_year=models.IntegerField(blank=True,null=True)
    description=models.TextField(blank=True,null=True)
    cover_image=models.ImageField(upload_to='book_cover/',blank=True,null=True)
    authors=models.ManyToManyField(Author,related_name='books')

    total_copies=models.PositiveIntegerField(default=1)
    available_copies=models.PositiveIntegerField(default=1)
    added_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

    @property
    def is_available(self):
        return self.available_copies > 0


class Member(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='member')
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=20,blank=True,null=True)
    address=models.TextField(blank=True,null=True)
    joined_date=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Borrow(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name='borrows')
    member=models.ForeignKey(Member,on_delete=models.CASCADE,related_name='borrows')
    borrow_date=models.DateField(auto_now_add=True)
    due_date=models.DateField()
    return_date=models.DateField(blank=True,null=True)
    is_returned=models.BooleanField(default=False)
    fine=models.DecimalField(max_digits=10,decimal_places=2,default=0)

    class Meta:
        ordering=['-borrow_date']

    def __str__(self):
        return f"{self.member.name} - {self.book.title}"


    @property
    def is_overdue(self):
        from django.utils import timezone
        if self.is_returned:
            return False
        return timezone.now().date() > self.due_date