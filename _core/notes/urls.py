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
from notes import views

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('note')), name='notes_index'),
    path('note/', RedirectView.as_view(url=reverse_lazy('note_list')), name='note'),
    path('note/list/', views.NoteListView.as_view(), name='note_list'),
    path('note/deleted/', views.NoteDeletedListView.as_view(), name='note_deleted_list'),

    path('note/<int:pk>/', views.NoteDetailView.as_view(), name='note_detail'),
    path('note/create/', views.NoteCreateView.as_view(), name='note_create'),
    path('note/<int:pk>/update/', views.NoteUpdateView.as_view(), name='note_update'),
    path('note/<int:pk>/delete/', views.NoteDeleteView.as_view(), name='note_delete'),
]
