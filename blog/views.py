from django.utils import timezone

from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from .models import Blogger, Blog, Comment
from .forms import UserRegisterForm, BloggerProfileForm

from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

# Create your views here.
def index(request):
    blogs = Blog.objects.all().count()
    comments = Comment.objects.all().count()
    bloggers = Blogger.objects.all().count()

    return render(request, 'index.html', context={
        'blogs_num': blogs,
        'comments_num': comments,
        'bloggers_num': bloggers,
    })

class BlogListView(generic.ListView):
    model = Blog
    paginate_by = 5

class BloggerListView(generic.ListView):
    model = Blogger

class BlogDetailView(generic.DetailView):
    model = Blog

class BloggerDetailView(generic.DetailView):
    model = Blogger

class CommentCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'blog.can_comment_blogs'

    model = Comment
    fields = ['description']

    def form_valid(self, form):
        form.instance.post_date = timezone.now()

        id = self.kwargs.get('pk')
        form.instance.blog = get_object_or_404(Blog, id=id)

        form.instance.author = Blogger.objects.get(user=self.request.user) 

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('blog_detail', kwargs={'pk': self.object.blog.pk})
    
def register(request):
    if request.method == 'POST':
       user_form = UserRegisterForm(request.POST)
       profile_form = BloggerProfileForm(request.POST)
       
       if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.registration_date = timezone.now()
            profile.save()

            return redirect('login')
    else:
        user_form = UserRegisterForm()
        profile_form = BloggerProfileForm()

    return render(
        request,
        'registration/register.html',
        context={
            'user_form': user_form,
            'profile_form': profile_form,
        }
    )

class BlogCreate(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.post_date = timezone.now()
        form.instance.author = Blogger.objects.get(user=self.request.user)

        return super().form_valid(form)
    