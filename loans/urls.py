from django.urls import path
from . import views

app_name = 'loans'
urlpatterns = [
    path('', views.landing_page, name='loan-landing'),
    path('portal/', views.LoanListView.as_view(), name='loan-list'),
    path('create/', views.LoanCreateView.as_view(), name='add-loan'),
    # path('profile/', views.ProfileCreateView.as_view(), name='profile'),
    path('chart/', views.pie_chart, name='loan-visual'),
    path('<int:id>/delete', views.LoanDeleteView.as_view(), name='loan-delete'),
    path('<int:id>/update/', views.LoanUpdateView.as_view(), name='loan-update'),

]
