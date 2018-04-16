from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'^squad/$', views.SquadView.as_view(), name='squad'),
    url(r'^gallery/$', views.GalleryView.as_view(), name='gallery'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^contact/$', views.ContactView.as_view(), name='contact'),
    url(r'^post/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^post/new/$', views.CreatePostView.as_view(), name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.PostEditView.as_view(), name='post_edit'),
    url(r'^draft/$', views.DraftListView.as_view(), name='post_draft_list'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.PostDeleteView.as_view(), name='post_delete'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment, name='add_comment'),
    # url(r'^comment/(?P<pk>\d+)/approve/$', views.approve_comment, name='approve_comment'),
    url(r'^comment/(?P<pk>\d+)/edit/$', views.CommentEditView.as_view(), name='edit_comment'),
    url(r'^comment/(?P<pk>\d+)/delete/$', views.delete_comment, name='delete_comment'),
    url(r'^matches/$', views.MatchesView.as_view(), name='matches'),
    url(r'^reset-season/$', views.ResetTeamSeason.as_view()),
    url(r'^table/$', views.TableView.as_view(), name='table'),
    url(r'^stats/$', views.StatsView.as_view(), name='stats'),
]
