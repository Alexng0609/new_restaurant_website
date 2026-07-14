"""Generate django.po locale files from translation dictionary."""
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

TRANSLATIONS = {
    "Language": "Ngôn ngữ",
    "Open menu": "Mở menu",
    "Close menu": "Đóng menu",
    "Menu": "Menu",
    "Home": "Trang Chủ",
    "News": "Tin Tức",
    "Cart": "Giỏ Hàng",
    "Orders": "Đơn Hàng",
    "Reports": "Báo Cáo",
    "Order History": "Lịch Sử",
    "Profile": "Hồ Sơ",
    "Log Out": "Đăng Xuất",
    "Log In": "Đăng Nhập",
    "Sign Up": "Đăng Ký",
    "Traditional Vietnamese Cuisine": "Món Ăn Truyền Thống Việt Nam",
    "All rights reserved.": "Bản quyền thuộc về.",
    "Username": "Tên đăng nhập",
    "Email": "Email",
    "Phone number": "Số điện thoại",
    "Password": "Mật khẩu",
    "Password confirmation": "Xác nhận mật khẩu",
    "Phone number is required.": "Vui lòng nhập số điện thoại.",
    "Already have an account?": "Đã có tài khoản?",
    "Forgot your password?": "Quên mật khẩu?",
    "Create an account to track orders and earn reward points.": (
        "Tạo tài khoản để theo dõi đơn hàng và tích điểm thưởng."
    ),
    "Account created successfully. Please log in.": (
        "Tạo tài khoản thành công. Vui lòng đăng nhập."
    ),
    "Manage your account information.": "Quản lý thông tin tài khoản của bạn.",
    "First name": "Họ",
    "Last name": "Tên",
    "Reward points": "Điểm thưởng",
    "Save Changes": "Lưu Thay Đổi",
    "Change Password": "Đổi Mật Khẩu",
    "Profile updated successfully.": "Cập nhật hồ sơ thành công.",
    "View your past orders and their status.": (
        "Xem các đơn hàng trước đây và trạng thái của chúng."
    ),
    "Order": "Đơn",
    "Placed on": "Đặt lúc",
    "Status": "Trạng thái",
    "View Details": "Xem Chi Tiết",
    "You have no orders yet.": "Bạn chưa có đơn hàng nào.",
    "Browse Menu": "Xem Thực Đơn",
    "Back to News": "Quay Lại Tin Tức",
    "Edit": "Sửa",
    "Related News": "Tin Liên Quan",
    "Welcome to Bò Nhúng Giấm Ngày Xưa!": "Chào Mừng Đến Với Bò Nhúng Giấm Ngày Xưa!",
    "Experience traditional Vietnamese flavors with fresh ingredients and culinary passion.": (
        "Trải nghiệm hương vị truyền thống Việt Nam với nguyên liệu tươi ngon và đam mê ẩm thực"
    ),
    "View Menu": "Xem Thực Đơn",
    "Order Now": "Đặt Món Ngay",
    "Sign Up Now": "Đăng Ký Ngay",
    "Latest News & Promotions": "Tin Tức & Khuyến Mãi Mới Nhất",
    "View All News": "Xem Tất Cả Tin Tức",
    "Featured Dishes": "Món Ăn Nổi Bật",
    "View Full Menu": "Xem Toàn Bộ Thực Đơn",
    "Customer Reviews": "Đánh Giá Từ Khách Hàng",
    "See reviews from real customers on Google Maps.": (
        "Xem các đánh giá từ khách hàng thực tế trên Google Maps"
    ),
    "Many reviews on Google": "Nhiều đánh giá trên Google",
    "Diverse menu": "Thực đơn đa dạng",
    "Excellent quality": "Chất lượng tuyệt vời",
    "Attentive service": "Phục vụ tận tình",
    "Convenient location": "Vị trí thuận tiện",
    "View All Reviews": "Xem Tất Cả Đánh Giá",
    "Write a Review": "Viết Đánh Giá",
    "Add Menu Item": "Thêm Món Ăn",
    "All": "Tất Cả",
    "Add to cart": "Thêm vào giỏ",
    "Adding...": "Đang thêm...",
    "No items in this category yet.": "Chưa có món ăn nào trong danh mục này.",
    "Back to Menu": "Quay Lại Thực Đơn",
    "In stock": "Còn Hàng",
    "Out of stock": "Hết Hàng",
    "News & Promotions": "Tin Tức & Khuyến Mãi",
    "Latest updates from the restaurant.": "Cập nhật tin tức mới nhất từ nhà hàng",
    "Add News Post": "Thêm Tin Tức Mới",
    "No news yet": "Chưa có tin tức",
    "Check back later for the latest updates!": "Hãy quay lại sau để xem tin tức mới nhất!",
    "Review your items before checkout.": "Xem lại món ăn trước khi tiến hành đặt hàng",
    "serving": "phần",
    "Update": "Cập Nhật",
    "Remove from cart": "Xóa Khỏi Giỏ",
    "Total": "Tổng Cộng",
    "items in cart": "món trong giỏ hàng",
    "Proceed to Checkout": "Tiến Hành Thanh Toán",
    "Your cart is empty.": "Giỏ hàng của bạn đang trống.",
    "Checkout": "Thanh Toán",
    "Fill in delivery details to complete your order.": (
        "Điền thông tin giao hàng để hoàn tất đơn hàng"
    ),
    "Payment": "Thanh toán",
    "Cash on delivery": "Tiền mặt khi nhận hàng",
    "Confirm Order": "Xác Nhận Đặt Hàng",
    "Back to Cart": "Quay Lại Giỏ Hàng",
    "Your Order": "Đơn Hàng Của Bạn",
    "Order Confirmation": "Xác Nhận Đơn Hàng",
    "Thank You!": "Cảm Ơn Bạn!",
    "Order time": "Thời gian đặt hàng",
    "Recipient": "Người nhận",
    "Phone": "Điện thoại",
    "Fulfillment method": "Hình thức nhận hàng",
    "Delivery address": "Địa chỉ giao hàng",
    "Notes": "Ghi chú",
    "Order Details": "Chi Tiết Đơn Hàng",
    "Create an Account": "Tạo Tài Khoản Ngay",
    "Track orders and earn reward points on future visits!": (
        "Theo dõi đơn hàng và tích điểm thưởng cho những lần đặt sau!"
    ),
    "Order Management": "Quản Lý Đơn Hàng",
    "Cancellation reason": "Lý do hủy",
    "Cancelled at": "Hủy lúc",
    "by": "bởi",
    "Advance to": "Chuyển Sang",
    "Cancel Order": "Hủy Đơn",
    "No orders found.": "Không có đơn hàng nào.",
    "Confirm Cancellation": "Xác Nhận Hủy Đơn",
    "Back": "Quay Lại",
    "Today": "Hôm Nay",
    "This Week": "Tuần Này",
    "This Month": "Tháng Này",
    "This Year": "Năm Nay",
    "Export CSV": "Xuất CSV",
    "Revenue": "Doanh Thu",
    "Total Orders": "Tổng Đơn Hàng",
    "Completed Orders": "Đơn Hoàn Thành",
    "Cancelled Orders": "Đơn Hủy",
    "Average Order Value": "Giá Trị TB / Đơn",
    "Orders by Status": "Đơn Hàng Theo Trạng Thái",
    "Top Selling Items": "Món Bán Chạy Nhất",
    "Quantity": "Số lượng",
    "No data for this time period.": "Chưa có dữ liệu cho khoảng thời gian này.",
    "Sales Details": "Chi Tiết Doanh Thu",
    "Order-by-order breakdown for the selected period.": (
        "Danh sách từng đơn hàng trong khoảng thời gian đã chọn."
    ),
    "Back to Reports": "Quay Lại Báo Cáo",
    "Total Sales": "Tổng Doanh Thu",
    "completed orders": "đơn hoàn thành",
    "cancelled": "đã hủy",
    "total": "tổng cộng",
    "Average order value": "Giá trị đơn trung bình",
    "View Sales Details": "Xem Chi Tiết Doanh Thu",
    "Tap to view all orders": "Nhấn để xem tất cả đơn hàng",
    "No orders for this time period.": "Không có đơn hàng trong khoảng thời gian này.",
    "Manage in Orders": "Quản Lý Trong Đơn Hàng",
    "Customer": "Khách hàng",
    "Items": "Món đã đặt",
    "Get Directions": "Chỉ đường",
    "Restaurant location on Google Maps": "Vị trí nhà hàng trên Google Maps",
    "Item name": "Tên Món",
    "Description": "Mô Tả",
    "Price (₫)": "Giá (₫)",
    "Category": "Danh Mục",
    "Image (optional)": "Hình Ảnh (không bắt buộc)",
    "Add Item": "Thêm Món",
    "Cancel": "Hủy",
    "Title": "Tiêu Đề",
    "Content": "Nội Dung",
    "Video (optional)": "Video (không bắt buộc)",
    "Publish": "Đăng Tin",
    "Enter your email address and we'll send instructions to reset your password.": (
        "Nhập email của bạn, chúng tôi sẽ gửi hướng dẫn đặt lại mật khẩu."
    ),
    "Send reset instructions": "Gửi hướng dẫn đặt lại",
    "Back to login": "Quay lại đăng nhập",
    "Password change": "Đổi mật khẩu",
    "Enter your current password, then your new password twice to confirm.": (
        "Nhập mật khẩu hiện tại, sau đó nhập mật khẩu mới hai lần để xác nhận."
    ),
    "Change my password": "Đổi mật khẩu",
    "Current password": "Mật khẩu hiện tại",
    "New password": "Mật khẩu mới",
    "New password confirmation": "Xác nhận mật khẩu mới",
    "Title (Vietnamese)": "Tiêu đề (Tiếng Việt)",
    "Title (English)": "Tiêu đề (Tiếng Anh)",
    "Content (Vietnamese)": "Nội dung (Tiếng Việt)",
    "Content (English)": "Nội dung (Tiếng Anh)",
    "Item name (Vietnamese)": "Tên món (Tiếng Việt)",
    "Item name (English)": "Tên món (Tiếng Anh)",
    "Description (Vietnamese)": "Mô tả (Tiếng Việt)",
    "Description (English)": "Mô tả (Tiếng Anh)",
    "Enter Vietnamese text first. English fields are optional and used when the site language is EN.": (
        "Nhập nội dung tiếng Việt trước. Trường tiếng Anh là tùy chọn và sẽ hiển thị khi người dùng chọn EN."
    ),
    "Item names stay in Vietnamese. Add an English description for EN mode, or leave blank to auto-translate.": (
        "Tên món luôn hiển thị bằng tiếng Việt. Thêm mô tả tiếng Anh cho chế độ EN, hoặc để trống để tự dịch."
    ),
    "Titles stay in Vietnamese. Add English content for EN mode, or leave blank to auto-translate.": (
        "Tiêu đề luôn hiển thị bằng tiếng Việt. Thêm nội dung tiếng Anh cho chế độ EN, hoặc để trống để tự dịch."
    ),
    "Your browser does not support the video tag.": "Trình duyệt của bạn không hỗ trợ thẻ video.",
    "Video": "Video",
    "Watch Video": "Xem Video",
    "Read More": "Đọc Thêm",
    "Back to Profile": "Quay Lại Hồ Sơ",
    "Email Sent": "Email đã gửi",
    "Check your inbox.": "Kiểm tra hộp thư của bạn.",
    "We've emailed you instructions for resetting your password. You should receive it shortly!": (
        "Chúng tôi đã gửi email hướng dẫn đặt lại mật khẩu. Bạn sẽ nhận được trong giây lát!"
    ),
    "Password reset complete": "Đặt lại mật khẩu thành công",
    "Your new password has been set.": "Mật khẩu mới của bạn đã được thiết lập.",
    "Set new password": "Đặt mật khẩu mới",
    "Set a new password": "Đặt mật khẩu mới",
    "Password Change Successful": "Đổi mật khẩu thành công",
    "Password change successful": "Đổi mật khẩu thành công",
    "Your password was changed.": "Mật khẩu của bạn đã được thay đổi.",
    "Full name": "Họ và tên",
    "Optional notes": "Ghi chú (không bắt buộc)",
    "Please enter a delivery address.": "Vui lòng nhập địa chỉ giao hàng.",
    "Manager confirmation code": "Mã xác nhận quản lý",
    "Required unless you are a senior manager (superuser).": (
        "Chỉ cần nhập nếu bạn không phải quản lý cấp cao (superuser)."
    ),
    "ADMIN_CANCEL_CODE is not configured in settings — contact an administrator.": (
        "Chưa thiết lập ADMIN_CANCEL_CODE trong settings — liên hệ quản trị viên."
    ),
    "Confirmation code is incorrect.": "Mã xác nhận không đúng.",
    "Pending": "Chờ xử lý",
    "Confirmed": "Đã xác nhận",
    "Preparing": "Đang chuẩn bị",
    "Delivered": "Đã giao",
    "Cancelled": "Đã hủy",
    "Pickup": "Tự đến lấy",
    "Delivery": "Giao hàng",
    "Online payment": "Thanh toán online",
    "Invalid quantity.": "Số lượng không hợp lệ.",
    "Failed to add to cart.": "Lỗi khi thêm vào giỏ hàng",
    "Network connection error.": "Lỗi kết nối mạng",
    "Some items are no longer available: %(names)s. Please update your cart.": (
        "Một số món không còn khả dụng: %(names)s. Vui lòng cập nhật giỏ hàng."
    ),
    "Order #%(number)s cannot be advanced further.": (
        "Đơn #%(number)s không thể chuyển trạng thái tiếp."
    ),
    "Order #%(number)s -> %(status)s": "Đơn #%(number)s -> %(status)s",
    "Order #%(number)s cannot be cancelled in its current status.": (
        "Đơn #%(number)s không thể hủy ở trạng thái hiện tại."
    ),
    "Order #%(number)s has been cancelled.": "Đơn #%(number)s đã bị hủy.",
    '"%(name)s" added to cart.': 'Đã thêm "%(name)s" vào giỏ hàng!',
    "Order #%(number)s has been received": "Đơn hàng #%(number)s đã được ghi nhận",
    "Cancel Order #%(number)s": "Hủy Đơn #%(number)s",
    "The hot pot broth is sweet, sour, and light — very enjoyable. The beef is tender and fresh, vegetables are clean. The restaurant is not too crowded, atmosphere is comfortable, staff are enthusiastic. I will come back to support.": (
        "Nước lẩu của quán ngọt ngọt, chua chua, thanh thanh dùng rất vừa miệng, thịt bò mềm và tươi, rau sạch. Quán không quá đông, không khí thoải mái, nhân viên nhiệt tình. Mình sẽ quay lại ủng hộ"
    ),
    "This is the only vinegar hot pot in Can Tho that truly matches my taste. The flavor is balanced, not overly sour. Meat and vegetables are fresh. Always supporting!": (
        "Bò nhúng giấm ở Cần Thơ chỉ có chỗ này đúng gu mình nhất. Vị thanh vừa, hông bị chua giấm. Thịt và rau đều tươi. Mãi ủng hộ"
    ),
    "A wonderful traditional restaurant! Authentic vinegar hot pot flavor, rich seasoning. Catching up with old friends here is absolutely perfect.": (
        "Quán ăn truyền thống tuyệt vời! Bò nhúng giấm đúng vị, gia vị đậm đà. Có thêm mấy chiến hữu xưa để ôn lại chuyện cũ thì quá tuyệt vời."
    ),
}


