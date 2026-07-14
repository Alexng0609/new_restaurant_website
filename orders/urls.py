from django.urls import path

from . import views

urlpatterns = [
    path("cart/", views.CartDetailView.as_view(), name="cart_detail"),
    path("cart/add/<int:item_id>/", views.AddToCartView.as_view(), name="add_to_cart"),
    path(
        "cart/update/<int:item_id>/",
        views.UpdateCartItemView.as_view(),
        name="update_cart_item",
    ),
    path(
        "cart/remove/<int:item_id>/",
        views.RemoveFromCartView.as_view(),
        name="remove_from_cart",
    ),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path(
        "order/confirmation/<str:order_number>/",
        views.OrderConfirmationView.as_view(),
        name="order_confirmation",
    ),
    # Staff order management
    path("staff/orders/", views.OrderManagementView.as_view(), name="staff_order_list"),
    path(
        "staff/orders/<str:order_number>/advance/",
        views.AdvanceOrderStatusView.as_view(),
        name="advance_order_status",
    ),
    path(
        "staff/orders/<str:order_number>/cancel/",
        views.CancelOrderStatusView.as_view(),
        name="cancel_order_status",
    ),
    path("staff/reports/", views.ReportsView.as_view(), name="staff_reports"),
    path(
        "staff/reports/export/",
        views.ReportsExportView.as_view(),
        name="staff_reports_export",
    ),
]
