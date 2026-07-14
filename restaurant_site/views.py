from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from .models import NewsFeed, MenuItem, Category
from .forms import NewsFeedForm, MenuItemForm
from accounts.utils import (
    is_manager_or_admin,
)  # utils.py lives in accounts, not this app


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


class FeedAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Create a new news feed post — replaces the old /admin/.../add/ link
    that feeds.html's "Thêm Tin Tức Mới" button used to point at."""

    model = NewsFeed
    form_class = NewsFeedForm
    template_name = "feed_form.html"

    def test_func(self):
        # Was previously just is_staff, which let plain staff manage news
        # posts too. Feed management is manager+/admin only, same as menu
        # items — staff only gets the Order page.
        return is_manager_or_admin(self.request.user)

    def get_success_url(self):
        return reverse("feed_detail", kwargs={"news_id": self.object.id})


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


class MenuItemAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Create a new menu item — replaces the old /admin/.../add/ link
    that menu.html's "Thêm Món Ăn" button used to point at."""

    model = MenuItem
    form_class = MenuItemForm
    template_name = "menu_form.html"

    def test_func(self):
        return is_manager_or_admin(self.request.user)

    def get_success_url(self):
        return reverse("menu_item_detail", kwargs={"item_id": self.object.id})
