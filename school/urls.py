from django.urls import path
from .views import SchoolListAndCreateView
from .views import StudentListAndCreateView
from .views import GradeListAndCreateView
from .views import SchoolDetailView

from rest_framework.authtoken import views


urlpatterns = [
    path('schools/', SchoolListAndCreateView.as_view(), name='schools'),
    path('schools/<int:pk>/', SchoolDetailView.as_view(), name='schools'),
    path('schools/<int:school_pk>/students/', StudentListAndCreateView.as_view(), name='school-students'),
    path('students/', StudentListAndCreateView.as_view(), name='students'),
    path('grades/', GradeListAndCreateView.as_view(), name='students'),
    path('login/', views.obtain_auth_token, name='login'),
]
