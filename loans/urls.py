from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'loans'
urlpatterns = [
    path('', views.landing_page, name='loan-landing'),
    path('portal/', views.LoanListView.as_view(), name='loan-list'),
    path('create/', views.LoanCreateView.as_view(), name='add-loan'),
    path('register/', views.registerPage, name='register'),
    path('chart/', views.pie_chart, name='loan-visual'),
    path('<int:id>/delete', views.LoanDeleteView.as_view(), name='loan-delete'),
    path('<int:id>/update/', views.LoanUpdateView.as_view(), name='loan-update'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='loans/password_reset.html'),name='password_reset'),
    path('accounts/password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='loans/password_reset_sent.html'),name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='loans/password_reset_form.html'),name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='loans/password_reset_complete.html'),name='password_reset_complete'),
]
