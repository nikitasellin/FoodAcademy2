from django.views.generic import TemplateView


class FrontendTestView(TemplateView):
    template_name = 'frontend_test.html'
