from django.shortcuts import render
from django.views import generic, View

# Create your views here.
class Blog(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'blog/blog_index_page.html')