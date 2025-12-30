from .models import Author, Book
from rest_framework import serializers
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'birth_date']


class BookSerializer(serializers.ModelSerializer):
    author_details = AuthorSerializer(read_only=True,)

    class Meta:
        model = Book
        fields = ['id', 'title',"author", "is_archived",  'published_date', 'genre', 'language', 'created_at', 'updated_at',"author_details"]