from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Thread, Post
from .forms import PostForm, PostThread

# Головна сторінка зі списком усіх тем
class HomeView(ListView):
    model = Thread
    template_name = 'forum/home_page.html'
    context_object_name = 'threads'
    ordering = ['-created_at']

# Детальний перегляд теми та обробка нових повідомлень
class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'forum/thread_details.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Отримуємо всі повідомлення, пов'язані з цією темою
        context['posts'] = self.object.posts.all().order_by('created_at')
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        # Перевірка авторизації користувача
        if not request.user.is_authenticated:
            return redirect('login')
        
        self.object = self.get_object()
        form = PostForm(request.POST)
        
        if form.is_valid():
            user = request.user
            content = form.cleaned_data.get('content')
            
            # Логіка захисту від спаму та дублікатів
            last_post = Post.objects.filter(thread=self.object, author=user).last()
            
            if last_post:
                # Перевірка на однаковий зміст
                if last_post.content == content:
                    messages.error(request, "Ви вже надіслали таке саме повідомлення!")
                    return self.render_to_response(self.get_context_data(form=form))
                
                # Перевірка на частоту публікації (30 секунд)
                if timezone.now() - last_post.created_at < timedelta(seconds=30):
                    messages.warning(request, "Ви пишете занадто часто. Зачекайте 30 секунд.")
                    return self.render_to_response(self.get_context_data(form=form))

            # Збереження повідомлення
            post = form.save(commit=False)
            post.thread = self.object
            post.author = user
            post.save()
            
            messages.success(request, "Ваше повідомлення успішно додано!")
            return redirect('forum:thread_details', pk=self.object.pk)
        
        return self.render_to_response(self.get_context_data(form=form))

# Створення нової теми
class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    form_class = PostThread
    template_name = 'forum/thread_add.html'
    
    # Автоматичне призначення автора перед збереженням
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Тему успішно створено!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum:home')