from django.contrib import admin
from .models import Author,Book,Member,Borrow

# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display=('name','nationality','birth_date')
    search_fields=('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=('title','isbn','publisher','total_copies','available_copies')
    list_fliter=('published_year',)
    search_fields=('title','isbn')
    filter_horizontal=('authors',)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display=('name','phone','joined_date','is_active')
    list_filter=('is_active',)
    search_fields=('name','phone')


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display=('book','member','borrow_date','due_date','is_returned','fine')
    list_filter=('is_returned','borrow_date')
    search_fields=('book__title','member__name')