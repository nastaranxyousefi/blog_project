from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views import generic

from .models import Post, Comment
from .forms import PostForm, CommentForm



# def post_list(request): 
#     posts = Post.objects.filter(status='published').order_by('-datetime_modified')
#     context = {
#         'posts' : posts, 
#     }
#     return render(request, 'blog/posts_list.html', context)

class PostListView(generic.ListView):
    model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(status='published').order_by('-datetime_modified')


# def post_detail(request, pk):
#     postObj = get_object_or_404(Post, id=pk)
#     context = {
#         'post' : postObj, 
#     }
#     return render(request, 'blog/post_detail.html', context)


# class PostDetailView(generic.DetailView):
#     model = Post
#     template_name = 'blog/post_detail.html'
#     context_object_name = 'post'
#     slug_field = 'slug'


def post_detail_view(request, slug, pk):
    post = get_object_or_404(Post, slug=slug, pk=pk)
    post_comments = post.comments.all()

    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
        return redirect('post_detail', slug=slug, pk=pk)


    context = {
        'post' : post,
        'comments' : post_comments,
        'comment_form' : comment_form,
    }
    return render(request, 'blog/post_detail.html', context)

    

# def post_create(request):
#     form = PostForm()
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('post_list')
        
    
#     context = {
#         'form' : form,
#         'title' : 'Add new post',
#     }
    
#     return render(request, 'blog/post_create.html', context)

class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'
   




# def post_update(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     form = PostForm(instance=post)
#     if request.method == 'POST':
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             form.save()
#             return redirect('post_list')
        
    
#     context = {
#         'form' : form,
#         'title' : 'Edit post',
#     }
    
#     return render(request, 'blog/post_create.html', context)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, generic.UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'blog/post_create.html'
    slug_field = 'slug'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user



# def post_delete(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == 'POST':
#         post.delete()
#         return redirect('post_list')

#     context = {
#         'post' : post,
#     }

#     return render(request, 'blog/post_delete.html', context)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('post_list')
    slug_field = 'slug'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
