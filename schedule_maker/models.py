from django.db import models
from .process_data import create_classes


class Student(models.Model):
    powerschool_id = models.CharField(max_length=20, default="")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    grade_levels = [
        (6, 'Grade 6'),
        (7, 'Grade 7'),
        (8, 'Grade 8')
                    ]
    previous_grade = models.CharField(max_length=5)
    grade = models.IntegerField(choices=grade_levels, default=6)
    gender_types = [
        ('M', 'Male'),
        ('F', 'Female')
                    ]
    gender = models.CharField(max_length=6, choices=gender_types, default='M')
    social_grouping = models.CharField(max_length=200, default="")
    language_types = [
        ('N', 'Native'),
        ('NN', 'Non-Native'),
        ('None', 'None')
    ]
    arabic = models.CharField(max_length=6, choices=language_types, default='NN')
    islamic = models.CharField(max_length=6, choices=language_types, default='None')
    takes_native_arabic = models.BooleanField(default=False)
    takes_islamic = models.BooleanField(default=False)
    nationality = models.CharField(max_length=200, default="")
    ell = models.CharField(max_length=1, default="N") # Y or N
    send = models.CharField(max_length=1, default="N") # Y or N
    behavior = models.CharField(max_length=200, default="") # Explanation of child's behavior issues if any
    hmp = models.CharField(max_length=200, default="")
    hORl_types = [
        ('N', 'None'),
        ('H', 'H'),
        ('L', 'L')
    ]
    hORl = models.CharField(max_length=4, choices=hORl_types, default='N')
    friend1 = models.IntegerField(max_length=3, default=-1) # First will be name, then changed to number
    friend2 = models.IntegerField(max_length=3, default=-1)
    friend3 = models.IntegerField(max_length=3, default=-1)
    friend4 = models.IntegerField(max_length=3, default=-1)
    friend5 = models.IntegerField(max_length=3, default=-1)
    friends_unprocessed = models.CharField(max_length=300) # Friends as they were written in the CSV file
    avoid = models.CharField(max_length=200, default="")
    notes = models.CharField(max_length=300, default="")



    def __str__(self):
        return self.first_name + " " + self.last_name

    @staticmethod
    def distribute_to_classes(grade):
        students = list(Student.objects.filter(grade=grade).values('first_name',
                                                                   'last_name',
                                                                   'takes_islamic',
                                                                   'takes_native_arabic',
                                                                   'gender',
                                                                   'friend1',
                                                                   'friend2',
                                                                   'friend3',
                                                                   'friend4',
                                                                   'friend5',
                                                                   'id'))
        students = [list(x.values()) for x in students]
        return create_classes(students)