def po_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def build_po(language: str, plural: str) -> str:
    header = (
        'msgid ""\n'
        'msgstr ""\n'
        f'"Project-Id-Version: restaurant_website\\n"\n'
        f'"Language: {language}\\n"\n'
        '"MIME-Version: 1.0\\n"\n'
        '"Content-Type: text/plain; charset=UTF-8\\n"\n'
        '"Content-Transfer-Encoding: 8bit\\n"\n'
        f'"Plural-Forms: {plural}\\n"\n\n'
    )
    lines = [header]
    for msgid in sorted(TRANSLATIONS, key=str.lower):
        msgstr = TRANSLATIONS[msgid] if language == "vi" else msgid
        lines.append(f'msgid "{po_escape(msgid)}"\n')
        lines.append(f'msgstr "{po_escape(msgstr)}"\n\n')
    return "".join(lines)


def main():
    vi_dir = BASE / "locale" / "vi" / "LC_MESSAGES"
    en_dir = BASE / "locale" / "en" / "LC_MESSAGES"
    vi_dir.mkdir(parents=True, exist_ok=True)
    en_dir.mkdir(parents=True, exist_ok=True)
    vi_dir.joinpath("django.po").write_text(
        build_po("vi", "nplurals=1; plural=0"), encoding="utf-8"
    )
    en_dir.joinpath("django.po").write_text(
        build_po("en", "nplurals=2; plural=(n != 1)"), encoding="utf-8"
    )
    print(f"Generated {len(TRANSLATIONS)} entries")


if __name__ == "__main__":
    main()
