from django.urls import path

from api.views import *

urlpatterns = [
    path("todo_classes/", TodoClassesAPI),
    path("todo_class/<int:id>/", TodoClassAPI),
    path("todos/", TodosAPI),
    path("todos/<int:id>", TodosAPI),
    path("todo/<int:id>/", TodoAPI)

]