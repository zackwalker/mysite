from django.shortcuts import render,get_object_or_404
from .models import LoanInformation, Profile
from .forms import AddLoans
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from itertools import permutations
from  .loan_payoff_logic import master_func
from django.http import HttpResponse


class LoanListView(ListView):
    def get_queryset(self):
        return LoanInformation.objects.filter(loan_user__user=self.request.user)

def pie_chart(request):
    first_row = []
    loan_list = []
    attribute_list = []

    for li in LoanInformation.objects.filter(loan_user__user=request.user):
        row = [float(li.principal), round(float(li.interest_rate/12/100),4), float(li.minimum_payment), li.loan_name]
        loan_list.append(row)

    for li in Profile.objects.filter(user=request.user):
        row = [li.payoff_style, float(li.extra_payment)]
        attribute_list.append(row)

    data = master_func(loan_list,attribute_list[0][1],attribute_list[0][0])
    interest = []
    period = []
    oop = []

    interest = data[0][0:7]
    period = data[1][0:7]
    oop = data[2][0:7]
    return render(request, 'loans/pie_chart.html', {
        'interest': interest,
        'period': period,
        'oop': oop,
    })

class LoanCreateView(CreateView):
    template_name = 'loans/LoanInformation_create.html'
    form_class = AddLoans
    success_url = '/'
    
class LoanUpdateView(UpdateView):
    template_name = 'loans/LoanInformation_update.html'
    form_class = AddLoans

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(LoanInformation, id=id_)

class LoanDeleteView(DeleteView):
    model = LoanInformation
    template_name = 'loans/LoanInformation_delete.html'
    success_url = '/'
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(LoanInformation, id=id_)
