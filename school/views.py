from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Grade
from .models import School
from .models import Student
from .serializers import GradeSerializer
from .serializers import SchoolCreateSerializer
from .serializers import SchoolSerializer
from .serializers import StudentCreateSerializer
from .serializers import StudentSerializer


class SchoolListView(generics.ListAPIView):
    serializer_class = SchoolSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return School.objects.filter(is_active=True)


class SchoolCreateView(generics.CreateAPIView):
    serializer_class = SchoolCreateSerializer


class SchoolDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SchoolSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        return School.objects.get(id=self.kwargs.get("pk"), is_active=True)


class StudentListView(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        if self.kwargs.get("school_pk"):

            # this can be handled seprately through the custom permisions
            user = self.request.user
            school = get_object_or_404(School, pk=self.kwargs.get("school_pk"))
            if user.pk != school.user.pk:
                return Student.objects.none()

            if self.request.query_params.get("grade"):
                return Student.objects.filter(
                    school=school,
                    grade__id=self.request.query_params.get("grade"),
                    is_active=True,
                )
            return Student.objects.filter(school=school, is_active=True)
        return Student.objects.filter(is_active=True)


class StudentCreateView(generics.CreateAPIView):
    serializer_class = StudentCreateSerializer


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        return Student.objects.get(id=self.kwargs.get("pk"), is_active=True)


class GradeListAndCreateView(generics.ListCreateAPIView):
    serializer_class = GradeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return Grade.objects.filter(is_active=True)


class ChangePasswordView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        school = None
        old_password = request.data.get("old_password", None)
        new_password_1 = request.data.get("new_password_1", None)
        new_password_2 = request.data.get("new_password_2", None)

        if (new_password_1 is None) or (new_password_2 is None):
            return Response(
                data={"message": "New password 1 and New Password 2 are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if new_password_1 != new_password_2:
            return Response(
                data={"message": "New password 1 and New Password 2 are different"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if self.kwargs.get("school_pk"):
            try:
                school = School.objects.get(pk=self.kwargs.get("school_pk"))
            except School.DoesNotExist:
                return Response(
                    data={"message": "Invalid school"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if school is None and old_password is None:
            return Response(
                data={"message": "Old password is mandatory"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            if self.kwargs.get("school_pk"):
                user = User.objects.get(pk=self.kwargs.get("pk"))
            else:
                if self.kwargs.get("pk") != user.pk:
                    return Response(
                        data={"message": "You are not allowed to change your password"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    if user.check_password(old_password):
                        return Response(
                            data={"message": "Entered incorrect old password"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

            user.password = make_password(new_password_1)
            user.save()
            return Response(
                data={"message": "Password changed successfully"},
                status=status.HTTP_200_OK,
            )

        except User.DoesNotExist:
            return Response(
                data={"message": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST
            )
