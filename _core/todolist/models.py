import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Case, When
from django.urls import reverse_lazy


class TaskManager(models.Manager):
    def get_queryset(self):
        now = datetime.datetime.now()
        qs = super().get_queryset().annotate(
            has_started=Case(
                When(start__isnull=True, then=True),
                When(start__lt=now, then=True),
                default=False,
                output_field=models.BooleanField()
            )
        )
        return qs


class Task(models.Model):
    title = models.CharField(max_length=120, verbose_name='Title')
    details = models.TextField(blank=True, null=True, verbose_name='Details')
    category = models.CharField(max_length=60, null=True, blank=True, verbose_name='Category')
    place = models.CharField(max_length=60, null=True, blank=True, verbose_name='Place')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', verbose_name='User')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Create Time')
    start = models.DateTimeField(null=True, blank=True, verbose_name='Start')
    deadline = models.DateTimeField(null=True, blank=True, verbose_name='Deadline')
    complete_time = models.DateTimeField(null=True, blank=True, default=None, verbose_name='Complete Time')
    duration = models.DurationField(null=True, blank=True, verbose_name='Duration')
    importance = models.IntegerField(null=True, blank=True, verbose_name='Importance')
    priority = models.IntegerField(null=True, blank=True, verbose_name='Priority')
    status = models.CharField(max_length=60, null=True, blank=True, verbose_name='Status')
    deleted = models.BooleanField(default=False, verbose_name='Deleted')

    class Meta:
        verbose_name = "Task"

    objects = TaskManager()

    @classmethod
    def get_absolute_url(cls):
        return reverse_lazy(cls._meta.model_name + '_list')

    @property
    def time_to_end(self):
        if self.deadline:
            delta = self.deadline - datetime.datetime.now()
            result = datetime.timedelta(days=delta.days, seconds=delta.seconds)
            return result
        else:
            return None

    def toggle_complete(self):
        if self.complete_time:
            self.complete_time = None
        else:
            self.complete_time = datetime.datetime.now()

    def toggle_delete(self):
        if self.deleted:
            self.deleted = False
        else:
            self.deleted = True


