
from django.urls import path
from . import views

urlpatterns = [
    # The home page (http://127.0.0.1:8000/)
    path('', views.home_view, name='home_view'),
    
    # The encryption page (http://127.0.0.1:8000/encrypt/)
    path('encrypt/', views.encrypt_view, name='encrypt_view'),
    
    # The decryption page (http://127.0.0.1:8000/decrypt/)
    path('decrypt/', views.decrypt_view, name='decrypt_view'),
]