from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'IosTrade - Главная'
        context['content'] = "Магазин техники Apple"
        return context


class AboutView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О нас - iOStrade' # Обнови заголовок для вкладки браузера
        return context