from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)

    def _str_(self):
        return self.name

class Class(models.Model):
    department = models.ForeignKey(Department, related_name='classes', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def _str_(self):
        return self.name

class Unit(models.Model):
    class_instance = models.ForeignKey(Class, related_name='units', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def _str_(self):
        return self.name

class Exam(models.Model):
    unit = models.ForeignKey(Unit, related_name='exams', on_delete=models.CASCADE)
    number_of_questions = models.PositiveIntegerField()
    is_completed = models.BooleanField(default=False)

    def _str_(self):
        return f"Exam for {self.unit.name}"

class Question(models.Model):
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    is_multiple_choice = models.BooleanField(default=False)
    answer = models.TextField()  # Correct answer; hidden from examinee

    def _str_(self):
        return self.question_text
    
class Question(models.Model):
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    is_multiple_choice = models.BooleanField(default=False)
    answer = models.TextField()  # Correct answer; hidden from examinee
    option_a = models.CharField(max_length=200, blank=True)
    option_b = models.CharField(max_length=200, blank=True)
    option_c = models.CharField(max_length=200, blank=True)
    option_d = models.CharField(max_length=200, blank=True)

    def _str_(self):
        return self.question_text    

class StudentPortfolio(models.Model):
    student_name = models.CharField(max_length=100)
    exam = models.ForeignKey(Exam, related_name='portfolios', on_delete=models.CASCADE)
    result = models.FloatField()

    def _str_(self):
        return f"{self.student_name}'s Portfolio"
    
class StudentPortfolio(models.Model):
    student_name = models.CharField(max_length=100)
    exam = models.ForeignKey(Exam, related_name='portfolios', on_delete=models.CASCADE)
    result = models.FloatField()

    def _str_(self):
        return f"{self.student_name}'s Portfolio"    