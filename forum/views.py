from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm
from .models import Thread, Post
from django.contrib import messages

# Create your views here.
def homeview(request):
    threads = Thread.objects.all()
    context = {'threads': threads}

    return render(request, 'forum/home_page.html', context)

def theme_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    posts = thread.posts.all().order_by('created_at')
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.thread = thread
                post.author = request.user
                post.save()
                return redirect('forum:thread_details', pk=pk)
        else:
            return redirect('login')
    else:
        form = PostForm()

    context = {
        'thread': thread,
        'posts': posts,
        'form': form
    }
    return render(request, 'forum/thread_details.html', context)

# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     form_class = PostForm
    
#     def form_valid(self, form):
#         user = self.request.user
#         last_post = Post.objects.filter(thread=self.kwargs['pk']).last()
#         if last_post:
#             if last_post.content == form.cleaned_data.get('content'):
#                 form.add_error('content', 'Ви вже надіслали таке саме повідомлення')
#                 return super().form_invalid(form)
#             if timezone.now() - last_post.created_at < timedelta(seconds=30):
#                 form.add_error('content', 'Ви пишете занадто часто. Очікуйте 30 секунд')
#                 return super().form_invalid(form)
                
                
#         form.instance.author = user
#         form.instance.thread = self.kwargs['pk']
#         return super().form_valid(form)
    
#     def get_success_url(self):
#         return self.object.thread.get_absolute_url()