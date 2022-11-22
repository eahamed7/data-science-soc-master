from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from django.contrib.messages.views import SuccessMessageMixin

from dal import autocomplete
from .models import Course



class SignUp(SuccessMessageMixin, generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    success_message = "Signed up correctly. Log in here to get started :)"
    template_name = 'signup.html'


class CourseAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Course.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
