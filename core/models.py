from django.db import models
from authentication.models import User
from django.utils import timezone


class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    course_image = models.ImageField(upload_to='media')
    teacher_name = models.CharField(max_length=50)
    course_code = models.CharField(max_length=50, null=False, default='CSC 101')
    teacher_details = models.TextField()
    course_description = models.TextField()
    created_at = models.DateField(default=timezone.now())
    end_date = models.CharField(max_length=20)

    def __str__(self):
        return self.course_name

'''
Data Structures are a specialized means of organizing and storing data in computers in such a way 
that we can perform operations on the stored data more efficiently. Data structures have a wide and 
diverse scope of usage across the fields of Computer Science and Software Engineering.
'''

class Assignment(models.Model):
    assign_status = (
            ('Completed','Completed'),
            ('Pending','Pending'),
            ('Incomplete','Incomplete')
        )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    assignment_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    student_score = models.CharField(max_length=60, null=True)
    marks = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=assign_status, default='Incomplete')
    duration = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.title

class Exam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    marks = models.CharField(max_length=20)
    duration = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.title

class AssignmentSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment_course = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True, blank=False)
    assignment_course_code = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=False)
    name = models.CharField(max_length=100)
    university_id = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.university_id

class ExamSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam_course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    exam_course_code = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True, blank=False)
    name = models.CharField(max_length=100)
    university_id = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.university_id
