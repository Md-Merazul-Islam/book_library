
from celery import shared_task
from django.utils import timezone
from datetime import timedelta

@shared_task(name='library.tasks.archive_old_books')
def archive_old_books():
    from .models import Book
    
    cutoff_date = timezone.now().date() - timedelta(days=10*365)
    old_books = Book.objects.filter(published_date__lte=cutoff_date, is_archived=False)
    count = old_books.update(is_archived=True)
    return f"Archived {count} books published on or before {cutoff_date}"