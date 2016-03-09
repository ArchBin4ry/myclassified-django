from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.contrib.sites.models import Site # For robot?
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView, TemplateView
from django.utils.decorators import method_decorator
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from .models import Section, Group, Post, Image

class IndexPageView(TemplateView):

    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context['sections'] = Section.objects.all()
        return context


def page403(request):
    return render(request, '403.html', {}, status=403)


def page404(request):
    return render(request, '404.html', {}, status=404)


def page500(request):
    return render(request, '500.html', {}, status=500)
