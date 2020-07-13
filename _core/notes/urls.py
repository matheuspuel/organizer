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
from _core.notes import views

urlpatterns = views.NoteViewSet().url_patterns()
urlpatterns.append(
    path('', RedirectView.as_view(url=reverse_lazy('note_list')), name='notes_index')
)


# urlpatterns = [
#     # path('', RedirectView.as_view(url='note/'), name='notes'),
#     path('', views.notes, name='notes'),
#     path('note/', RedirectView.as_view(url='active/'), name='note'),
#     path('note/active/', views.note_list_active, name='note_active'),
#     path('note/deleted/', views.note_list_deleted, name='note_deleted'),
#
#     path('note/<int:id>/', views.note_detail, name='note_detail'),
#     path('note/add/', views.note_add, name='note_add'),
#     path('note/<int:id>/change/', views.note_change, name='note_change'),
#     path('note/<int:id>/delete/', views.note_delete, name='note_delete'),
# ]
