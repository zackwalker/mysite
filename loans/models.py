from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    extra_payment = models.DecimalField(decimal_places=2, max_digits=10,default=0)
    payoff_style = models.CharField(max_length=25,null=True, blank=True,default='Dave Ramsey')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class LoanInformation(models.Model):
    loan_user       = models.ForeignKey(Profile, on_delete=models.CASCADE,default=1)
    principal       = models.DecimalField(decimal_places=2, max_digits=100)
    interest_rate   = models.DecimalField(decimal_places=2, max_digits=3)
    minimum_payment = models.DecimalField(decimal_places=2, max_digits=10)
    loan_name       = models.CharField(max_length=25)

    def __str__(self):
        return self.loan_name

    def get_absolute_url(self):
        return reverse("loans:loan-update", kwargs={"id":self.id})
