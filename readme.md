# Insight Agent - Trợ lý quan sát hành vi (Student Care)

## Dự án thi vòng 2 ITMC

> **Chủ đề:** Student Care - Nâng cao chất lượng học tập sinh viên
> **Tác giả:** Nguyễn Thành Tâm - N25DCCN147

---

## Ý tưởng & Vấn đề giải quyết

Sinh viên thường dành thời gian nhiều cho việc học, đó là điều tốt, nhưng nghịch lý là gần như chẳng làm được gì. Vấn đề không nằm ở việc thiếu kế hoạch (todolist), mà nằm ở việc \*\*thiếu nhận thức về sự xao nhãng.

**Insight Agent** là một công cụ theo dõi năng suất **thụ động**. Nó giúp sinh viên:

1.  **Tự động ghi lại** toàn bộ quá trình sử dụng máy tính mà không cần nhập liệu thủ công.
2.  **Phân tích khách quan** thời gian dành cho các loại hoạt động.
3.  **Nhận diện "kẻ thù"**: Chỉ mặt đặt tên những ứng dụng/trang web ngốn nhiều thời gian nhất (Facebook, YouTube, Game...).

Một khi có số liệu, sinh viên sẽ tự điều chỉnh hành vi để nâng cao chất lượng học tập.

## Tính năng

**Agent ngầm:** Chạy nhẹ nhàng dưới nền, tự động bắt tiêu đề cửa sổ mỗi 5 giây.
**Dashboard trực quan:** Biểu đồ tròn (Cơ cấu thời gian) và Biểu đồ cột (Top ứng dụng).
**Tùy biến quy tắc:** Người dùng có thể tự "dạy" Agent bằng cách thêm từ khóa phân loại (ví dụ: thêm "Discord" vào nhóm "Giải trí").
**Siêu nhẹ:** Sử dụng SQLite, không cần cài đặt server phức tạp.
**Tốc độ nhanh:** Chạy trực tiếp trên máy người dùng, không cần truyền dữ liệu qua mạng.

## Công nghệ sử dụng

- **Python 3.x**
- **Streamlit:** Xây dựng giao diện.
- **Pandas:** Xử lý và phân tích dữ liệu.
- **SQLite:** Cơ sở dữ liệu tích hợp sẵn.
- **PyGetWindow:** Tương tác với API hệ điều hành để lấy thông tin cửa sổ.

## Hướng dẫn Cài đặt & Chạy

Dự án gồm 2 thành phần chạy song song: **Agent** (thu thập) và **App** (hiển thị).

B1: Cài đặt môi trường
Clone repository hoặc giải nén
cd insight-agent

B2: Cài đặt các thư viện phụ thuộc
( Nếu xuất hiện lỗi error: {externally-managed-environment}, hãy tạo môi trường ảo. Hoặc tốt nhất là bạn cũng nên làm kể cả khi không bị lỗi)

python3 -m venv venv

source venv/bin/activate

( Bạn có thể bắt đầu cài lại )

pip install -r requirements.txt

B3: Chạy Agent

python agent.py

B4: Chạy App

streamlit run app.py

Chúc bạn năng suất và tối ưu thời gian của chính mình!!!

## CẢNH BÁO: INSIGHT AGENT ĐƯỢC TẠO ĐỂ CHẠY TRÊN WINDOW, NẾU BẠN SỬ DỤNG MAC HOẶC LINUX SẼ KHÔNG SỬ DỤNG ĐƯỢC ỨNG DỤNG NÀY HOÀN CHỈNH
