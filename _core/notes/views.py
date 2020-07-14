from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.urls import path
from django.views import generic
from django.views.generic.edit import ModelFormMixin

from . import models, forms


class NoteListView(LoginRequiredMixin, generic.ListView):
    model = models.Note
    template_name = 'notes/note_list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, deleted=False)\
            .order_by('-importance', '-create_time')


class NoteDeletedListView(NoteListView):

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, deleted=True)


class NoteDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Note
    template_name = 'notes/note_detail.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class NoteCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Note
    template_name = 'notes/note_form.html'
    form_class = forms.NoteForm
    success_url = model.get_absolute_url()

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Note
    template_name = 'notes/note_form.html'
    form_class = forms.NoteForm
    success_url = model.get_absolute_url()

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class NoteDeleteView(LoginRequiredMixin, ModelFormMixin, generic.View):
    model = models.Note
    success_url = model.get_absolute_url()

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.toggle_delete()
        obj.save()
        return HttpResponseRedirect(self.success_url)



