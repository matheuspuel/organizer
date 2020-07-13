from django.http import HttpResponseRedirect
from django.urls import path
from django.views import generic
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from . import forms


class Action:
    def __init__(self, function, name, verbose_name, class_action=False, hide=False, button_classes=None, icon_classes=None):
        self.function = function
        self.name = name
        self.verbose_name = verbose_name
        self.class_action = class_action
        self.hide = hide
        self.button_classes = button_classes
        self.icon_classes = icon_classes


class ContextTitleMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = self.model._meta.app_config.verbose_name
        context['model_name'] = self.model._meta.model_name
        context['model_verbose_name'] = self.model._meta.verbose_name
        context['action_name'] = self.action_name
        context['class_actions'] = [action for action in self.view_set.actions if action.class_action and not action.hide]
        context['instance_actions'] = [action for action in self.view_set.actions if not action.class_action and not action.hide]
        context['quick_form'] = forms.TaskQuickModelForm
        return context


class SetUserMixin(ContextTitleMixin):
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class DataPresentationMixin(ContextTitleMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = self.get_fields()
        return context

    def exclude_fields(self):
        field_list = list(self.model._meta.fields)
        for name in self.__class__.exclude:
            for field in field_list:
                if name == field.name:
                    field_list.remove(field)
                    break
        return field_list

    def include_fields(self):
        field_list = []

        def inner():
            for field in list(self.model._meta.fields):
                if name == field.name:
                    field_list.append(field)
                    return
            field_list.append(getattr(self.model, name))
        for name in self.__class__.fields:
            inner()
        return field_list

    def get_fields(self):
        if hasattr(self.__class__, 'fields'):
            return self.include_fields()
        elif hasattr(self.__class__, 'exclude'):
            return self.exclude_fields()
        else:
            return self.model._meta.fields


class TaskViewSet:
    model = models.Task
    has_user = True
    list_fields = ['priority', 'importance', 'title', 'category', 'place', 'duration', 'start', 'deadline', 'time_to_end_field', 'status', ]
    list_exclude = ['id', 'user', 'details', 'create_time', 'complete_time', 'deleted', ]
    detail_exclude = ['id', 'user', ]

    def model_mixin(self):
        class ModelMixin(LoginRequiredMixin):
            model = self.model
            has_user = self.has_user
            success_url = model.get_absolute_url()
            form_class = forms.TaskModelForm

            def get_queryset(self):
                if self.has_user:
                    return self.model.objects.filter(user=self.request.user)
                else:
                    return self.model.objects.all()

        return ModelMixin

    def __init__(self):
        self.model = self.__class__.model
        self.has_user = self.__class__.has_user
        self.list_fields = self.__class__.list_fields
        self.list_exclude = self.__class__.list_exclude
        self.detail_exclude = self.__class__.detail_exclude
        self.actions = []

        class ListView(self.model_mixin(), DataPresentationMixin, generic.ListView):
            fields = self.list_fields
            action_name = 'List'
            view_set = self
            form_class = forms.TaskQuickModelForm

            def get_queryset(self):
                return self.model.list_active(user=self.request.user)

        class DeletedListView(self.model_mixin(), DataPresentationMixin, generic.ListView):
            fields = self.list_fields
            action_name = 'Deleted List'
            view_set = self

            def get_queryset(self):
                return self.model.list_deleted(user=self.request.user)

        class CompletedListView(self.model_mixin(), DataPresentationMixin, generic.ListView):
            fields = self.list_fields
            action_name = 'Completed List'
            view_set = self

            def get_queryset(self):
                return self.model.list_completed(user=self.request.user)

        class DetailView(self.model_mixin(), DataPresentationMixin, generic.DetailView):
            exclude = self.detail_exclude
            action_name = 'Detail'
            view_set = self

        class CreateView(self.model_mixin(), SetUserMixin, generic.CreateView):
            action_name = 'Create'
            view_set = self

        class UpdateView(self.model_mixin(), SetUserMixin, generic.UpdateView):
            action_name = 'Update'
            view_set = self

        class QuickCreateView(self.model_mixin(), SetUserMixin, generic.CreateView):
            action_name = 'Quick Create'
            view_set = self
            form_class = forms.TaskQuickModelForm
            # template_name = 'task_quick_form.html'

        class CompleteView(self.model_mixin(), ModelFormMixin, generic.View):
            action_name = 'Complete'
            view_set = self

            def get(self, request, *args, **kwargs):
                self.object = self.get_object()
                self.object.toggle_complete()
                self.object.save()
                return HttpResponseRedirect(self.success_url)

        class DeleteView(self.model_mixin(), ModelFormMixin, generic.View):
            action_name = 'Delete'
            view_set = self

            def get(self, request, *args, **kwargs):
                self.object = self.get_object()
                self.object.toggle_delete()
                self.object.save()
                return HttpResponseRedirect(self.success_url)

        self.actions = [
            Action(CreateView.as_view, 'create', 'Create', class_action=True, button_classes='btn btn-success', icon_classes='fa fa-plus'),
            Action(ListView.as_view, 'list', 'List', class_action=True, button_classes='btn btn-info'),
            Action(CompletedListView.as_view, 'completed_list', 'Completed List', class_action=True, button_classes='btn btn-info'),
            Action(DeletedListView.as_view, 'deleted_list', 'Deleted List', class_action=True, button_classes='btn btn-info'),
            Action(DetailView.as_view, 'detail', 'Detail', button_classes='btn btn-info', icon_classes='fa fa-search'),
            Action(UpdateView.as_view, 'update', 'Update', button_classes='btn btn-warning', icon_classes='fa fa-pencil-alt'),
            Action(CompleteView.as_view, 'complete', 'Complete', button_classes='btn btn-success', icon_classes='fa fa-check'),
            Action(DeleteView.as_view, 'delete', 'Delete', button_classes='btn btn-danger', icon_classes='fa fa-trash'),
            Action(QuickCreateView.as_view, 'quick_create', 'Quick Create', class_action=True, hide=True),
        ]

    def url_patterns(self):
        name = self.model._meta.model_name
        urls = []
        for action in self.actions:
            urls.append(path(
                name + '/' + ('' if action.class_action else '<int:pk>/') + action.name + '/',
                action.function(),
                name=name + '_' + action.name
            ))
        return urls


