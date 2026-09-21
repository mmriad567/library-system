from django.shortcuts import render,get_object_or_404
from .models import Book

# Create your views here.

def book_list(request):
    books=Book.objects.all().order_by('-added_at')
    return render(request,'library/book_list.html',{'books':books})


def book_detail(request,pk):
    book=get_object_or_404(Book,pk=pk)
    return render(request,'library/book_detail.html',{'book':book})


def book_search(request):
    query=request.GET.get('q','')
    if query:
        books=Book.objects.filter(title__icontains=query).order_by('-added_at')
    else:
        books=Book.objects.all().order_by('-added_at')

    return render(request,'library/_book_cards.html',{'books':books})

