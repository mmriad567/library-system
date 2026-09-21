from django.urls import path
from . import views

urlpatterns = [
    path('books/',views.book_list,name='book_list'),
    path('book/search/',views.book_search,name='book_search'),
    path('book/<int:pk>/',views.book_detail,name='book_detail'),
    
]
