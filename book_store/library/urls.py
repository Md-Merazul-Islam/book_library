from .views import BookCreateView, AuthorCreateView, BookListView, AuthorListView
from django.urls import path
urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('authors/create/', AuthorCreateView.as_view(), name='author-create'),
]