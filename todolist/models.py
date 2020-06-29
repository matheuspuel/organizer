import datetime

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse_lazy


class CalculatedField:
    def __init__(self, name, verbose_name, pretty_type=None):
        self.name = name
        self.verbose_name = verbose_name
        self.pretty_type = pretty_type


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

    @classmethod
    def get_absolute_url(cls):
        return reverse_lazy(cls._meta.model_name + '_list')

    @property
    def is_deleted(self):
        return self.deleted

    @property
    def is_completed(self):
        if self.complete_time is None:
            return False
        else:
            return True

    @property
    def is_active(self):
        if not self.is_completed and not self.is_deleted:
            return True
        else:
            return False

    @property
    def has_started(self):
        if not self.start or self.start < datetime.datetime.now():
            return True
        else:
            return False

    @property
    def time_to_end(self):
        if self.deadline:
            delta = self.deadline - datetime.datetime.now()
            result = datetime.timedelta(days=delta.days, seconds=delta.seconds)
            return result
        else:
            return None
    time_to_end_field = CalculatedField(name='time_to_end', verbose_name='Time Left', pretty_type='dhm')

    @staticmethod
    def list_active(user):
        now = datetime.datetime.now()
        qs_no_date = __class__.objects.filter(user=user, deleted=False, complete_time=None, start=None)\
            .annotate(qs_order=models.Value(0, models.IntegerField()))

        qs_before = __class__.objects.filter(user=user, deleted=False, complete_time=None, start__lte=now)\
            .annotate(qs_order=models.Value(0, models.IntegerField()))

        qs_started = (qs_no_date | qs_before)

        qs_not_started = __class__.objects.filter(user=user, deleted=False, complete_time=None, start__gt=now)\
            .annotate(qs_order=models.Value(1, models.IntegerField()))

        return qs_started.union(qs_not_started).order_by('qs_order', '-priority', '-importance')

    @staticmethod
    def list_completed(user):
        return __class__.objects.filter(user=user, deleted=False).exclude(complete_time=None).order_by('-complete_time')

    @staticmethod
    def list_deleted(user):
        return __class__.objects.filter(user=user, deleted=True)

    def do_complete(self):
        self.complete_time = datetime.datetime.now()

    def undo_complete(self):
        self.complete_time = None

    def toggle_complete(self):
        if self.complete_time:
            self.undo_complete()
        else:
            self.do_complete()

    def do_delete(self):
        self.deleted = True

    def undo_delete(self):
        self.deleted = False

    def toggle_delete(self):
        if self.deleted:
            self.undo_delete()
        else:
            self.do_delete()


