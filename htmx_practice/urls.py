from django.urls import path 
from . import views

urlpatterns = [
    path('',views.index,name='htmx_practice'),
    path('hello/',views.hello,name='htmx_hello'),
    path('char-count/',views.char_count,name='char_count'),
    path('like/',views.like_button,name='like_button'),
    path('toggle/',views.toggle,name='toggle'),
    path('delete/',views.delete_item,name='delete_item'),
    path('search/', views.search, name='search'),
]
