from django import forms

class StudentAnswerForm(forms.Form):
    def _init_(self, *args, **kwargs):
        exam_questions = kwargs.pop('exam_questions')
        super(StudentAnswerForm, self)._init_(*args, **kwargs)
        
        for question in exam_questions:
            if question.is_multiple_choice:
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    choices=[
                        (question.answer, question.answer),
                        (question.option_a, question.option_a),
                        (question.option_b, question.option_b),
                        (question.option_c, question.option_c),
                        (question.option_d, question.option_d),
                    ],
                    widget=forms.RadioSelect,
                    label=question.question_text
                )
            else:
                self.fields[f'question_{question.id}'] = forms.CharField(
                    label=question.question_text,
                    widget=forms.Textarea
                )