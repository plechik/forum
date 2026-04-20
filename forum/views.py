from django.views.generic import DeleteView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Theme, Thread, Post
from .forms import PostForm, PostThread
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.http import JsonResponse
import pymorphy3

# Головна сторінка зі списком усіх тем
class HomeView(ListView):
    model = Theme
    template_name = 'forum/home_page.html'
    context_object_name = 'themes'
    ordering = ['created_at']

class ThreadsView(ListView):
    model = Thread
    template_name = 'forum/threads.html'
    context_object_name = 'threads'
    ordering = ['-created_at']
    

    def get_queryset(self):
        t_id = self.kwargs.get('pk')
        return Thread.objects.filter(theme_id=t_id)
    
    def get_context_data(self, **kwargs):
        # Сначала получаем стандартный контекст (список тредов)
        context = super().get_context_data(**kwargs)
        
        # Находим объект темы по pk из URL
        # Используем get_object_or_404 для безопасности
        context['current_theme'] = get_object_or_404(Theme, pk=self.kwargs.get('pk'))
        
        return context


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
                    messages.error(request, "Ви вже надсилали таке саме повідомлення!")
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
            
            messages.success(request, "Ваш коментар додано!")
            return redirect('forum:thread_details', pk=self.object.pk)
        
        return self.render_to_response(self.get_context_data(form=form))

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('forum:thread_details', kwargs={'pk': self.get_object().thread.pk})

    def test_func(self):
        return self.request.user == self.get_object().author

    def get(self, request, *args, **kwargs):
        return redirect(self.get_success_url())

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Коментар видалено.")
        return super().delete(request, *args, **kwargs)
    
class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    form_class = PostThread
    template_name = 'forum/thread_add.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Достаем объект темы по ID из URL, чтобы показать название в крошках
        context['current_theme'] = get_object_or_404(Theme, pk=self.kwargs.get('pk'))
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.theme = get_object_or_404(Theme, pk=self.kwargs['pk'])
        messages.success(self.request, "Тему успішно створено!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('forum:thread_details', kwargs={'pk': self.object.pk})

class SearchView(ListView):
    model = Thread
    template_name = 'forum/search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Thread.objects.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(content__icontains=query)
            ).distinct()
        return Thread.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context

@login_required
def profile_view(request):
    user = request.user
    
    if request.method == 'POST':
        if 'username' in request.POST:
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.save()
            messages.success(request, 'Дані оновлено')
            tab = request.POST.get('tab', 'profile')
            return redirect(f"{request.path}?tab={tab}")
        
        elif 'current_password' in request.POST:
                # Смена пароля
                user = request.user
                current_pass = request.POST.get('current_password')
                new_pass = request.POST.get('new_password')
                confirm_pass = request.POST.get('confirm_password')

                if not user.check_password(current_pass):
                    messages.error(request, 'Неправильний поточний пароль')
                elif new_pass != confirm_pass:
                    messages.error(request, 'Нові паролі не збігаються')
                elif len(new_pass) < 8:
                    messages.error(request, 'Пароль занадто короткий (мінімально 8 символів)')
                else:
                    user.set_password(new_pass)
                    user.save()
                    update_session_auth_hash(request, user) # Чтобы не разлогинило
                    messages.success(request, 'Пароль успішно змінено!')
                tab = request.POST.get('tab', 'profile')
                return redirect(f"{request.path}?tab={tab}")

    user_threads = Thread.objects.filter(author=user).order_by('-created_at')
    
    user_posts = Post.objects.filter(author=user).order_by('-created_at')

    context = {
        'user_threads': user_threads,
        'user_posts': user_posts,
    }
    
    return render(request, 'forum/account/account.html', context)

morph_ru = pymorphy3.MorphAnalyzer(lang='ru')
morph_uk = pymorphy3.MorphAnalyzer(lang='uk')

def normalize_word(word):
    res_ru = morph_ru.parse(word)[0].normal_form
    res_uk = morph_uk.parse(word)[0].normal_form
    # Возвращаем список из обоих вариантов, чтобы искать по обоим
    return list(set([res_ru, res_uk, word.lower()]))

def search_api(request):
    query_text = request.GET.get('q', '').strip()
    if len(query_text) > 2:
        words = query_text.split()
        q_objects = Q()
        
        for word in words:
            forms = normalize_word(word)
            word_q = Q()
            for f in forms:
                word_q |= Q(title__icontains=f) | Q(content__icontains=f)
            q_objects &= word_q # Слово (или его формы) должно быть в результате
            
        results = Thread.objects.filter(q_objects).distinct()[:5]
        
        data = [{
            'id': r.id,
            'title': r.title,
            'url': f"/threads/{r.id}/"
        } for r in results]
        
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)