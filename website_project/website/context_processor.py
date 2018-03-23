from .models import TeamSeason


def team_seasons_processor(request):
    team_seasons = TeamSeason.objects.filter(season__is_active=True).order_by('-points')
    return {'teamseason_list': team_seasons}
