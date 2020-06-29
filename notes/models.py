import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy


class Note(models.Model):
    title = models.CharField(max_length=120, verbose_name='Title')
    text = models.TextField(blank=True, null=True, verbose_name='Text')
    category = models.CharField(max_length=60, null=True, blank=True, verbose_name='Category')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes', verbose_name='User')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Create Time')
    importance = models.IntegerField(null=True, blank=True, verbose_name='Importance')
    deleted = models.BooleanField(default=False, verbose_name='Deleted')

    class Meta:
        verbose_name = "Note"

    @classmethod
    def get_absolute_url(cls):
        return reverse_lazy(cls._meta.model_name + '_list')

    @property
    def is_deleted(self):
        return self.deleted

    @property
    def is_active(self):
        return not self.is_deleted

    @staticmethod
    def list_active(owner):
        return __class__.objects.filter(owner=owner, deleted=False).order_by('-importance', '-create_time')

    @staticmethod
    def list_deleted(owner):
        return __class__.objects.filter(owner=owner, deleted=True)

    def do_delete(self):
        self.deleted = True

    def undo_delete(self):
        self.deleted = False

    def toggle_delete(self):
        if self.deleted:
            self.undo_delete()
        else:
            self.do_delete()

