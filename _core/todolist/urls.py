"""_core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from todolist import views


urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('task_list')), name='todolist_index'),
    path('task/list/', views.TaskListView.as_view(), name='task_list'),
    path('task/completed_list/', views.TaskCompletedListView.as_view(), name='task_completed_list'),
    path('task/deleted_list/', views.TaskDeletedListView.as_view(), name='task_deleted_list'),
    path('task/<int:pk>/detail/', views.TaskDetailList.as_view(), name='task_detail'),
    path('task/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/complete/', views.TaskCompleteView.as_view(), name='task_complete'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('task/quick_create/', views.TaskQuickCreateView.as_view(), name='task_quick_create'),
]
