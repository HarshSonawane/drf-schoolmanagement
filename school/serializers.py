from rest_framework import serializers
from django.contrib.auth.models import User

from .models import School
from .models import Student
from .models import Grade
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        )


class SchoolSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = School
        fields = (
            'id',
            'user',
            'city',
            'pincode',
        )


class SchoolCreateSerializer(serializers.Serializer):
    password1 = serializers.CharField(max_length=255, write_only=True)
    password2 = serializers.CharField(max_length=255, write_only=True)
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    city = serializers.CharField(max_length=255)
    pincode = serializers.CharField(max_length=255)

    def save(self):
            password = self.validated_data['password1']
            password2 = self.validated_data['password2']
            pincode = self.validated_data['pincode']

            if password != password2:
                raise serializers.ValidationError({'password': 'Passwords must match'})

            if len(pincode) != 6:
                raise serializers.ValidationError({'pincode': 'Pincode must be 6 characters'})

            if User.objects.filter(email=self.validated_data['email']).exists():
                raise serializers.ValidationError({'email': 'Email already in use'})


            user = User(
                username=self.validated_data['email'],
                email=self.validated_data['email'],
                first_name=self.validated_data['name'],
                password=make_password(password)
            )

            user.save()

            school = School(
                city = self.validated_data['city'],
                pincode = pincode,
                user=user,
            )

            school.save()

            return school
    

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    school = SchoolSerializer()

    class Meta:
        model = Student
        fields = (
            'id',
            'user',
            'grade',
            'school',
        )

        
class StudentCreateSerializer(serializers.Serializer):
    password1 = serializers.CharField(max_length=255, write_only=True)
    password2 = serializers.CharField(max_length=255, write_only=True)
    name = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    grade = serializers.CharField(max_length=255)
    school = serializers.CharField(max_length=255)

    def save(self):
        password = self.validated_data['password1']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})

        if not School.objects.filter(id=self.validated_data['school']).exists():
            raise serializers.ValidationError({'school': 'Invalid School Id'})
        
        if not Grade.objects.filter(id=self.validated_data['grade']).exists():
            raise serializers.ValidationError({'grade': 'Invalid Grade Id'})

        if User.objects.filter(username=self.validated_data['username']).exists():
                raise serializers.ValidationError({'username': 'Usernmae already in use'})


        user = User(
                username=self.validated_data['username'],
                email=self.validated_data['username'],
                first_name=self.validated_data['name'],
                password=make_password(password)
            )

        user.save()

        student = Student(
            grade_id = self.validated_data['grade'],
            school_id = self.validated_data['school'],
            user = user
        )
        student.save()

        return student


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = (
            'id',
            'name',
        )