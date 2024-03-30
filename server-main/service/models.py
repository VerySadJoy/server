from django.db import models

# Create your models here.
from django.db.models.deletion import CASCADE
import os


class TimeStampedModel(models.Model):
    # 최초 생성 일자
    created_at = models.DateTimeField(auto_now_add=True)
    # 최종 수정 일자
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(TimeStampedModel):
    # primary key
    user_id = models.CharField(max_length=100, primary_key=True)

    password = models.CharField(max_length=100)


class Project(TimeStampedModel):
    # primary key, 기존에 이미 디비가 존재하는데 새로운 필드를 추가하려니 에러 발생 -> default 값으로 우선처리
    project_id = models.AutoField(primary_key=True) 

    # foreign key
    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name="user_projects"
    )

    name = models.CharField(max_length=20, blank=False, null=False)
    description = models.CharField(max_length=100, blank=False, null=True)


class TestCase(TimeStampedModel):
    # primary key
    testcase_id = models.AutoField(primary_key=True)

    # foreign key
    project = models.ForeignKey(
        Project,
        on_delete=CASCADE,
        related_name="project_testcases"
    )

    description = models.CharField(max_length=100)
    input = models.CharField(max_length=100)
    output = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    exit_code = models.CharField(max_length=100)
    stdout = models.CharField(max_length=100)


class Rating(models.Model):
    # primary key & foreign key
    rating_id = models.AutoField(primary_key=True)

    # foreign key
    user_id = models.IntegerField()
    testcase_id = models.IntegerField()

    # 평점 1~5점
    content = models.IntegerField(default=3)


class File(models.Model):
    # 프로그래밍 언어 옵션
    LANGUAGE_CHOICES = (
        (1,'Python'),
        (2, 'Java'),
        (3,'JavaScript'), 
        (4,'C++'),
        (5,'C'),
    )

    # foreign key
    testcase_id = models.IntegerField()
    
    attached = models.FileField(blank=False, upload_to='code_txt')
    language = models.IntegerField(choices=LANGUAGE_CHOICES, blank=False)
    
    def get_file_name(self):
        return os.path.basename(self.attached.name)

