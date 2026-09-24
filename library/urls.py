from django.urls import path
from . import views

urlpatterns = [
    path('books/',views.book_list,name='book_list'),
    path('book/search/',views.book_search,name='book_search'),
    path('book/<int:pk>/',views.book_detail,name='book_detail'),
    path('borrows/',views.borrow_list,name='borrow_list'),
    path('borrow/book/<int:book_id>/',views.borrow_book,name='borrow_book'),
    path('return/<int:borrow_id>',views.return_book,name='return_book'),
    
]
