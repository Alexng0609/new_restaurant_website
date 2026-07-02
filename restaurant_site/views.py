from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import NewsFeed, MenuItem, Category

# Create your views here.


class IndexView(TemplateView):
    """Homepage view"""

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_news"] = NewsFeed.objects.filter(is_active=True)[:3]
        context["featured_items"] = MenuItem.objects.filter(is_available=True)[:6]
        return context


class FeedsView(ListView):
    """News feeds view"""

    template_name = "feeds.html"
    context_object_name = "news_feeds"

    def get_queryset(self):
        return NewsFeed.objects.filter(is_active=True)


class FeedDetailView(DetailView):
    """Single news feed detail view"""

    template_name = "feed_detail.html"
    context_object_name = "news"

    def get_object(self):
        return get_object_or_404(NewsFeed, id=self.kwargs["news_id"], is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_news"] = NewsFeed.objects.filter(is_active=True).exclude(
            id=self.kwargs["news_id"]
        )[:3]
        return context


class MenuView(ListView):
    """Menu view with categories"""

    template_name = "menu.html"
    context_object_name = "menu_items"

    def get_queryset(self):
        selected_category = self.request.GET.get("category")
        if selected_category:
            return MenuItem.objects.filter(
                category_id=selected_category, is_available=True
            )
        return MenuItem.objects.filter(is_available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.prefetch_related("items").all()
        context["selected_category"] = self.request.GET.get("category")
        return context


class MenuItemDetailView(DetailView):
    """Single menu item detail view"""

    model = MenuItem
    template_name = "menu_item_detail.html"
    context_object_name = "item"
    pk_url_kwarg = "item_id"
