import streamlit as st
import pandas as pd
from datetime import date, timedelta
from pathlib import Path

# =========================================================
# 1. CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Smart Saving - Tính tiền gửi tiết kiệm",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. KHỞI TẠO DỮ LIỆU
# =========================================================

if "lich_su" not in st.session_state:
    st.session_state.lich_su = []

if "ket_qua" not in st.session_state:
    st.session_state.ket_qua = None


# =========================================================
# 3. CSS - CHỈ TRANG TRÍ, KHÔNG DÙNG HTML CARD
# =========================================================

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Tiêu đề */
.main-title {
    font-size: 38px;
    font-weight: 700;
}

.subtitle {
    color: #666666;
    font-size: 16px;
}

/* Làm đẹp metric */
[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 18px;
    border-radius: 15px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}

/* Nút */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}

/* Thanh progress */
.stProgress > div > div > div > div {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 4. HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def tien_vnd(so_tien):
    return f"{so_tien:,.0f} VNĐ"


# =========================================================
# 5. SIDEBAR
# =========================================================

with st.sidebar:

    logo_path = Path("logo.jpg.PNG")

    if logo_path.exists():
        st.image(
            str(logo_path),
            use_container_width=True
        )

    st.markdown("## 💰 SMART SAVING")

    st.caption(
        "Quản lý tiền gửi và mục tiêu tài chính cá nhân"
    )

    st.divider()

    menu = st.radio(
        "📌 MENU",
        [
            "🏠 Dashboard",
            "🧮 Tính tiền gửi",
            "🎯 Mục tiêu tiết kiệm",
            "🛒 Giá trị món đồ",
            "🛡️ Quỹ khẩn cấp",
            "📋 Lịch sử giao dịch"
        ]
    )

    st.divider()

    st.caption(
        "APP TÍNH TIỀN GỬI TIẾT KIỆM"
    )

    st.caption(
        "Tạ Thị Thanh Thùy"
    )


# =========================================================
# 6. TỔNG HỢP DỮ LIỆU
# =========================================================

tong_tien_gui = sum(
    item["tien_gui"]
    for item in st.session_state.lich_su
)

tong_tien_lai = sum(
    item["tien_lai"]
    for item in st.session_state.lich_su
)

tong_tai_san = (
    tong_tien_gui + tong_tien_lai
)


# =========================================================
# 7. DASHBOARD
# =========================================================

if menu == "🏠 Dashboard":

    st.title("🏠 Tình hình tài chính của bạn")

    st.write(
        "Theo dõi tiền gửi, tiền lãi, mục tiêu tiết kiệm "
        "và kế hoạch tài chính cá nhân."
    )

    st.divider()

    # =====================================================
    # 4 THẺ TÀI CHÍNH
    # =====================================================

    st.subheader("📊 Tổng quan tài chính")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            label="💰 Tổng tiền gửi",
            value=tien_vnd(tong_tien_gui),
            help="Tổng số tiền gốc trong các khoản gửi"
        )

    with col2:

        st.metric(
            label="📈 Tổng tiền lãi",
            value=tien_vnd(tong_tien_lai),
            help="Tổng tiền lãi dự kiến"
        )

    with col3:

        st.metric(
            label="💎 Tổng tài sản",
            value=tien_vnd(tong_tai_san),
            help="Tổng tiền gốc cộng tiền lãi"
        )

    with col4:

        if tong_tien_gui > 0:

            ty_le_sinh_loi = (
                tong_tien_lai
                / tong_tien_gui
                * 100
            )

        else:

            ty_le_sinh_loi = 0

        st.metric(
            label="📊 Tỷ lệ sinh lời",
            value=f"{ty_le_sinh_loi:.2f}%",
            help="Tổng lãi chia cho tổng tiền gửi"
        )

    st.write("")

    # =====================================================
    # MỤC TIÊU TÀI CHÍNH
    # =====================================================

    st.subheader("🎯 Mục tiêu tài chính của bạn")

    col1, col2 = st.columns(2)

    with col1:

        muc_tieu = st.number_input(
            "🎯 Bạn muốn có bao nhiêu tiền?",
            min_value=0.0,
            value=100_000_000.0,
            step=5_000_000.0,
            format="%.0f"
        )

    with col2:

        tien_hien_co = st.number_input(
            "💰 Số tiền hiện có",
            min_value=0.0,
            value=float(tong_tai_san),
            step=1_000_000.0,
            format="%.0f"
        )

    if muc_tieu > 0:

        phan_tram = (
            tien_hien_co
            / muc_tieu
            * 100
        )

        phan_tram = min(
            max(phan_tram, 0),
            100
        )

        tien_con_thieu = max(
            muc_tieu - tien_hien_co,
            0
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "🎯 Tiến độ",
                f"{phan_tram:.1f}%"
            )

        with col2:

            st.metric(
                "💰 Đã có",
                tien_vnd(tien_hien_co)
            )

        with col3:

            st.metric(
                "📌 Còn thiếu",
                tien_vnd(tien_con_thieu)
            )

        st.progress(
            int(phan_tram)
        )

        if phan_tram >= 100:

            st.success(
                "🎉 Chúc mừng! Bạn đã đạt mục tiêu tài chính."
            )

        else:

            st.info(
                f"🎯 Bạn đã hoàn thành {phan_tram:.1f}% "
                f"mục tiêu."
            )

    st.divider()

    # =====================================================
    # DỰ BÁO TÀI SẢN
    # =====================================================

    st.subheader(
        "🔮 Dự báo tài sản trong tương lai"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        tiet_kiem_thang = st.number_input(
            "💵 Có thể tiết kiệm mỗi tháng",
            min_value=0.0,
            value=3_000_000.0,
            step=500_000.0,
            format="%.0f"
        )

    with col2:

        lai_suat_du_bao = st.number_input(
            "📈 Lãi suất dự kiến (%/năm)",
            min_value=0.0,
            max_value=100.0,
            value=5.0,
            step=0.1
        )

    with col3:

        so_nam_du_bao = st.number_input(
            "📅 Thời gian dự báo",
            min_value=1,
            max_value=50,
            value=5,
            step=1
        )

    # Tính dự báo

    lai_suat_thang = (
        lai_suat_du_bao
        / 100
        / 12
    )

    tong_so_thang = (
        so_nam_du_bao * 12
    )

    so_du = tien_hien_co

    du_bao = []

    for thang in range(
        1,
        tong_so_thang + 1
    ):

        so_du = (
            so_du
            * (1 + lai_suat_thang)
            + tiet_kiem_thang
        )

        if thang % 12 == 0:

            nam = thang // 12

            du_bao.append({
                "Năm": nam,
                "Tài sản": so_du
            })

    if du_bao:

        df_du_bao = pd.DataFrame(
            du_bao
        )

        st.line_chart(
            df_du_bao.set_index("Năm"),
            height=350
        )

        tai_san_cuoi = (
            df_du_bao.iloc[-1]["Tài sản"]
        )

        st.success(
            f"💰 Sau {so_nam_du_bao} năm, "
            f"tài sản dự kiến khoảng "
            f"**{tien_vnd(tai_san_cuoi)}**."
        )

    st.divider()

    # =====================================================
    # MỤC TIÊU CÓ KHẢ THI KHÔNG
    # =====================================================

    st.subheader(
        "🧠 Mục tiêu của bạn cần bao lâu?"
    )

    if muc_tieu > tien_hien_co:

        tien_con_thieu = (
            muc_tieu - tien_hien_co
        )

        if tiet_kiem_thang > 0:

            so_thang_can = (
                tien_con_thieu
                / tiet_kiem_thang
            )

            nam_can = int(
                so_thang_can // 12
            )

            thang_le = int(
                so_thang_can % 12
            )

            st.info(
                f"📌 Với mức tiết kiệm "
                f"**{tien_vnd(tiet_kiem_thang)}/tháng**, "
                f"bạn cần khoảng "
                f"**{nam_can} năm {thang_le} tháng** "
                f"để đạt mục tiêu."
            )

        else:

            st.warning(
                "⚠️ Hãy nhập số tiền có thể tiết kiệm "
                "mỗi tháng."
            )

    else:

        st.success(
            "🎉 Bạn đã đạt mục tiêu tài chính!"
        )

    st.divider()

    # =====================================================
    # GIAO DỊCH GẦN ĐÂY
    # =====================================================

    st.subheader(
        "📋 Giao dịch gần đây"
    )

    if st.session_state.lich_su:

        danh_sach = []

        for item in reversed(
            st.session_state.lich_su[-5:]
        ):

            danh_sach.append({

                "Ngày": item["ngay"],

                "Số tiền gửi": tien_vnd(
                    item["tien_gui"]
                ),

                "Kỳ hạn": (
                    f'{item["ky_han"]} tháng'
                ),

                "Lãi suất": (
                    f'{item["lai_suat"]:.2f}%/năm'
                ),

                "Tiền lãi": tien_vnd(
                    item["tien_lai"]
                ),

                "Tổng nhận": tien_vnd(
                    item["tong_tien"]
                )
            })

        st.dataframe(
            pd.DataFrame(danh_sach),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "📭 Chưa có giao dịch nào. "
            "Hãy sang mục **🧮 Tính tiền gửi** "
            "để tạo giao dịch đầu tiên."
        )

    st.divider()

    # =====================================================
    # GỢI Ý
    # =====================================================

    st.subheader(
        "💡 Gợi ý cho bạn"
    )

    if tong_tien_gui == 0:

        st.info(
            "💡 Bạn chưa có khoản tiền gửi nào. "
            "Hãy bắt đầu bằng cách sử dụng "
            "máy tính tiền gửi."
        )

    elif tien_con_thieu > 0:

        st.warning(
            f"🎯 Bạn còn thiếu "
            f"**{tien_vnd(tien_con_thieu)}** "
            f"để đạt mục tiêu."
        )

    else:

        st.success(
            "✨ Bạn đã đạt mục tiêu tài chính hiện tại."
        )


# =========================================================
# 8. TÍNH TIỀN GỬI
# =========================================================

elif menu == "🧮 Tính tiền gửi":

    # =====================================================
    # LOGO
    # =====================================================

    logo_path = Path("logo.jpg.PNG")

    if logo_path.exists():

        st.image(
            str(logo_path),
            width=120
        )

    # =====================================================
    # TIÊU ĐỀ GIỮ NGUYÊN
    # =====================================================

    st.title(
        "💰 APP TÍNH TIỀN GỬI TIẾT KIỆM "
        "TẠI NGÂN HÀNG TẠ THỊ THANH THÙY"
    )

    st.write(
        "Tính tiền lãi theo **lãi đơn** hoặc **lãi kép**, "
        "với các hình thức lãnh lãi theo tháng, "
        "theo quý hoặc cuối kỳ."
    )

    st.divider()

    # =====================================================
    # THÔNG TIN TIỀN GỬI
    # =====================================================

    st.subheader(
        "📌 Thông tin tiền gửi"
    )

    col1, col2 = st.columns(2)

    with col1:

        tien_gui = st.number_input(
            "💵 Số tiền gửi (VNĐ)",
            min_value=0.0,
            value=200_000_000.0,
            step=1_000_000.0,
            format="%.0f"
        )

    with col2:

        ky_han_thang = st.number_input(
            "📅 Kỳ hạn (tháng)",
            min_value=1,
            max_value=120,
            value=3,
            step=1
        )

    col3, col4 = st.columns(2)

    with col3:

        lai_suat = st.number_input(
            "📈 Lãi suất (%/năm)",
            min_value=0.0,
            max_value=100.0,
            value=5.0,
            step=0.1
        )

    with col4:

        loai_lai = st.selectbox(
            "🔢 Phương pháp tính lãi",
            [
                "Lãi đơn",
                "Lãi kép"
            ]
        )

    hinh_thuc = st.selectbox(
        "💳 Hình thức lãnh lãi",
        [
            "Lãnh lãi hàng tháng",
            "Lãnh lãi hàng quý",
            "Lãnh lãi cuối kỳ"
        ]
    )

    st.divider()

    # =====================================================
    # NÚT TÍNH
    # =====================================================

    if st.button(
        "🧮 TÍNH LÃI",
        use_container_width=True,
        type="primary"
    ):

        if tien_gui <= 0:

            st.error(
                "⚠️ Vui lòng nhập số tiền gửi lớn hơn 0."
            )

            st.stop()

        lai_suat_nam = (
            lai_suat / 100
        )

        thoi_gian_nam = (
            ky_han_thang / 12
        )

        # =================================================
        # LÃI ĐƠN
        # =================================================

        if loai_lai == "Lãi đơn":

            tong_tien_lai = (
                tien_gui
                * lai_suat_nam
                * thoi_gian_nam
            )

            tong_tien = (
                tien_gui
                + tong_tien_lai
            )

            lai_thang = (
                tien_gui
                * lai_suat_nam
                / 12
            )

            lai_quy = (
                tien_gui
                * lai_suat_nam
                / 4
            )

            bang_chi_tiet = []

            for thang in range(
                1,
                ky_han_thang + 1
            ):

                lai_ky = lai_thang

                bang_chi_tiet.append({

                    "Kỳ":
                        f"Tháng {thang}",

                    "Tiền gốc":
                        tien_gui,

                    "Tiền lãi":
                        lai_ky,

                    "Tổng tiền":
                        tien_gui
                        + lai_thang * thang
                })

        # =================================================
        # LÃI KÉP
        # =================================================

        else:

            lai_suat_thang = (
                lai_suat_nam / 12
            )

            tong_tien = (
                tien_gui
                * (1 + lai_suat_thang)
                ** ky_han_thang
            )

            tong_tien_lai = (
                tong_tien
                - tien_gui
            )

            bang_chi_tiet = []

            so_du = tien_gui

            for thang in range(
                1,
                ky_han_thang + 1
            ):

                lai_ky = (
                    so_du
                    * lai_suat_thang
                )

                so_du += lai_ky

                bang_chi_tiet.append({

                    "Kỳ":
                        f"Tháng {thang}",

                    "Tiền gốc":
                        so_du - lai_ky,

                    "Tiền lãi":
                        lai_ky,

                    "Tổng tiền":
                        so_du
                })

            lai_thang = (
                bang_chi_tiet[0]["Tiền lãi"]
            )

            lai_quy = None

        # =================================================
        # LÃI ĐỊNH KỲ
        # =================================================

        if hinh_thuc == "Lãnh lãi hàng tháng":

            lai_dinh_ky = lai_thang

        elif hinh_thuc == "Lãnh lãi hàng quý":

            if loai_lai == "Lãi đơn":

                lai_dinh_ky = lai_quy

            else:

                lai_dinh_ky = 0

                so_du_quy = tien_gui

                for _ in range(3):

                    lai_ky = (
                        so_du_quy
                        * lai_suat_nam
                        / 12
                    )

                    lai_dinh_ky += lai_ky

                    so_du_quy += lai_ky

        else:

            lai_dinh_ky = tong_tien_lai

        # =================================================
        # LƯU KẾT QUẢ
        # =================================================

        st.session_state.ket_qua = {

            "tien_gui":
                tien_gui,

            "ky_han":
                ky_han_thang,

            "lai_suat":
                lai_suat,

            "loai_lai":
                loai_lai,

            "hinh_thuc":
                hinh_thuc,

            "tien_lai":
                tong_tien_lai,

            "tong_tien":
                tong_tien
        }

        # =================================================
        # LƯU LỊCH SỬ
        # =================================================

        st.session_state.lich_su.append({

            "ngay":
                date.today().strftime(
                    "%d/%m/%Y"
                ),

            "tien_gui":
                tien_gui,

            "ky_han":
                ky_han_thang,

            "lai_suat":
                lai_suat,

            "loai_lai":
                loai_lai,

            "hinh_thuc":
                hinh_thuc,

            "tien_lai":
                tong_tien_lai,

            "tong_tien":
                tong_tien
        })

        # =================================================
        # THÔNG BÁO
        # =================================================

        st.success(
            "✅ Tính toán thành công!"
        )

        # =================================================
        # KẾT QUẢ
        # =================================================

        st.subheader(
            "📊 KẾT QUẢ"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "💵 Tiền lãi định kỳ",
                tien_vnd(lai_dinh_ky)
            )

        with col2:

            st.metric(
                "📈 Tổng tiền lãi",
                tien_vnd(tong_tien_lai)
            )

        with col3:

            st.metric(
                "💰 Tổng gốc + lãi",
                tien_vnd(tong_tien)
            )

        st.divider()

        # =================================================
        # NGÀY ĐÁO HẠN
        # =================================================

        ngay_dao_han = (
            date.today()
            + timedelta(
                days=ky_han_thang * 30
            )
        )

        st.info(
            f"📅 Ngày bắt đầu: "
            f"**{date.today().strftime('%d/%m/%Y')}**\n\n"
            f"🔔 Ngày dự kiến đáo hạn: "
            f"**{ngay_dao_han.strftime('%d/%m/%Y')}**"
        )

        # =================================================
        # THÔNG TIN KHOẢN GỬI
        # =================================================

        st.subheader(
            "📋 Thông tin khoản gửi"
        )

        thong_tin = pd.DataFrame({

            "Thông tin": [

                "Số tiền gửi",

                "Kỳ hạn",

                "Lãi suất",

                "Phương pháp tính",

                "Hình thức lãnh lãi"

            ],

            "Giá trị": [

                tien_vnd(tien_gui),

                f"{ky_han_thang} tháng",

                f"{lai_suat:.2f}%/năm",

                loai_lai,

                hinh_thuc

            ]

        })

        st.table(
            thong_tin
        )

        # =================================================
        # BẢNG CHI TIẾT
        # =================================================

        st.subheader(
            "📑 Chi tiết tiền lãi theo từng tháng"
        )

        df = pd.DataFrame(
            bang_chi_tiet
        )

        df["Tiền gốc"] = df[
            "Tiền gốc"
        ].apply(tien_vnd)

        df["Tiền lãi"] = df[
            "Tiền lãi"
        ].apply(tien_vnd)

        df["Tổng tiền"] = df[
            "Tổng tiền"
        ].apply(tien_vnd)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        # =================================================
        # BIỂU ĐỒ
        # =================================================

        st.subheader(
            "📈 Biểu đồ tăng trưởng"
        )

        df_chart = pd.DataFrame(
            bang_chi_tiet
        )

        df_chart = df_chart[
            ["Kỳ", "Tổng tiền"]
        ]

        df_chart = df_chart.set_index(
            "Kỳ"
        )

        st.line_chart(
            df_chart
        )

        # =================================================
        # CÔNG THỨC
        # =================================================

        with st.expander(
            "📚 Xem công thức tính"
        ):

            if loai_lai == "Lãi đơn":

                st.write(
                    "### Lãi đơn"
                )

                st.latex(
                    r"I = P \times r \times t"
                )

                st.write(
                    "P: tiền gốc"
                )

                st.write(
                    "r: lãi suất năm"
                )

                st.write(
                    "t: thời gian gửi tính theo năm"
                )

            else:

                st.write(
                    "### Lãi kép"
                )

                st.latex(
                    r"A = P(1+r)^n"
                )

                st.write(
                    "P: tiền gốc"
                )

                st.write(
                    "r: lãi suất mỗi kỳ"
                )

                st.write(
                    "n: số kỳ nhập lãi"
                )

        st.info(
            "💡 Lưu ý: Đây là công cụ tính toán mô phỏng. "
            "Lãi suất thực tế của ngân hàng có thể áp dụng "
            "quy định và cách tính khác tùy sản phẩm tiền gửi."
        )


# =========================================================
# 9. MỤC TIÊU TIẾT KIỆM
# =========================================================

elif menu == "🎯 Mục tiêu tiết kiệm":

    st.title(
        "🎯 Mục tiêu tiết kiệm"
    )

    st.write(
        "Lập kế hoạch để đạt được mục tiêu tài chính."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        muc_tieu = st.number_input(
            "🎯 Số tiền mục tiêu",
            min_value=0.0,
            value=100_000_000.0,
            step=5_000_000.0,
            format="%.0f"
        )

    with col2:

        hien_co = st.number_input(
            "💰 Số tiền hiện có",
            min_value=0.0,
            value=float(tong_tai_san),
            step=1_000_000.0,
            format="%.0f"
        )

    tiet_kiem = st.number_input(
        "💵 Có thể tiết kiệm mỗi tháng",
        min_value=0.0,
        value=3_000_000.0,
        step=500_000.0,
        format="%.0f"
    )

    if muc_tieu > 0:

        tien_thieu = max(
            muc_tieu - hien_co,
            0
        )

        tien_do = min(
            hien_co / muc_tieu,
            1
        )

        st.metric(
            "📊 Tiến độ",
            f"{tien_do * 100:.1f}%"
        )

        st.progress(
            int(tien_do * 100)
        )

        st.write(
            f"💰 Còn thiếu: "
            f"**{tien_vnd(tien_thieu)}**"
        )

        if tiet_kiem > 0:

            so_thang = (
                tien_thieu
                / tiet_kiem
            )

            st.success(
                f"⏳ Dự kiến cần "
                f"**{so_thang:.1f} tháng**."
            )


# =========================================================
# 10. GIÁ TRỊ MÓN ĐỒ
# =========================================================

elif menu == "🛒 Giá trị món đồ":

    st.title(
        "🛒 Món đồ này thực sự tốn bao nhiêu?"
    )

    st.write(
        "Biến giá tiền thành số tháng tiết kiệm."
    )

    st.divider()

    gia_mon_do = st.number_input(
        "🛍️ Giá món đồ (VNĐ)",
        min_value=0.0,
        value=25_000_000.0,
        step=500_000.0,
        format="%.0f"
    )

    tiet_kiem_thang = st.number_input(
        "💵 Tiền tiết kiệm mỗi tháng",
        min_value=0.0,
        value=3_000_000.0,
        step=500_000.0,
        format="%.0f"
    )

    if tiet_kiem_thang > 0:

        so_thang = (
            gia_mon_do
            / tiet_kiem_thang
        )

        st.metric(
            "⏳ Thời gian cần tiết kiệm",
            f"{so_thang:.1f} tháng"
        )

        st.info(
            f"💡 Món đồ "
            f"**{tien_vnd(gia_mon_do)}** "
            f"tương đương khoảng "
            f"**{so_thang:.1f} tháng tiết kiệm**."
        )


# =========================================================
# 11. QUỸ KHẨN CẤP
# =========================================================

elif menu == "🛡️ Quỹ khẩn cấp":

    st.title(
        "🛡️ Quỹ khẩn cấp"
    )

    st.write(
        "Ước tính số tháng bạn có thể duy trì "
        "chi phí sinh hoạt nếu không có thu nhập."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        tien_khan_cap = st.number_input(
            "💰 Tiền tiết kiệm hiện có",
            min_value=0.0,
            value=30_000_000.0,
            step=1_000_000.0,
            format="%.0f"
        )

    with col2:

        chi_tieu = st.number_input(
            "💸 Chi phí sinh hoạt/tháng",
            min_value=0.0,
            value=7_000_000.0,
            step=500_000.0,
            format="%.0f"
        )

    if chi_tieu > 0:

        so_thang = (
            tien_khan_cap
            / chi_tieu
        )

        st.metric(
            "🛡️ Quỹ hiện tại",
            f"{so_thang:.1f} tháng"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "3 tháng",
                tien_vnd(
                    chi_tieu * 3
                )
            )

        with col2:

            st.metric(
                "6 tháng",
                tien_vnd(
                    chi_tieu * 6
                )
            )

        with col3:

            st.metric(
                "12 tháng",
                tien_vnd(
                    chi_tieu * 12
                )
            )

        if so_thang < 3:

            st.warning(
                "⚠️ Quỹ hiện tại dưới 3 tháng."
            )

        elif so_thang < 6:

            st.info(
                "💡 Quỹ hiện tại khoảng 3–6 tháng."
            )

        else:

            st.success(
                "✅ Quỹ hiện tại từ 6 tháng trở lên."
            )


# =========================================================
# 12. LỊCH SỬ GIAO DỊCH
# =========================================================

elif menu == "📋 Lịch sử giao dịch":

    st.title(
        "📋 Lịch sử giao dịch"
    )

    st.write(
        "Theo dõi những khoản tiền gửi đã tính."
    )

    st.divider()

    if not st.session_state.lich_su:

        st.info(
            "📭 Chưa có giao dịch nào."
        )

    else:

        danh_sach = []

        for item in st.session_state.lich_su:

            danh_sach.append({

                "Ngày":
                    item["ngay"],

                "Tiền gửi":
                    tien_vnd(
                        item["tien_gui"]
                    ),

                "Kỳ hạn":
                    f'{item["ky_han"]} tháng',

                "Lãi suất":
                    f'{item["lai_suat"]:.2f}%',

                "Phương pháp":
                    item["loai_lai"],

                "Tiền lãi":
                    tien_vnd(
                        item["tien_lai"]
                    ),

                "Tổng nhận":
                    tien_vnd(
                        item["tong_tien"]
                    )
            })

        df_history = pd.DataFrame(
            danh_sach
        )

        st.dataframe(
            df_history,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "💰 Tổng vốn",
                tien_vnd(
                    tong_tien_gui
                )
            )

        with col2:

            st.metric(
                "📈 Tổng lãi",
                tien_vnd(
                    tong_tien_lai
                )
            )

        with col3:

            st.metric(
                "💎 Tổng tài sản",
                tien_vnd(
                    tong_tai_san
                )
            )

        # =================================================
        # TẢI FILE CSV
        # =================================================

        csv = df_history.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            "📥 Tải lịch sử giao dịch",
            data=csv,
            file_name="lich_su_tiet_kiem.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.divider()

        # =================================================
        # XÓA
        # =================================================

        if st.button(
            "🗑️ Xóa toàn bộ lịch sử"
        ):

            st.session_state.lich_su = []

            st.success(
                "Đã xóa toàn bộ lịch sử giao dịch."
            )

            st.rerun()
