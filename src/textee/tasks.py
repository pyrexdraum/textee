from celery import shared_task

from .models import Snippet


@shared_task
def delete_expired_snippets():
    result = Snippet.inactive.all().delete()
    return f"Сниппетов удалено: {result[0]}"
