from django.http import HttpResponseRedirect
from django.urls import path
from django.views import generic
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from . import forms


class TaskListView(generic.ListView, LoginRequiredMixin):
    model = models.Task

    def get_queryset(self):
        return self.model.list_active(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['quick_form'] = forms.TaskQuickModelForm
        return context


class TaskQuickCreateView(generic.CreateView):
    model = models.Task
    fields = ('title',)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class TaskCreateView(generic.CreateView, LoginRequiredMixin):
    model = models.Task
    fields = (
        'title', 'details', 'category', 'place', 'start', 'deadline', 'duration', 'importance', 'priority', 'status',)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class TaskUpdateView(generic.UpdateView, LoginRequiredMixin):
    model = models.Task
    fields = (
        'title', 'details', 'category', 'place', 'start', 'deadline', 'duration', 'importance', 'priority', 'status',)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

