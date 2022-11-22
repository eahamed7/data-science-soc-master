from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import FreshersMail
from .forms import FreshersForm
from django.contrib import messages



# Create your views here.

def freshers(request):
    if request.method == 'POST':
        form = FreshersForm(request.POST)
        if form.is_valid():
            new_mail_client = FreshersMail.objects.create(
                email = form.data['email']
            )
            new_mail_client.save()
            messages.success(request, 'Your email has been successfully registered, check your inbox soon :)')
            return HttpResponseRedirect('/freshers')
    else:
        form = FreshersForm()

    return render(request, 'home/freshers.html', {'form': form})


def index(request):
    return render(request, 'home/home.html')

