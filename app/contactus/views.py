from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

from django.conf import settings

from .models import Message


class ContactUsView(CreateView):
    model = Message
    fields = \
        'first_name', 'last_name', 'email', 'phone_number', 'title', 'text'
    success_url = reverse_lazy('contactus:send_message')

    def form_valid(self, form):
        message = form.save(commit=False)
        try:
            message.send_emails()
            messages.success(self.request, 'успешно.')
        except Exception as e:
            if settings.DEBUG:
                messages.error(self.request, f'ошибка: "{e}"')
            else:
                messages.error(self.request, f'ошибка, попробуйте позже!')
        return super().form_valid(form)
