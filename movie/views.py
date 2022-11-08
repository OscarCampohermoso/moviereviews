from django.shortcuts import render
from .models import Movie, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
# We import get_object_or_404 from django.shortcuts because it is a shortcut 
# function that returns a 404 error if the object is not found.

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html',
        {'searchTerm':searchTerm, 'movies': movies})

def about(request):
    return HttpResponse('<h1>Welcome to About Page</h1>')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = Review.objects.filter(movie=movie)
    return render(request, 'detail.html', {'movie': movie, 'reviews': reviews})

@login_required
def createreview(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'GET':
        form = ReviewForm()
        return render(request, 'createreview.html', {'form': ReviewForm(), 'movie': movie})
    else:
        try:
            form = ReviewForm(request.POST)
            newReview = form.save(commit=False)
            newReview.movie = movie
            newReview.user = request.user
            newReview.save()
            return redirect('detail', movie_id=movie.id)
        except ValueError:
            return render(request, 'createreview.html', {'form': form, 'movie': movie,
                    'error': 'Bad data passed in. Try again.'})

@login_required
def updatereview(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    movie = review.movie
    if request.method == 'GET':
        form = ReviewForm(instance=review)
        return render(request, 'updatereview.html', {'review': review, 'form': form})
    else:
        try:
            form = ReviewForm(request.POST, instance=review)
            form.save()
            return redirect('detail', movie_id=movie.id)
        except ValueError:
            return render(request, 'updatereview.html', { 'review': review, 'form': form, 
                    'error': 'Bad data in form. Try again.'})

@login_required
def deletereview(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    movie_id = review.movie.id
    review.delete()
    return redirect('detail', movie_id=movie_id)