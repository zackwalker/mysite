from django.shortcuts import render,get_object_or_404
from .models import LoanInformation, Profile
from .forms import AddLoans, ProfileForm, UserForm
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView, View
from itertools import permutations
from  .loan_payoff_logic import master_func
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
import csv


def landing_page(request):
    return render(request,'loans/landing_page.html')

class CSVFileView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type = 'text/csv')
        cd = 'attachment;filename="{0}"'.format('test.csv')
        response['Content-Disposition'] = cd

        fieldnames = ('principal','loan_name')
        data = LoanInformation.objects.values(*fieldnames)

        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

        return response


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

def registerPage(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'loans/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
    # return render(request, 'loans/register.html', context)

class ProfileCreateView(CreateView):
    template_name = 'loans/Profile_create.html'
    form_class = Profile
    success_url = reverse_lazy('loans:loan-list')

class LoanUpdateView(UpdateView):
    template_name = 'loans/LoanInformation_update.html'
    form_class = AddLoans

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(LoanInformation, id=id_)

class LoanDeleteView(DeleteView):
    model = LoanInformation
    template_name = 'loans/LoanInformation_delete.html'
    success_url = reverse_lazy('loans:loan-list')
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(LoanInformation, id=id_)

class LoanCreateView(CreateView):
    template_name = 'loans/LoanInformation_create.html'
    form_class = AddLoans
    success_url = reverse_lazy('loans:loan-list')
