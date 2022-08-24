from rest_framework import generics
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from .models import School
from .models import Student
from .models import Grade

from .serializers import SchoolSerializer
from .serializers import StudentSerializer
from .serializers import GradeSerializer
from .serializers import SchoolCreateSerializer
from .serializers import StudentCreateSerializer



class SchoolListAndCreateView(generics.ListCreateAPIView):
    serializer_class = SchoolSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return School.objects.filter(is_active=True)

    def post(self, request, *args, **kwargs):
        self.serializer_class = SchoolCreateSerializer
        return super().post(request, *args, **kwargs)


class SchoolDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SchoolSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        return School.objects.get(id=self.kwargs.get("pk"), is_active=True)

    def patch(self, request, *args, **kwargs):
        self.serializer_class = SchoolCreateSerializer
        return super().post(request, *args, **kwargs)


class StudentListAndCreateView(generics.ListCreateAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        if self.kwargs.get("school_pk"):
            if self.request.query_params.get("grade"):
                return Student.objects.filter(
                    school__id=self.kwargs.get("school_pk"),
                    grade__id=self.request.query_params.get("grade"),
                    is_active=True
                    )
            return Student.objects.filter(school__id=self.kwargs.get("school_pk"), is_active=True)
        return Student.objects.filter(is_active=True)

    def get(self, request, *args, **kwargs):
        self.permission_classes = (permissions.IsAuthenticated,)
        self.authentication_classes = (TokenAuthentication,)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = StudentCreateSerializer
        return super().post(request, *args, **kwargs)


class GradeListAndCreateView(generics.ListCreateAPIView):
    serializer_class = GradeSerializer 
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return Grade.objects.filter(is_active=True)

