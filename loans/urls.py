from django.urls import path
from . import views

app_name = 'loans'
urlpatterns = [
    path('', views.LoanListView.as_view(), name='loan-list'),
    path('create/', views.LoanCreateView.as_view(), name='add-loan'),
    path('chart/', views.pie_chart, name='pie-chart'),
    # path('templatetest/', views.LoanTemplateView.as_view(), name='template_home'),
    path('<int:id>/', views.LoanDetailView.as_view(), name='loan-details'),
    path('<int:id>/update/', views.LoanUpdateView.as_view(), name='loan-update'),

]
