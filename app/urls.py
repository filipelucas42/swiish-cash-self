from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("login/", views.Login.as_view(), name="login"),
    path('confirm/', views.confirm, name='confirm'),
    path('send-transaction/', views.send_transaction, name='send-transaction'),
    path('send/', views.send, name='send'),
    path('history/', views.history, name='history'),
    path('logout/', views.logout_handler, name='logout'),
    path('self/', views.self, name='self'),
    path('confirm-transfer/', views.confirm_transfer, name='confirm-transfer'),
    path('create-login/', views.CreateLogin.as_view(), name='create-login'),
]