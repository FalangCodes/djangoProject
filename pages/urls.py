from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login_signup, name='login_signup'),
    path('login/', views.handle_login, name='handle_login'),
    path('signup/', views.handle_signup, name='handle_signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log-expense/', views.log_expense, name='log_expense'),
    path('logout/', LogoutView.as_view(next_page='login_signup'), name='logout'),
]
