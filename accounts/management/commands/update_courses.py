from django.core.management.base import BaseCommand, CommandError
from accounts.models import Course
import csv


class Command(BaseCommand):
    help = "Update the courses models from a 'degrees.csv' file "

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
            with open('degrees.csv') as f:
                if f is None:
                    "No 'degrees.csv' file was found"
                else:
                    reader = csv.reader(f)
                    for row in reader:
                        if (Course.objects.filter(name=row[0])):
                            pass
                        else: 
                            new_course = Course(name=row[0])
                            new_course.save()
                        
                            
                
