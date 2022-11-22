from django.urls import reverse_lazy
from django.views import generic, View
from .models import Opportunity, Answer, Question, Material, Proposal, Application, Post
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator




from django.http import HttpResponseRedirect, Http404
from .forms import ApplicationForm

from accounts.models import CustomUser
from accounts.forms import CustomUserCreationForm, CourseWidget

# Main Hub
class Hub(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'hub.html', {'user': request.user })
            


@method_decorator(login_required, name='dispatch')
class ProfileUpdate(generic.UpdateView):
    model = CustomUser
    fields = ["email",
            "first_name",
            "last_name",
            "course",
            "stage",
            "year",
            "cv",]
    template_name = 'profile_update.html'
    success_url="/hub/"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['course'].widget = CourseWidget()
        return form



# Opportunities
class Opportunities(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        full_list = Opportunity.objects.all().filter(visible=True)
        already_applied = full_list.filter(users=request.user)
        not_applied = full_list.filter(~Q(users=request.user)) # TODO: Here we need to check if the opportunity is visible!
        return render(request, 'opportunities.html',
            {'already_applied': already_applied, 'not_applied': not_applied})

@method_decorator(login_required, name='dispatch')
class OpportunityDetailView(generic.DetailView):
    model = Opportunity
    template_name = "opportunity_detail.html"

@login_required
def opportunities_apply(request, pk):
    opportunity = Opportunity.objects.get(pk=pk)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ApplicationForm(request.POST, pk=pk)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            questions = opportunity.questions.all()
            new_answers = []
            for i in range(0, len(questions)):
                answer = Answer(
                    user= request.user,
                    question = questions[i],
                    text = form.cleaned_data['char_field_%i' %i])
                answer.save()
                new_answers.append(answer)
            new_application = Application.objects.create(
                user=request.user, opportunity=opportunity)
            new_application.answers.set(new_answers)
            opportunity.users.add(request.user)
            # redirect to a new URL:
            return HttpResponseRedirect('/hub/opportunities')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ApplicationForm(pk=pk)
    
    context =   {
        'opportunity' : opportunity,
        'form' : form,
    }

    return render(request, 'opportunity_detail.html', context)


# Materials
class Materials(View):
    template_name = "materials.html"
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        full_list = Material.objects.all().filter(visible=True)
        workshops = full_list.filter(category="Workshop")
        featured_works = full_list.filter(category="Featured Works")
        courses = full_list.filter(category="Course")
        return render(request, 'materials.html',
            {'workshops': workshops, 'featured_works': featured_works, 'courses': courses})


# Proposals
class Proposals(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        full_list = Proposal.objects.filter(active=True)
        logged_email = request.user.email 
        already_applied = full_list.filter(applicants__email=logged_email)
        not_applied = full_list.filter(~Q(applicants__email=logged_email))
        return render(request, 'proposals.html',
            {'already_applied': already_applied, 'not_applied': not_applied})

class ProposalsManage(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        full_list = Proposal.objects.all()
        logged_email = request.user.email
        user_proposals = full_list.filter(author__email=logged_email)
        active_proposal = user_proposals.filter(active=True).first()
        unactive_proposals = user_proposals.filter(active=False)
        print(unactive_proposals)
        return render(request, 'proposal_manage.html',
            {'active_proposal': active_proposal, 'unactive_proposals': unactive_proposals})

@method_decorator(login_required, name='dispatch')
class ProposalCreateView(LoginRequiredMixin, generic.CreateView):
    model = Proposal
    template_name = "proposal_create.html"
    fields = ['title','description']
    success_url="/hub/proposals"

    def form_valid(self, form):
        form.instance.author = self.request.user
        proposal_deactivate_old(self.request)
        form.instance.active = True
        return super(ProposalCreateView, self).form_valid(form)

class ProposalApplicantsView(LoginRequiredMixin, View):
    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        proposal = Proposal.objects.get(pk=pk)
        applicants = proposal.applicants.all()
        user_or_404(request, proposal.author)
        return render(request, 'proposal_applicants.html', 
        {'proposal': proposal,'applicants': applicants})


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'post.html'


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

@login_required
def proposals_apply(request, pk):
    proposal = Proposal.objects.get(pk=pk)
    proposal.applicants.add(request.user)
    return HttpResponseRedirect('/hub/proposals')

@login_required
def proposal_switch(request, pk):
    proposal = Proposal.objects.get(pk=pk)
    user_or_404(request, proposal.author)
    if (proposal.active == False):
        proposal_deactivate_old(request)
        proposal.active = True
    elif (proposal.active == True):
        proposal.active = False
    proposal.save()
    return HttpResponseRedirect('/hub/proposals/manage')

@login_required
def profile_delete(request):
    if (request.user.is_authenticated):
        user = request.user
        user.delete()
        return HttpResponseRedirect('/')
    else: 
        raise Http404()

@login_required
def proposal_delete(request, pk):
    proposal = Proposal.objects.get(pk=pk)
    user_or_404(request, proposal.author)
    proposal.delete()
    return HttpResponseRedirect('/hub/proposals/manage')

def user_or_404(request, user):
    if(request.user != user):
        raise Http404()


# Auxiliary (non url) functions
def proposal_deactivate_old(request):
    all_proposals = Proposal.objects.all()
    user_proposals = all_proposals.filter(author=request.user)
    old_active_proposal = user_proposals.filter(active=True).first()
    if (old_active_proposal):
        old_active_proposal.active = False
        old_active_proposal.save()
