from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="test"),
    path("signup/", views.sign_up, name="signup"),
    path("createproject", views.create_project, name="create_project"),
    path('edit/<int:project_id>', views.edit_project, name='edit_project')
]
