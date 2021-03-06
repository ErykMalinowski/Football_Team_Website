from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import View

from .models import Post, Comment, Player, Match, TeamSeason, Team, Season, PlayerStats
from .forms import PostForm, CommentForm


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'website/post_detail.html'

    form_class = PostForm

    model = Post


class PostEditView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'website/post_detail.html'

    form_class = PostForm

    model = Post


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'website/post_list.html'
    template_name = 'website/post_draft_list.html'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


# @login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            comment.approve()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'website/comment_form.html', {'form': form})


# @login_required
# def approve_comment(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     comment.approve()
#     return redirect('post_detail', pk=comment.post.pk)

class CommentEditView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'website/post_detail.html'

    form_class = CommentForm

    model = Comment


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


class AboutView(TemplateView):
    template_name = 'about.html'


class GalleryView(TemplateView):
    template_name = 'gallery.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class SquadView(ListView):
    model = Player

    def get_queryset(self):
        return Player.objects.all().order_by('number')


class MatchesView(ListView):
    model = Match

    def get_queryset(self):
        return Match.objects.order_by('round__id', 'id')


class ResetTeamSeason(View):
    def get(self, request):
        TeamSeason.objects.all().delete()

        for season in Season.objects.all():
            for team in Team.objects.all():
                TeamSeason.objects.create(team=team,
                                          season=season,
                                          matches=0,
                                          wins=0,
                                          draws=0,
                                          losts=0,
                                          goals_for=0,
                                          goals_against=0,
                                          points=0
                                          )
        for match in Match.objects.all():
            match.save()
        return HttpResponse("OK")


class TableView(ListView):
    model = TeamSeason

    def get_queryset(self):
        return TeamSeason.objects.all().order_by('-points')


class StatsView(ListView):
    model = PlayerStats

    def get_queryset(self):
        return PlayerStats.objects.all().order_by('player__number')
