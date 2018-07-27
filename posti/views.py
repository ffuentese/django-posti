from django.shortcuts import render
from django.http import Http404
import django.urls
from django.views import generic
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from posti import models
from posti.models import Post
from .forms import PostForm, UpdateForm
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'posti/index.html'
    context_object_name = 'posti_list'
    paginate_by = 5

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        if self.request.user.is_authenticated:
            return Post.objects.filter(user=self.request.user).order_by('-pub_date')
        else:
            return Post.objects.filter(pub_date__lte=timezone.now(),
                                       ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'form': PostForm()})
        return context


class DetailView(generic.DetailView):
    model = Post
    template_name = 'posti/detail.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    context_object_name = 'post'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {'title': self.object.title, 'text': self.object.text}
        context.update({'form': UpdateForm(initial=data)})
        return context


class ResultView(generic.DetailView):
    model = Post
    template_name = 'posti/result.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_queryset(self):
        return Post.objects.all()


@require_POST
def add(request):
    f = PostForm(request.POST)
    if f.is_valid():
        posti = Post.create_post(title=f.cleaned_data['title'], text=f.cleaned_data['text'])
        if request.user.is_authenticated:
            posti.user = request.user
        posti.save()
        return HttpResponseRedirect(django.urls.reverse('posti:detail', args=(posti.uuid,)))
    else:
        messages.error(request, "Please fill out all the fields")
        return HttpResponseRedirect(django.urls.reverse('posti:index'))


@require_POST
def update(request, uuid):
    posti = get_object_or_404(Post, uuid=uuid)
    f = UpdateForm(request.POST)
    if f.is_valid():
        posti.title = f.cleaned_data['title']
        posti.text = f.cleaned_data['text']
        if posti.user == request.user:
            posti.save()
            return HttpResponseRedirect(django.urls.reverse('posti:detail', args=(posti.uuid,)))
        else:
            messages.error(request, "Post does not belong to the user.")
            return HttpResponseRedirect(django.urls.reverse('posti:detail', args=(posti.uuid,)))
    else:
        messages.error(request, "No title in form")
        return HttpResponseRedirect(django.urls.reverse('posti:detail', args=(posti.uuid,)))


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(django.urls.reverse('posti:index'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@require_POST
def delete(request):
    uuid = request.POST['uuid']
    posti = get_object_or_404(Post, uuid=uuid)
    if posti.user == request.user:
        posti.delete()
        return HttpResponseRedirect(django.urls.reverse('posti:index'))
    else:
        messages.error(request, "Post does not belong to the user.")
        return HttpResponseRedirect(django.urls.reverse('posti:detail', args=(posti.uuid,)))

@require_GET
def report(request, uuid):
    posti = get_object_or_404(Post, uuid=uuid)
    if posti:
        address = django.urls.reverse('posti:detail', args=(posti.uuid,))
        msg = 'El siguiente posti debería ser revisado: ' + address
        send_mail('Posti report', msg, 'test@whatever.es', ['txi.francisco@gmail.com'])
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)