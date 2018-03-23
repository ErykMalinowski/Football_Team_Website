from django.contrib import admin

from .models import Post, Comment, Season, Round, Team, Match, TeamSeason, Player, PlayerStats


class MatchAdmin(admin.ModelAdmin):

    list_filter = ['round']


class PlayerAdmin(admin.ModelAdmin):

    list_display = ['number', 'name', 'surname', 'position']


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Season)
admin.site.register(Round)
admin.site.register(Team)
admin.site.register(Match, MatchAdmin)
admin.site.register(TeamSeason)
admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerStats)



