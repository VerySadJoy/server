from django.contrib.auth.password_validation import validate_password                                     
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import *


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = '__all__'
    
    def create(self, validated_data):
        return TestCase.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.description = validated_data.get("description", instance.description)
        instance.input = validated_data.get("input", instance.input)
        instance.status = validated_data.get("status", instance.status)
        instance.exit_code = validated_data.get("exit_code", instance.exit_code)
        instance.stdout = validated_data.stdout("stdout", instance.stdout)
        instance.save()
        return instance

class ProjectSerializer(serializers.ModelSerializer):
    project_testcases = TestCaseSerializer(many=True)

    class Meta:
        model = Project
        fields = '__all__'
    
    def create(self, validated_data):
        project_testcases_data = validated_data.pop("project_testcases")
        project = Project.objects.create(**validated_data)
        for project_testcase_data in project_testcases_data:
            TestCase.objects.create(user=user, **user_testcase_data)
        return project
  
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
    
    def create(self, validated_data):
        return Rating.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    user_projects = ProjectSerializer(many=True)
    ratings = RatingSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
                'user_id': {
                    'validators': [
                        UniqueValidator(
                            queryset=User.objects.all()
                        )
                    ]
                }
            }
    
    def create(self, validated_data):
        user_projects_data = validated_data.pop("user_projects")
        user = User.objects.create(**validated_data)
        for user_project_data in user_projects_data:
            Project.objects.create(user=user, **user_project_data)
        return user

    def update(self, instance, validated_data):
        instance.user_id = validated_data.get("user_id", instance.user_id)
        instance.save()
        return instance

class FileSerializer(serializers.ModelSerializer):
    attached = serializers.FileField()
    class Meta:
        model = File
        fields = '__all__'
    

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
