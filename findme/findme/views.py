
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseNotFound
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from django.template import Context
from django.template.loader import get_template, TemplateDoesNotExist

import djqscsv

from findme.forms import ContactForm


def handler404(request, template_name='404.html'):
    t = get_template(template_name)
    ctx = Context({})
    return HttpResponseNotFound(t.render(ctx))


class ContactFormView(FormView):

    form_class = ContactForm
    template_name = 'email_form.html'
    success_url = '/email_sent.html'

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


class StaticView(TemplateView):

    def get(self, request, page, *args, **kwargs):
        self.template_name = page
        response = super(StaticView, self).get(request, *args, **kwargs)
        try:
            return response.render()
        except TemplateDoesNotExist:
            raise HttpResponseNotFound


# class UtilitiesView(LoginRequiredMixin, TemplateView):

    # def get_csv(request):
        # qs = Person.objects.all()
        # filename = djqscsv.generate_filename(person_qs, append_datestamp=True)
        # render_to_csv_response(person_qs, use_verbose_names=False)
        ## for foreign keys
        # person_qs = Person.objects.values('id', 'name', 'hobby__name')
        # csv_file = TemporaryFile()
        # djqscsv.write_csv(person_qs, csv_file)
        # return djqscsv.render_to_csv_response(qs)