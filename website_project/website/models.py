from django.db import models
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('website.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=64)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text


class Season(models.Model):
    name = models.CharField(max_length=32)
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Round(models.Model):
    name = models.CharField(max_length=32)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Team(models.Model):
    logo = models.FileField()
    logo_icon = models.FileField()
    name = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    team_home = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_home")
    team_away = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_away")
    score_home = models.PositiveSmallIntegerField(null=True, blank=True)
    score_away = models.PositiveSmallIntegerField(null=True, blank=True)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)

    def __str__(self):
        if self.score_home is not None and self.score_away is not None:
            return self.team_home.name + "-" + self.team_away.name + " " + str(self.score_home) + ":" + str(self.score_away)
        else:
            return self.team_home.name + "-" + self.team_away.name + " -:- "

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.score_home is not None and self.score_away is not None:
            ts_home = self.team_home.teamseason_set.filter(season__is_active=True).first()
            ts_away = self.team_away.teamseason_set.filter(season__is_active=True).first()

            ts_home.matches = ts_home.matches + 1
            ts_away.matches = ts_away.matches + 1
            ts_home.goals_for += self.score_home
            ts_away.goals_for += self.score_away
            ts_home.goals_against += self.score_away
            ts_away.goals_against += self.score_home

            if self.score_home > self.score_away:
                ts_home.wins += 1
                ts_away.losts += 1
                ts_home.points += 3

            if self.score_home < self.score_away:
                ts_home.losts += 1
                ts_away.wins += 1
                ts_away.points += 3

            if self.score_home == self.score_away:
                ts_home.draws += 1
                ts_away.draws += 1
                ts_home.points += 1
                ts_away.points += 1

            ts_home.save()
            ts_away.save()


class TeamSeason(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    matches = models.PositiveSmallIntegerField()
    wins = models.PositiveSmallIntegerField()
    draws = models.PositiveSmallIntegerField()
    losts = models.PositiveSmallIntegerField()
    goals_for = models.PositiveSmallIntegerField()
    goals_against = models.PositiveSmallIntegerField()
    points = models.SmallIntegerField()

    def __str__(self):
        return self.team.name


class Player(models.Model):
    number = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    position = models.CharField(max_length=32)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name + " " + self.surname


class PlayerStats(models.Model):
    appearances = models.PositiveSmallIntegerField(null=True)
    goals = models.PositiveSmallIntegerField(null=True)
    conceded = models.PositiveSmallIntegerField(null=True)
    clean_sheets = models.PositiveSmallIntegerField(null=True)
    assists = models.PositiveSmallIntegerField(null=True)
    yellow_cards = models.PositiveSmallIntegerField(null=True)
    red_cards = models.PositiveSmallIntegerField(null=True)
    minutes = models.PositiveSmallIntegerField(null=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return self.player.name + " " + self.player.surname