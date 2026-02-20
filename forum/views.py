from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Theme, Post
from django.contrib import messages

# Create your views here.
def homeview(request):
    themes = Theme.objects.all()
    context = {'themes': themes}

    return render(request, 'forum/home_page.html', context)

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