import json

import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.edit import FormMixin

from courses.views import SuperUserPassesTestMixin

from .models import Teacher
from .forms import TeacherForm, TokenForm


class TeacherListView(ListView):
    model = Teacher


class TeacherDetailView(DetailView):
    model = Teacher


class TeacherAddView(SuperUserPassesTestMixin, CreateView):
    model = Teacher
    form_class = TeacherForm
    extra_context = {'page_title': 'добавление нового преподавателя'}
    success_url = reverse_lazy('users:teacher_list')


class TeacherEditView(SuperUserPassesTestMixin, UpdateView):
    model = Teacher
    fields = (
        'first_name', 'last_name', 'phone_number', 'avatar', 'bio')
    extra_context = {
        'page_title': 'редактирование личных данных преподавателя'}
    success_url = reverse_lazy('users:teacher_list')


class TeacherDeleteView(SuperUserPassesTestMixin, DeleteView):
    model = Teacher
    success_url = reverse_lazy('users:teacher_list')


class UserProfileView(LoginRequiredMixin, DetailView):
    queryset = get_user_model().objects.all()
    form_class = TokenForm

    def get_context_data(self, **kwargs):
        access_token = self.request.session.get('access_token', '')
        refresh_token = self.request.session.get('refresh_token', '')
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(
            initial={'refresh_token': refresh_token})
        context['access_token'] = access_token
        context['refresh_token'] = refresh_token
        return context

    def post(self, *args, **kwargs):
        pk = self.kwargs.get('pk', '')
        form = self.form_class(self.request.POST)
        if not form.is_valid():
            return redirect(reverse('users:user_profile', kwargs={'pk': pk}))
        form_data = form.cleaned_data
        refresh_token = form_data['refresh_token']
        if refresh_token:
            tokens_dict = self.get_data_from_api(
                self.request.build_absolute_uri(
                    reverse_lazy('api:token_refresh')),
                {'refresh': refresh_token}
            )
            access_token = tokens_dict.get('access', '')
            if not access_token:
                refresh_token = ''
        else:
            tokens_dict = self.get_data_from_api(
                self.request.build_absolute_uri(
                    reverse_lazy('api:token_obtain_pair')), {
                        'email': self.request.user.email,
                        'password': form_data['password']})
            access_token = tokens_dict.get('access', '')
            refresh_token = tokens_dict.get('refresh', '')
        self.request.session.update({
            'access_token': access_token,
            'refresh_token': refresh_token})
        return redirect(reverse('users:user_profile', kwargs={'pk': pk}))

    @staticmethod
    def get_data_from_api(url, post_data):
        response = requests.post(url, data=post_data)
        if response.status_code == 401:
            return {}
        tokens_dict = json.loads(response.content.decode())
        return tokens_dict
