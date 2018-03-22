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


class Round(models.Model):
    name = models.CharField(max_length=32)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)


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
    score_home = models.PositiveSmallIntegerField()
    score_away = models.PositiveSmallIntegerField()
    round = models.ForeignKey(Round, on_delete=models.CASCADE)


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
