from django.shortcuts import render,get_object_or_404
from .models import LoanInformation, Profile
from .forms import AddLoans
from django.views.generic import CreateView, DetailView, UpdateView, ListView, TemplateView
from django.urls import reverse
import queryset_converter
from itertools import permutations
from  .student_loan_payoff2 import master_func
from django.http import HttpResponse
from chartjs.views.lines import BaseLineChartView
import json

class LoanListView(ListView):
    def get_queryset(self):
        return LoanInformation.objects.filter(loan_user__user=self.request.user)
        # if self.request.user.has_perm('djangocbv.admin_access') or self.request.user.has_perm('djangocbv.publisher_access'):
        #     return qs
        # return qs.filter(owned_by=self.request.user)
    # queryset = LoanInformation.objects.all().select_related('loan_user_id')

def pie_chart(request):
    select_labels = []
    select_labels_none = []
    select_data = []
    select_data_none = []
    first_row = []
    loan_list = []
    attribute_list = []

    interest = ['Interest']
    period = []
    oop = []
    for li in LoanInformation.objects.filter(loan_user__user=request.user):
        row = [float(li.principal), round(float(li.interest_rate/12/100),4), float(li.minimum_payment), li.loan_name]
        loan_list.append(row)

    for li in Profile.objects.filter(user=request.user):
        row = [li.payoff_style, float(li.extra_payment)]
        attribute_list.append(row)
    data = master_func(loan_list,attribute_list[0][1],attribute_list[0][0])
    # select_labels_none,select_data_none = master_func(loan_list,attribute_list[0][1],attribute_list[0][0])
    interest = []
    period = []
    oop = []
    i=0
    for object in data[0]:
        interest.append(data[0][i])
        i+=1
    period = data[1]
    oop = data[2]
    return render(request, 'loans/pie_chart.html', {
        'interest': interest,
        'period': period,
        'oop': oop,
    })

# def LoanTemplateFuncView(request):
#     loan_objects = LoanInformation.objects.filter(loan_user__user=request.user)
#     context = {
#         'loan_objects': loan_objects
#     }
#     return render(request,'loans/loan.html',context)
#
# class LoanTemplateView(TemplateView):
#     template_name = 'loans/loan.html'
#
#
#     def get_context_data(self,*args, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['loan_objects'] = LoanInformation.objects.filter(loan_user__user=self.request.user)
#         context['payoff'] = Profile.objects.filter(user=self.request.user)
#         loan_list = []
#         for li in LoanInformation.objects.filter(loan_user__user=self.request.user):
#             row = [float(li.principal), round(float(li.interest_rate/12/100),4), float(li.minimum_payment), li.loan_name]
#             loan_list.append(row)
#         temp_dict = dict(enumerate(sorted(permutations(sorted(loan_list)))))
#         context['dataframe'] = master_func(loan_list,1000)
#         return context


class LoanCreateView(CreateView):
    template_name = 'loans/LoanInformation_create.html'
    form_class = AddLoans
    queryset = LoanInformation.objects.all()

class LoanUpdateView(UpdateView):
    template_name = 'loans/LoanInformation_update.html'
    form_class = AddLoans
    queryset = LoanInformation.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(LoanInformation, id=id_)

# class LoanDetailView(DetailView):
#     template_name = 'loans/LoanInformation_detail.html'
#     queryset = LoanInformation.objects.all()
#
#     def get_object(self):
#         id_ = self.kwargs.get("id")
#         return get_object_or_404(LoanInformation, id=id_)
