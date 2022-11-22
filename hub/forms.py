from django import forms
from .models import Opportunity, Question, Answer


class ApplicationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        super(ApplicationForm, self).__init__(*args, **kwargs)
        questions = Opportunity.objects.get(pk=pk).questions.all()
        for i in range(0, len(questions)):
            question_label = questions[i].name
            self.fields['char_field_%i' %i] = forms.CharField(max_length=1000, label = question_label + ' - max 150 words (approx)', widget = forms.Textarea(attrs={'placeholder': '','rows':4, 'cols':15}))



"""
class RiskForm(forms.Form):
def __init__(self, *args, **kwargs):
    programid = kwargs.pop('programid', None)
    super(RiskForm, self).__init__(*args, **kwargs)
    for i in range(0,len(Program.objects.get(id=programid).char_set.all())):
        charid = Program.objects.get(id=programid).char_set.all()[i].id
        charlabel = Program.objects.get(id=programid).char_set.all()[i].label
        self.fields['char_field_%i' %i] = forms.ModelChoiceField(Char.objects.get(id=charid).cat_set.all(), label=charlabel)

"""