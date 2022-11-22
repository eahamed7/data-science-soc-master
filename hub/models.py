from django.db import models
from accounts.models import CustomUser
from django.urls import reverse


# Opportunities
class Question(models.Model):
    name = models.CharField(max_length=500, help_text="Name of the question")
    def __str__(self):
        return self.name

class Answer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="Answer")
    text = models.TextField(max_length=1000)

    def __str__(self):
            return  self.question.name + ' - ' + self.text

class Opportunity(models.Model):
    title = models.CharField(max_length=100, help_text="Title of the opportunity")
    subtitle = models.CharField(max_length=300, help_text="Subtitle of the opportunity")
    description = models.TextField(max_length=1000, help_text="Description of the opportunity")
    questions = models.ManyToManyField(Question, blank=True, help_text="Additional questions related to the opportunity")
    users = models.ManyToManyField(CustomUser, blank=True, help_text="Users that have applied to this opportunity")
    image = models.ImageField(help_text="Image displayed for the opportunity", blank=True)
    visible = models.BooleanField(help_text="Is the opportunity currently visible", default=False)
    visible_to = models.ManyToManyField(CustomUser, blank=True, 
                                        default=None, help_text="Users that can see this opportunity, leave blank for open to all users",
                                        related_name="opportunity_visible")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('opportunity-detail', args=[str(self.pk)])

    class Meta:
        verbose_name_plural = "opportunities"

class Application(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, help_text="Applicant")
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, help_text="Application", related_name="applications")
    answers = models.ManyToManyField(Answer, help_text="Answers")
    successful = models.BooleanField(default=False, help_text="Has the application been successfull, or got an interview?")

    def __str__(self):
        return self.user.email + ' - ' + self.opportunity.title




# Materials
class Material(models.Model):
    title = models.CharField(max_length=100, help_text="Name of the matieral")
    description = models.TextField(max_length=1000, help_text="Description of the material")
    link = models.CharField(max_length=100, help_text="Link of the material", blank=True)
    attachment = models.FileField(help_text="File attached to the material", upload_to='materials/', blank=True)
    visible = models.BooleanField(help_text="Is the material currently visible?")

    CATEGORY_CHOICES = [ ("Workshop", "Workshop"),
                         ("Featured Works", "Featured Works"),
                         ("Course", "Course")]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.category + ' - ' + self.title

#Blogs 

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

POST_CATEGORIES = [ ("Partnerships", "Partnerships"),
                         ("Events", "Events"),
                         ("Technology", "Technology"),
                         ("Research", "Research"),
                         ("Committee", "Committee")]

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    subtitle = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(CustomUser, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateField(auto_now= True)
    content = models.TextField()
    created_on = models.DateField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='images/')
    status = models.IntegerField(choices=STATUS, default=0)
    
    category = models.CharField(max_length=20, choices=POST_CATEGORIES)
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

# Proposals
class Proposal(models.Model):
    title = models.CharField(max_length=100, help_text="Title of the proposal")
    description = models.TextField(max_length=1000, help_text="Description of the proposal")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, help_text="Author of the proposal", related_name="Author")
    applicants = models.ManyToManyField(CustomUser, blank=True, help_text="Applicants for the proposal", related_name="Applicants")
    active = models.BooleanField(help_text="Proposal actively displayed")

    def __str__(self):
        return self.author.email + ' - ' + self.title


