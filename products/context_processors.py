from .models import Category

def categories_processor(request):
    """
    Контекстный процессор для добавления списка всех категорий
    в контекст каждого шаблона.
    """
    return {
        'categories': Category.objects.all()
    }