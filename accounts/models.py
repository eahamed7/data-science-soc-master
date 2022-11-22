from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from .validators import validate_file_size


import csv

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    table = str.maketrans({'@':None, '.':None})
    return 'user_{0}/{1}'.format(instance.email.translate(table), filename)

def total_courses():
    courses = []
        

    
# Courses among which the user can select theirs
class Course(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the course", unique=True)

    def __str__(self):
        return self.name

# Our Custom User manager
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    
# Custom user class extending Django's 
class CustomUser(AbstractUser):
    PHD_STUDENT = 'PhD'
    MASTERS_STUDENT = 'Msc'
    UNDERGRAD_STUDENT = "Und"
    STAGE_CHOICES = [ (PHD_STUDENT, "PhD"),
                      (MASTERS_STUDENT, "Master's degree"),
                      (UNDERGRAD_STUDENT, "Undergraduate degree"),
                      ]
    stage = models.CharField(
        max_length=3,
        choices=STAGE_CHOICES,
        default=UNDERGRAD_STUDENT,
    )

    username = models.CharField(max_length=40, unique=False, default='')

    email = models.EmailField(_('email address'), unique = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    GENDER_CHOICES = [ ('M', "Male"),
                        ('F', "Female"),
                        ('N', "Prefer not to say")
                    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default="N",
        help_text="Select your gender"
    )

    COURSES = total_courses()
    course = models.ForeignKey(Course, help_text="Type down and/or select your course from the list", on_delete=models.CASCADE, blank=True, null= True)

    year = models.IntegerField(
        choices=[(1, "First year"), (2, "Second year") , (3, "Third year")],
        default=1
    )

    cv = models.FileField(help_text="Upload your CV. Please do not upload any information that is confidential to you and you would not want to share with a recruiter.", upload_to=user_directory_path,
                          validators=[FileExtensionValidator(allowed_extensions=['pdf']),validate_file_size])

    aggregate_consent = models.BooleanField(help_text="Tick if you consent to having your information be aggregated and disclosed completely anonymously with sponsors for the purposes of improving the society.", default=False)

