from catalog.models import Category


def categories(request):
    # Процессор для получения всех категорий
    return {
        'categories': Category.objects.all()
    }
