from .models import Category

def categories_processor(request):
    """
    Контекстный процессор для добавления списка всех категорий
    в контекст каждого шаблона.
    """
    # Мы возвращаем словарь. Ключ 'categories' - это имя переменной,
    # которая станет доступна во всех шаблонах.
    return {
        'categories': Category.objects.all()
    }