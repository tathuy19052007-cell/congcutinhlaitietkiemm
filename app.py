import streamlit as st
import pandas as pd
from datetime import date, timedelta
from pathlib import Path

# =========================================================
# 1. CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Tính lãi tiết kiệm",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. KHỞI TẠO SESSION STATE
# =========================================================

if "lich_su" not in st.session_state:
    st.session_state.lich_su = []

if "ket_qua" not in st.session_state:
    st.session_state.ket_qua = None

# =========================================================
# 3. CSS - GIAO DIỆN
# =========================================================

st.markdown("""
<style>

/* Toàn trang */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* Card Dashboard */
.dashboard-card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.06);
    min-height: 145px;
}

.dashboard-title {
    color: #6b7280;
    font-size: 14px;
    margin-bottom: 8px;
}

.dashboard-value {
    color: #111827;
    font-size: 25px;
    font-weight: 700;
}

.dashboard-small {
    color: #6b7280;
    font-size: 13px;
    margin-top: 8px;
}

/* Goal */
.goal-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.05);
}

/* Box cảnh báo */
.warning-box {
    background: #fff7ed;
    padding: 18px;
    border-radius: 14px;
    border-left: 5px solid #f59e0b;
}

/* Box thông tin */
.info-box {
    background: #eff6ff;
    padding: 18px;
    border-radius: 14px;
    border-left: 5px solid #3b82f6;
}

/* Tiêu đề */
h1 {
    font-weight: 700;
}

h2, h3 {
    font-weight: 650;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 4. HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def tien_vnd(value):
    return f"{value:,.0f} VNĐ"


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

    st.caption("APP TÍNH TIỀN GỬI TIẾT KIỆM")
    st.caption("Tạ Thị Thanh Thùy")


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

tong_tai_san = tong_tien_gui + tong_tien_lai

so_giao_dich = len(
    st.session_state.lich_su
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

    # -----------------------------------------------------
    # 7.1. 4 THẺ TỔNG QUAN
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="dashboard-card">

                <div class="dashboard-title">
                    💰 Tổng tiền gửi
                </div>

                <div class="dashboard-value">
                    {tien_vnd(tong_tien_gui)}
                </div>

                <div class="dashboard-small">
                    Tổng vốn đã gửi
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="dashboard-card">

                <div class="dashboard-title">
                    📈 Tổng tiền lãi
                </div>

                <div class="dashboard-value">
                    {tien_vnd(tong_tien_lai)}
                </div>

                <div class="dashboard-small">
                    Lãi dự kiến
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="dashboard-card">

                <div class="dashboard-title">
                    💎 Tổng tài sản
                </div>

                <div class="dashboard-value">
                    {tien_vnd(tong_tai_san)}
                </div>

                <div class="dashboard-small">
                    Gốc + lãi
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        if tong_tien_gui > 0:

            ty_le_lai = (
                tong_tien_lai
                / tong_tien_gui
                * 100
            )

        else:

            ty_le_lai = 0

        st.markdown(
            f"""
            <div class="dashboard-card">

                <div class="dashboard-title">
                    📊 Tỷ lệ sinh lời
                </div>

                <div class="dashboard-value">
                    {ty_le_lai:.2f}%
                </div>

                <div class="dashboard-small">
                    Lãi / vốn
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # -----------------------------------------------------
    # 7.2. MỤC TIÊU TÀI CHÍNH
    # -----------------------------------------------------

    st.subheader("🎯 Mục tiêu tài chính của bạn")

    col1, col2 = st.columns(2)

    with col1:

        muc_tieu = st.number_input(
            "🎯 Bạn muốn có bao nhiêu tiền?",
            min_value=0.0,
            value=100_000_000.0,
            step=5_000_000.0,
            format="%.0f",
            key="dashboard_goal"
        )

    with col2:

        tien_hien_co = st.number_input(
            "💰 Số tiền hiện có",
            min_value=0.0,
            value=float(tong_tai_san),
            step=1_000_000.0,
            format="%.0f",
            key="dashboard_current"
        )

    if muc_tieu > 0:

        tien_con_thieu = max(
            muc_tieu - tien_hien_co,
            0
        )

        phan_tram = min(
            tien_hien_co / muc_tieu * 100,
            100
        )

        st.markdown(
            f"""
            <div class="goal-card">

            <h3>🎯 Tiến độ mục tiêu</h3>

            <h1>{phan_tram:.1f}%</h1>

            <p>
            Đã có:
            <b>{tien_vnd(tien_hien_co)}</b>
            </p>

            <p>
            Còn thiếu:
            <b>{tien_vnd(tien_con_thieu)}</b>
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(
            int(phan_tram)
        )

        if phan_tram >= 100:

            st.success(
                "🎉 Chúc mừng! Bạn đã đạt mục tiêu tài chính."
            )

    st.divider()

    # -----------------------------------------------------
    # 7.3. DỰ BÁO TÀI SẢN
    # -----------------------------------------------------

    st.subheader("🔮 Dự báo tài sản trong tương lai")

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
            "📅 Số năm dự báo",
            min_value=1,
            max_value=50,
            value=5,
            step=1
        )

    lai_thang = (
        lai_suat_du_bao / 100 / 12
    )

    so_thang = (
        so_nam_du_bao * 12
    )

    so_du = tien_hien_co

    du_bao = []

    for thang in range(
        1,
        so_thang + 1
    ):

        so_du = (
            so_du * (1 + lai_thang)
            + tiet_kiem_thang
        )

        if thang % 12 == 0:

            nam = thang // 12

            du_bao.append({
                "Năm": nam,
                "Tài sản dự kiến": so_du
            })

    if du_bao:

        df_du_bao = pd.DataFrame(
            du_bao
        )

        st.line_chart(
            df_du_bao.set_index("Năm"),
            height=350
        )

        gia_tri_cuoi = (
            df_du_bao.iloc[-1]["Tài sản dự kiến"]
        )

        st.success(
            f"💰 Nếu duy trì kế hoạch hiện tại, "
            f"sau {so_nam_du_bao} năm tài sản "
            f"dự kiến khoảng "
            f"**{tien_vnd(gia_tri_cuoi)}**."
        )

    st.divider()

    # -----------------------------------------------------
    # 7.4. KIỂM TRA MỤC TIÊU
    # -----------------------------------------------------

    st.subheader("🧠 Mục tiêu của bạn cần bao lâu?")

    if muc_tieu > tien_hien_co:

        if tiet_kiem_thang > 0:

            tien_con_thieu = (
                muc_tieu - tien_hien_co
            )

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
                f"📌 Nếu tiết kiệm "
                f"**{tien_vnd(tiet_kiem_thang)}/tháng**, "
                f"bạn cần khoảng "
                f"**{nam_can} năm {thang_le} tháng** "
                f"để đạt mục tiêu."
            )

        else:

            st.warning(
                "Bạn chưa nhập số tiền có thể tiết kiệm mỗi tháng."
            )

    else:

        st.success(
            "🎉 Bạn đã đạt hoặc vượt mục tiêu!"
        )

    st.divider()

    # -----------------------------------------------------
    # 7.5. KHOẢN GỬI GẦN NHẤT
    # -----------------------------------------------------

    st.subheader("📋 Khoản tiền gửi gần đây")

    if st.session_state.lich_su:

        gan_nhat = (
            st.session_state.lich_su[-5:]
        )

        data = []

        for item in reversed(gan_nhat):

            data.append({
                "Ngày": item["ngay"],
                "Tiền gửi": tien_vnd(
                    item["tien_gui"]
                ),
                "Kỳ hạn": f'{item["ky_han"]} tháng',
                "Lãi suất": f'{item["lai_suat"]:.2f}%',
                "Tiền lãi": tien_vnd(
                    item["tien_lai"]
                ),
                "Tổng nhận": tien_vnd(
                    item["tong_tien"]
                )
            })

        st.dataframe(
            pd.DataFrame(data),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "📭 Bạn chưa có giao dịch nào. "
            "Hãy sử dụng phần **🧮 Tính tiền gửi**."
        )

    # -----------------------------------------------------
    # 7.6. GỢI Ý TÀI CHÍNH
    # -----------------------------------------------------

    st.subheader("💡 Gợi ý cho bạn")

    if tong_tien_gui == 0:

        st.info(
            "💡 Hãy bắt đầu bằng cách nhập một khoản tiền gửi "
            "ở phần Tính tiền gửi."
        )

    elif muc_tieu > tong_tai_san:

        st.markdown(
            f"""
            <div class="warning-box">

            🎯 Bạn còn thiếu
            <b>{tien_vnd(muc_tieu - tong_tai_san)}</b>
            để đạt mục tiêu.

            <br><br>

            💡 Hãy duy trì khoản tiết kiệm hàng tháng
            và theo dõi tiến độ trên Dashboard.

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.success(
            "✨ Tài chính của bạn đang đạt mục tiêu đã đặt!"
        )


# =========================================================
# 8. MÁY TÍNH TIỀN GỬI
# =========================================================

elif menu == "🧮 Tính tiền gửi":

    # =====================================================
    # GIỮ NGUYÊN PHẦN HIỆN TẠI TRONG ẢNH
    # =====================================================

    logo_path = Path("logo.jpg.PNG")

    if logo_path.exists():

        st.image(
            str(logo_path),
            width=120
        )

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

    st.subheader("📌 Thông tin tiền gửi")

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

        if lai_suat < 0:

            st.error(
                "⚠️ Lãi suất không được âm."
            )

            st.stop()

        # -------------------------------------------------
        # LÃI SUẤT
        # -------------------------------------------------

        lai_suat_nam = (
            lai_suat / 100
        )

        thoi_gian_nam = (
            ky_han_thang / 12
        )

        # -------------------------------------------------
        # LÃI ĐƠN
        # -------------------------------------------------

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
                    "Kỳ": f"Tháng {thang}",
                    "Tiền gốc": tien_gui,
                    "Tiền lãi": lai_ky,
                    "Tổng tiền": (
                        tien_gui
                        + lai_thang * thang
                    )
                })

        # -------------------------------------------------
        # LÃI KÉP
        # -------------------------------------------------

        else:

            lai_suat_thang = (
                lai_suat_nam / 12
            )

            so_ky = ky_han_thang

            tong_tien = (
                tien_gui
                * (1 + lai_suat_thang)
                ** so_ky
            )

            tong_tien_lai = (
                tong_tien
                - tien_gui
            )

            lai_thang = None

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
                    "Kỳ": f"Tháng {thang}",
                    "Tiền gốc": (
                        so_du - lai_ky
                    ),
                    "Tiền lãi": lai_ky,
                    "Tổng tiền": so_du
                })

            lai_quy = None

        # -------------------------------------------------
        # LÃI ĐỊNH KỲ
        # -------------------------------------------------

        if hinh_thuc == "Lãnh lãi hàng tháng":

            if loai_lai == "Lãi đơn":

                lai_dinh_ky = lai_thang

            else:

                lai_dinh_ky = (
                    bang_chi_tiet[0]["Tiền lãi"]
                )

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

        # -------------------------------------------------
        # LƯU KẾT QUẢ
        # -------------------------------------------------

        st.session_state.ket_qua = {
            "tien_gui": tien_gui,
            "ky_han": ky_han_thang,
            "lai_suat": lai_suat,
            "loai_lai": loai_lai,
            "hinh_thuc": hinh_thuc,
            "lai_dinh_ky": lai_dinh_ky,
            "tien_lai": tong_tien_lai,
            "tong_tien": tong_tien
        }

        # -------------------------------------------------
        # LƯU LỊCH SỬ
        # -------------------------------------------------

        st.session_state.lich_su.append({

            "ngay": date.today().strftime(
                "%d/%m/%Y"
            ),

            "tien_gui": tien_gui,

            "ky_han": ky_han_thang,

            "lai_suat": lai_suat,

            "loai_lai": loai_lai,

            "hinh_thuc": hinh_thuc,

            "tien_lai": tong_tien_lai,

            "tong_tien": tong_tien
        })

        st.success(
            "✅ Tính toán thành công!"
        )

        # =================================================
        # KẾT QUẢ
        # =================================================

        st.subheader("📊 KẾT QUẢ")

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
            f"**{date.today().strftime('%d/%m/%Y')}**  \n"
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

        df_bieu_do = pd.DataFrame(
            bang_chi_tiet
        )

        df_bieu_do = df_bieu_do[
            ["Kỳ", "Tổng tiền"]
        ]

        df_bieu_do = df_bieu_do.set_index(
            "Kỳ"
        )

        st.line_chart(
            df_bieu_do
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
                    "Trong đó: P là tiền gốc, "
                    "r là lãi suất năm, "
                    "t là thời gian gửi tính theo năm."
                )

            else:

                st.write(
                    "### Lãi kép"
                )

                st.latex(
                    r"A = P(1+r)^n"
                )

                st.write(
                    "Trong đó: P là tiền gốc, "
                    "r là lãi suất mỗi kỳ, "
                    "n là số kỳ nhập lãi."
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
        "Tạo kế hoạch để đạt được mục tiêu tài chính."
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
        "💵 Số tiền có thể tiết kiệm mỗi tháng",
        min_value=0.0,
        value=3_000_000.0,
        step=500_000.0,
        format="%.0f"
    )

    if muc_tieu > 0:

        phan_tram = min(
            hien_co / muc_tieu * 100,
            100
        )

        con_thieu = max(
            muc_tieu - hien_co,
            0
        )

        st.metric(
            "📊 Tiến độ",
            f"{phan_tram:.1f}%"
        )

        st.progress(
            int(phan_tram)
        )

        st.write(
            f"💰 Còn thiếu: "
            f"**{tien_vnd(con_thieu)}**"
        )

        if tiet_kiem > 0:

            so_thang = (
                con_thieu
                / tiet_kiem
            )

            st.success(
                f"⏳ Cần khoảng "
                f"**{so_thang:.1f} tháng** "
                f"nếu tiết kiệm đều."
            )


