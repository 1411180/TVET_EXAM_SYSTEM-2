from django.shortcuts import render, redirect
from .models import Department, Class, Unit, Exam, Question, StudentPortfolio
from .forms import StudentAnswerForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentPortfolio
from django.core.mail.import send_mail

def add_department(request):
    if request.method == 'POST':
        name = request.POST['name']
        Department.objects.create(name=name)
        return redirect('add_department')
    return render(request, 'exams/add_department.html')

# Add views for classes, units, exams, and questions similarly

def mark_exam(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    if request.method == 'POST':
        # Logic to mark the exam based on answers submitted
        # Calculate results and save to StudentPortfolio
        return redirect('results', exam_id=exam.id)
    return render(request, 'exams/mark_exam.html', {'exam': exam})

def mark_exam(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    questions = exam.questions.all()
    
    if request.method == 'POST':
        form = StudentAnswerForm(request.POST, exam_questions=questions)
        if form.is_valid():
            score = 0
            for question in questions:
                student_answer = form.cleaned_data[f'question_{question.id}']
                if student_answer == question.answer:
                    score += 1
            
            # Calculate percentage or any other metric
            total_questions = len(questions)
            result = (score / total_questions) * 100
            
            # Save result to student portfolio (you can modify this as needed)
            StudentPortfolio.objects.create(
                student_name='Student Name',  # Replace with actual student name
                exam=exam,
                result=result
            )
            
            return redirect('results', exam_id=exam.id)
    else:
        form = StudentAnswerForm(exam_questions=questions)

    return render(request, 'exams/mark_exam.html', {'form': form, 'exam': exam})

def results(request, exam_id):
    portfolios = StudentPortfolio.objects.filter(exam_id=exam_id)
    return render(request, 'exams/results.html', {'portfolios': portfolios})

def mark_exam(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    questions = exam.questions.all()
    
    if request.method == 'POST':
        form = StudentAnswerForm(request.POST, exam_questions=questions)
        if form.is_valid():
            score = 0
            for question in questions:
                student_answer = form.cleaned_data[f'question_{question.id}']
                if student_answer == question.answer:
                    score += 1
            
            # Calculate percentage or any other metric
            total_questions = len(questions)
            result = (score / total_questions) * 100
            
            # Automatically save result to student's portfolio
            student_name = request.user.username  # Assuming you're using Django's auth system
            StudentPortfolio.objects.create(
                student_name=student_name,  # Retrieve student's name from the logged-in user
                exam=exam,
                result=result
            )
            
            return redirect('results', exam_id=exam.id)
    else:
        form = StudentAnswerForm(exam_questions=questions)

    return render(request, 'exams/mark_exam.html', {'form': form, 'exam': exam})

def student_portfolio(request):
    portfolios = StudentPortfolio.objects.filter(student_name=request.user.username)
    return render(request, 'exams/student_portfolio.html', {'portfolios': portfolios})

@receiver(post_save, sender=StudentPortfolio)
def send_result_notification(sender, instance, **kwargs):
    student_email = instance.student_name + '@schooldomain.com'  # Or however you store emails
    send_mail(
        'Exam Results Uploaded',
        f'Dear {instance.student_name}, your results for {instance.exam.unit.name} have been uploaded. Your score is {instance.result}%.',
        'from@school.com',
        [student_email],
        fail_silently=False,
    )