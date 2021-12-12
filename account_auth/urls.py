from django.urls import path
from account_auth import views

urlpatterns = [
    path('signup/', views.Signup.as_view()),
    path('gettoken/', views.GetToken.as_view()),
]
