from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .models import Movie, Category, Actor, Genre
from .forms import ReviewsForm


class GenreView:
    """Жанры и года выхода фильмов"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


class MoviesView(GenreView, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)


class MovieDetailView(GenreView, DetailView):
    """Полное описание фильма"""

    model = Movie
    slug_field = 'url'


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewsForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreView, DetailView):
    """Вывод информации об актере"""
    model = Actor
    template_name = 'movie_app/actor.html'
    slug_field = 'name'


class FilterMoviesView(GenreView, ListView):
    """Фильтр фильмов"""

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        )
        return queryset
