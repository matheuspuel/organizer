from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from . import forms


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = models.Task

    def get_queryset(self):
        qs = self.model.objects.filter(
            user=self.request.user, deleted=False, complete_time=None
        )
        return qs.order_by('-has_started', '-priority', '-importance')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['quick_form'] = forms.TaskQuickModelForm
        return context


class TaskCompletedListView(TaskListView):
    def get_queryset(self):
        qs = self.model.objects.filter(user=self.request.user, deleted=False).exclude(complete_time=None)
        return qs.order_by('-complete_time')


class TaskDeletedListView(TaskListView):
    def get_queryset(self):
        qs = self.model.objects.filter(user=self.request.user, deleted=True)
        return qs


class TaskDetailList(LoginRequiredMixin, generic.DetailView):
    model = models.Task
    template_name = 'todolist/task_detail.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TaskQuickCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Task
    form_class = forms.TaskQuickModelForm

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Task
    form_class = forms.TaskModelForm

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Task
    form_class = forms.TaskModelForm

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class TaskCompleteView(LoginRequiredMixin, generic.View, generic.edit.ModelFormMixin):
    model = models.Task
    success_url = model.get_absolute_url()

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.toggle_complete()
        obj.save()
        return HttpResponseRedirect(self.success_url)


class TaskDeleteView(LoginRequiredMixin, generic.View, generic.edit.ModelFormMixin):
    model = models.Task
    success_url = model.get_absolute_url()

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.toggle_delete()
        obj.save()
        return HttpResponseRedirect(self.success_url)
