from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Post, Comment
from .forms import PostForm


class PostListView(ListView):
    template_name = 'list.html'
    queryset = Post.objects.filter(published=True)
    paginate_by = 10


class PostDetailView(DetailView):
    template_name = 'detail.html'
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'create_update.html'
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:list')

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object().author:
            return redirect(reverse_lazy('accounts:login'))
        else:
            return super(PostUpdateView, self).dispatch(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'create_update.html'
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
