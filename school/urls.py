from django.urls import path
from rest_framework.authtoken import views

from .views import ChangePasswordView
from .views import GradeListAndCreateView
from .views import SchoolCreateView
from .views import SchoolDetailView
from .views import SchoolListView
from .views import StudentCreateView
from .views import StudentDetailView
from .views import StudentListView


urlpatterns = [
    path("schools/", SchoolListView.as_view(), name="schools"),
    path("schools/signup/", SchoolCreateView.as_view(), name="schools"),
    path("schools/<int:pk>/", SchoolDetailView.as_view(), name="schools"),
    path(
        "schools/<int:school_pk>/students/",
        StudentListView.as_view(),
        name="school-students",
    ),
    path(
        "schools/<int:school_pk>/students/<int:pk>/",
        StudentDetailView.as_view(),
        name="school-students",
    ),
    path(
        "schools/<int:school_pk>/students/<int:pk>/change_password/",
        ChangePasswordView.as_view(),
        name="change_password",
    ),
    path("students/", StudentListView.as_view(), name="students"),
    path("students/<int:pk>/", StudentDetailView.as_view(), name="student-details"),
    path(
        "students/<int:pk>/change_password/",
        ChangePasswordView.as_view(),
        name="change_password",
    ),
    path("students/signup/", StudentCreateView.as_view(), name="students"),
    path("grades/", GradeListAndCreateView.as_view(), name="students"),
    path("login/", views.obtain_auth_token, name="login"),
]
