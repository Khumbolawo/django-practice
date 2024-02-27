from django.forms import BaseModelForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.views.generic import (ListView, 
                                  DetailView, 
                                  CreateView,
                                  UpdateView,
                                  DeleteView)

# Create your views here.

#function based views for home page i learned first
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

#class based view for home page
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

#view for post details
class PostDetailView(DetailView):
    model = Post

#view for post creation with extra parameters for validation
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
#view for post updating with extra parameters for validation
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    #first validation function. checks current logged user was author of the post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    #2nd validation function. stops other users from updating another user's post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

#view for deleting posts. also includes same user tests
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    #success url attribute that takes you to homepage when you delete
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

#function based view for about page
def about(request):
    return render(request, 'blog/about.html', {'title': 'about'})

