from django.shortcuts import render,get_object_or_404,redirect
from .models import Book,Member,Borrow
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta

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




@login_required
def borrow_book(request,book_id):

    if not request.user.is_staff:
        messages.error(request,'শুধু লাইব্রেরিয়ান বই ইস্যু করতে পারবেন।')
        return redirect('book_list')

    book=get_object_or_404(Book,pk=book_id)

    if request.method == 'POST':
        member_id=request.POST.get('member')
        member=get_object_or_404(Member,pk=member_id)

        if not book.is_available:
            messages.error(request,'এই বইয়ের কোনো কপি খালি নেই।')
            return redirect('book_detail',pk=book.id)


        if not member.is_active:
            messages.error(request,'এই সদস্য সক্রিয় নয়।')
            return redirect('book_detail',pk=book.id)

        due_date=timezone.now().date() + timedelta(days=14)
        Borrow.objects.create(
            book=book,
            member=member,
            due_date=due_date,
        )

        book.available_copies -=1
        book.save()

        messages.success(request,f'"{book.title}" {member.name}-কে দেওয়া হলো। ফেরত: {due_date}')
        return redirect('borrow_list')

    members=Member.objects.filter(is_active=True)
    return render(request,'library/borrow_book.html',{'book':book, 'members':members})



@login_required
def return_book(request,borrow_id):

    if not request.user.is_staff:
        messages.error(request,'শুধু লাইব্রেরিয়ান বই ফেরত নিতে পারবেন।')
        return redirect('book_list')

    borrow=get_object_or_404(Borrow,pk=borrow_id)

    if borrow.is_returned:
        messages.warning(request,'এই বই আগেই ফেরত দেওয়া হয়েছে।')
        return redirect('borrow_list')

    if request.method == 'POST':
        borrow.return_date=timezone.now().date()
        borrow.is_returned=True

        if borrow.return_date > borrow.due_date:
            days_late=(borrow.return_date - borrow.due_date).days
            borrow.fine=days_late * 5

        borrow.save()

        book=borrow.book
        book.available_copies +=1
        book.save()

        if borrow.fine > 0:
            messages.success(request,f'বই ফেরত নেওয়া হলো। জরিমানা: {borrow.fine} টাকা')
        else:
            messages.success(request,'বই ফেরত নেওয়া হলো। কোনো জরিমানা নেই।')
        return redirect('borrow_list')

    return render(request,'library/return_book.html',{'borrow':borrow})



@login_required
def borrow_list(request):
    if not request.user.is_staff:
        messages.error(request,'শুধু লাইব্রেরিয়ান এই তালিকা দেখতে পারবেন।')
        return redirect('book_list')

    active_borrows=Borrow.objects.filter(is_returned=False).order_by('due_date')
    return render(request,'library/borrow_list.html',{'borrows':active_borrows})
