from django.urls import path, include
from rest_framework import routers

from service.views import *

project_list = ProjectViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
project_detail = ProjectViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
testcase_list = TestCaseViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
testcase_detail = TestCaseViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
file_list = FileViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
file_detail = FileViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
urlpatterns = [
    path("projects", project_list, name='project-list'),
    path("projects/<int:pk>", project_detail, name='project-detail'),
    path("testcases", testcase_list, name='testcase-list'),
    path("testcases/<int:pk>", testcase_detail, name='testcase-detail'),
    path("files", file_list, name='file-list'),
    path("files/<int:pk>", file_detail, name='file-detail'),
]
