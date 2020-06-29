from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.urls import path
from django.views import generic
from django.views.generic.edit import ModelFormMixin

from . import models


def model_form_factory(meta_model):
    class GenericModelForm(ModelForm):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['title'].widget.attrs.update(size='45', autofocus=True)

        class Meta:
            model = meta_model
            exclude = ['user', 'create_time', 'deleted']
    return GenericModelForm


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
        context['class_actions'] = [action for action in self.actions if action.class_action]
        context['instance_actions'] = [action for action in self.actions if not action.class_action]
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
        context['fields'] = self.exclude_fields()
        return context

    def exclude_fields(self):
        field_list = list(self.model._meta.fields)
        for name in self.__class__.exclude:
            for field in field_list:
                if name == field.name:
                    field_list.remove(field)
                    break
        return field_list


class BaseViewSet:
    model = None
    has_user = False
    list_exclude = []
    detail_exclude = []
    actions = []

    def __init__(self):
        self.model = self.__class__.model

    def model_mixin(self):
        class ModelMixin(LoginRequiredMixin):
            model = self.model
            has_user = self.has_user
            success_url = model.get_absolute_url()
            form_class = model_form_factory(model)

            def get_queryset(self):
                if self.has_user:
                    return self.model.objects.filter(user=self.request.user)
                else:
                    return self.model.objects.all()
        return ModelMixin

    # VIEWS
    def list_view(self):
        class SpecificView(self.model_mixin(), DataPresentationMixin, generic.ListView):
            exclude = self.list_exclude
            action_name = 'List'
            actions = self.__class__.actions
        return SpecificView.as_view()

    def detail_view(self):
        class SpecificView(self.model_mixin(), DataPresentationMixin, generic.DetailView):
            exclude = self.detail_exclude
            action_name = 'Detail'
            actions = self.__class__.actions
        return SpecificView.as_view()

    def create_view(self):
        class SpecificView(self.model_mixin(), SetUserMixin, generic.CreateView):
            action_name = 'Create'
            actions = self.__class__.actions
        return SpecificView.as_view()

    def update_view(self):
        class SpecificView(self.model_mixin(), SetUserMixin, generic.UpdateView):
            action_name = 'Update'
            actions = self.__class__.actions
        return SpecificView.as_view()

    def delete_view(self):
        class SpecificView(self.model_mixin(), DataPresentationMixin, generic.DeleteView):
            exclude = self.detail_exclude
            action_name = 'Delete'
            actions = self.__class__.actions
        return SpecificView.as_view()

    def url_patterns(self):
        name = self.model._meta.model_name
        urls = []
        for action in self.actions:
            urls.append(path(
                name + '/' + ('' if action.class_action else '<int:pk>/') + action.name + '/',
                action.function(self),
                name=name + '_' + action.name
            ))
        return urls


class NoteViewSet(BaseViewSet):
    model = models.Note
    has_user = True
    list_exclude = ['id', 'user', 'text', 'create_time', 'deleted']
    detail_exclude = ['id', 'user']

    def delete_view(self):
        class SpecificView(self.model_mixin(), ModelFormMixin, generic.View):
            action_name = 'Delete'
            actions = self.__class__.actions

            def get(self, request, *args, **kwargs):
                self.object = self.get_object()
                self.object.toggle_delete()
                self.object.save()
                return HttpResponseRedirect(self.success_url)
        return SpecificView.as_view()

    def list_view(self):
        class SpecificView(self.model_mixin(), DataPresentationMixin, generic.ListView):
            exclude = self.list_exclude
            action_name = 'List'
            actions = self.__class__.actions

            def get_queryset(self):
                return self.model.objects.filter(user=self.request.user, deleted=False)\
                    .order_by('-importance', '-create_time')

        return SpecificView.as_view()

    def deleted_list_view(self):
        class SpecificView(self.model_mixin(), DataPresentationMixin, generic.ListView):
            exclude = self.list_exclude
            action_name = 'Deleted List'
            actions = self.__class__.actions

            def get_queryset(self):
                return self.model.objects.filter(user=self.request.user, deleted=True)

        return SpecificView.as_view()

    actions = [
        Action(BaseViewSet.create_view, 'create', 'Create', class_action=True, button_classes='btn btn-success', icon_classes='fa fa-plus'),
        Action(list_view, 'list', 'List', class_action=True, button_classes='btn btn-info'),
        Action(deleted_list_view, 'deleted_list', 'Deleted List', class_action=True, button_classes='btn btn-info'),
        Action(BaseViewSet.detail_view, 'detail', 'Detail', button_classes='btn btn-info', icon_classes='fa fa-search'),
        Action(BaseViewSet.update_view, 'update', 'Update', button_classes='btn btn-warning', icon_classes='fa fa-pencil-alt'),
        Action(delete_view, 'delete', 'Delete', button_classes='btn btn-danger', icon_classes='fa fa-trash'),
    ]

