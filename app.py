import streamlit as st
import pandas as pd
import analyzer
from datetime import datetime, timedelta
import altair as alt
import database as db
import time

# Subprogram


def Page_Dashboard():
    st.title("📊 Dashboard")

    st.sidebar.header("Bộ lọc Dữ liệu")

    today = datetime.now()
    seven_days_ago = today - timedelta(days=7)

    # st.date_input return tuple (start_date, end_date) -> Should be datetime objects
    date_range = st.sidebar.date_input(
        "Chọn khoảng thời gian:",
        value=(seven_days_ago, today),  # Default value: a week
        min_value=datetime(2020, 1, 1),
        max_value=today,
        format="DD/MM/YYYY",
    )
    top = st.sidebar.number_input(
        "Hiển thị số lượng hoạt động tốn thời gian nhất:", min_value=1, max_value=100
    )
    if len(date_range) == 2:
        start_date, end_date = date_range

        start_str = start_date.strftime("%Y-%m-%d 00:00:00")
        end_str = end_date.strftime("%Y-%m-%d 23:59:59")

        st.sidebar.write(f"Đang phân tích từ: **{start_date.strftime('%d/%m/%Y')}**")
        st.sidebar.write(f"Đến: **{end_date.strftime('%d/%m/%Y')}**")

        try:
            analysis_df = analyzer.get_analysis(start_str, end_str)

            if not analysis_df.empty:
                SECONDS_PER_LOG = 5  # = INTERVAL_TIME

                category_counts = analysis_df["category"].value_counts()
                category_time = (category_counts * SECONDS_PER_LOG) / 60
                category_time_df = category_time.reset_index()
                category_time_df.columns = ["Loại", "Số phút"]

                # Top
                title_counts = analysis_df["window_title"].value_counts().head(top)

                # Exchange seconds to minutes
                title_time = (title_counts * SECONDS_PER_LOG) / 60
                title_time_df = title_time.reset_index()
                title_time_df.columns = ["Hoạt động", "Số phút"]

                st.header("Tổng quan Phân bổ Thời gian")

                col1, col2 = st.columns([1, 2])

                with col1:
                    st.subheader("Phân loại chung (Phút)")

                    pie_chart = (
                        alt.Chart(category_time_df)
                        .mark_arc(outerRadius=120)
                        .encode(
                            theta=alt.Theta("Số phút", stack=True),
                            color=alt.Color("Loại"),
                            tooltip=["Loại", "Số phút"],
                        )
                        .properties(title="Phân loại theo Loại")
                    )
                    st.altair_chart(pie_chart, use_container_width=True)

                with col2:
                    st.subheader(f"Top {top} Hoạt động (Phút)")

                    bar_chart = (
                        alt.Chart(title_time_df)
                        .mark_bar()
                        .encode(
                            x=alt.X("Số phút", title="Tổng số phút"),
                            y=alt.Y("Hoạt động", sort="-x"),  # Sort by value down
                            tooltip=["Hoạt động", "Số phút"],
                        )
                        .properties(title=f"Top {top} hoạt động tốn thời gian nhất")
                    )
                    st.altair_chart(bar_chart, use_container_width=True)
            else:
                st.warning(
                    "Do something bro, Không có dữ liệu trong khoảng thời gian này."
                )
                st.image("assets/Can't_find_data.jpg", width=300)

        except Exception as e:
            st.error(f"Đã xảy ra lỗi, hãy gửi lỗi sau đến tui để sửa(Tama): {e}")
            st.exception(e)

    else:
        st.sidebar.error(
            "Vui lòng chọn một khoảng thời gian hợp lệ (Bắt đầu và Kết thúc)."
        )


def Page_Setting():
    st.title("⚙️ Cài đặt Quy tắc Phân loại")

    # --- 1. Form Thêm Quy tắc Mới ---
    st.subheader("Thêm quy tắc mới")

    # Dùng `st.form` để nhóm các input
    with st.form("add_rule_form", clear_on_submit=True):
        new_keyword = st.text_input("Từ khóa (Ví dụ: 'Discord', 'Photoshop', ...)")
        new_category = st.selectbox(
            "Phân loại là:", ("Học tập", "Giải trí", "Khác"), accept_new_options=True
        )
        submitted = st.form_submit_button("Thêm quy tắc")

        if submitted:
            if new_keyword:  # Đảm bảo từ khóa không bị rỗng
                success, message = db.add_rule(new_keyword, new_category)
                if success:
                    st.success(message)
                else:
                    st.error(message)
            else:
                st.warning("Từ khóa không được để trống.")

    st.divider()  # Thêm một đường kẻ ngang

    # --- 2. Danh sách & Xóa Quy tắc ---
    st.subheader("Quản lý quy tắc hiện có")

    all_rules = db.get_rules()

    if not all_rules:
        st.info("Chưa có quy tắc nào. Hãy thêm ở trên!")
    else:
        # Tạo DataFrame để hiển thị cho đẹp
        rules_df = pd.DataFrame(all_rules, columns=["id", "keyword", "category"])
        st.dataframe(rules_df, use_container_width=True, hide_index=True)

        # Form Xóa Quy tắc
        st.markdown("Xóa một quy tắc:")

        # Tạo một danh sách các lựa chọn để xóa
        # (Hiển thị dạng: 'Học tập: Visual Studio Code (ID: 1)')
        rule_options = {
            f"{rule['category']}: {rule['keyword']} (ID: {rule['id']})": rule["id"]
            for rule in all_rules
        }

        rule_to_delete = st.selectbox(
            "Chọn quy tắc để xóa:",
            options=rule_options.keys(),
            index=None,  # Mặc định không chọn gì
            placeholder="Chọn một quy tắc...",
        )

        if st.button("Xóa quy tắc đã chọn", type="primary"):
            if rule_to_delete:
                rule_id = rule_options[rule_to_delete]
                success, message = db.delete_rule(rule_id)
                if success:
                    st.success(message)
                    st.rerun()  # Refresh page to reflect changes
                else:
                    st.error(message)
            else:
                st.warning("Bạn muốn tôi xóa cái gì bro?.")


# ----------------------------------------------------------------------------------------------------#
# Main
st.set_page_config(
    page_title="Insight Agent",
    page_icon="🦆",
    layout="wide",
)
# Center align st.title
st.markdown(
    """  
    <style>  
        h1 { text-align: center; }
    </style>  
""",
    unsafe_allow_html=True,
)

page = st.sidebar.selectbox(
    "Chọn trang",
    [
        "📈Dashboard",
        "⚙️Cài đặt",
    ],
)
if page == "📈Dashboard":
    Page_Dashboard()
elif page == "⚙️Cài đặt":
    Page_Setting()
