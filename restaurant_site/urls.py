from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("feeds/", views.FeedsView.as_view(), name="feeds"),
    path("feeds/add/", views.FeedAddView.as_view(), name="feed_add"),
    path("feeds/<int:news_id>/", views.FeedDetailView.as_view(), name="feed_detail"),
    path("menu/", views.MenuView.as_view(), name="menu"),
    path("menu/add/", views.MenuItemAddView.as_view(), name="menu_item_add"),
    path(
        "menu/<int:item_id>/",
        views.MenuItemDetailView.as_view(),
        name="menu_item_detail",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
