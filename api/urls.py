from django.urls import path

from api.views import *

urlpatterns = [
    path("todo_classes/", TodoClassesAPI),
    # path("todo_class/<string:class_name>/", ),
    path("todos/", TodosAPI),
]