# =========================================================
# 10. GIÁ TRỊ MÓN ĐỒ
# =========================================================

elif menu == "🛒 Giá trị món đồ":

    st.title(
        "🛒 Món đồ này thực sự tốn bao nhiêu?"
    )

    st.write(
        "Tính xem một món đồ tương đương bao nhiêu tháng tiết kiệm."
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
        "💵 Số tiền tiết kiệm mỗi tháng",
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
            f"💡 Món đồ trị giá "
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
        "Xem số tiền hiện tại có thể duy trì cuộc sống "
        "trong bao nhiêu tháng nếu không có thu nhập."
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
            "💸 Chi phí mỗi tháng",
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
                "⚠️ Quỹ hiện tại dưới 3 tháng chi phí."
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
        "Theo dõi những khoản tiền gửi bạn đã tính."
    )

    st.divider()

    if not st.session_state.lich_su:

        st.info(
            "📭 Chưa có giao dịch nào."
        )

    else:

        data = []

        for item in st.session_state.lich_su:

            data.append({

                "Ngày": item["ngay"],

                "Tiền gửi": tien_vnd(
                    item["tien_gui"]
                ),

                "Kỳ hạn": (
                    f'{item["ky_han"]} tháng'
                ),

                "Lãi suất": (
                    f'{item["lai_suat"]:.2f}%'
                ),

                "Phương pháp": item[
                    "loai_lai"
                ],

                "Tiền lãi": tien_vnd(
                    item["tien_lai"]
                ),

                "Tổng nhận": tien_vnd(
                    item["tong_tien"]
                )

            })

        df_history = pd.DataFrame(
            data
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

        # -------------------------------------------------
        # DOWNLOAD CSV
        # -------------------------------------------------

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

        if st.button(
            "🗑️ Xóa toàn bộ lịch sử"
        ):

            st.session_state.lich_su = []

            st.success(
                "Đã xóa toàn bộ lịch sử."
            )

            st.rerun()
