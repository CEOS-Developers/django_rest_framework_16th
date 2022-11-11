from django.urls import path

from api.views import *

urlpatterns = [
    path("todo_classes/", TodoClassesAPI),
    path("todo_classes/<int:id>/", TodoClassAPI),
    path("todos/", TodosAPI),
    path("todos/<int:id>/", TodoAPI)

]