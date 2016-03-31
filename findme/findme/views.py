from findme.forms import ContactForm
from django.views.generic.base import TemplateView
from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import FormView
from django.shortcuts import render, redirect, render_to_response, get_object_or_404

class ContactFormView(FormView):

    form_class = ContactForm
    template_name = "email_form.html"
    success_url = '/contact/'
    
    def get(self, request):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return render(self.request, self.template_name, {'form':form})
    
    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form':form}) 

    def form_valid(self, form):
        message = "{name} / {email} said: ".format(
            name=form.cleaned_data.get('name'),
            email=form.cleaned_data.get('email'))
        message += "\n\n{0}".format(form.cleaned_data.get('message'))
        send_mail(
            subject=form.cleaned_data.get('subject').strip(),
            message=message,
            from_email='contact-form@f.com',
            recipient_list=[settings.LIST_OF_EMAIL_RECIPIENTS],
        )
        return super(ContactFormView, self).form_valid(form)

class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context

