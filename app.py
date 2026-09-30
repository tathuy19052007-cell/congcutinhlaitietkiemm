import streamlit as st
import pandas as pd

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 ỨNG DỤNG TÍNH LÃI TIỀN GỬI TIẾT KIỆM")
st.write(
    "Tính tiền lãi theo **lãi đơn** hoặc **lãi kép**, "
    "với các hình thức lãnh lãi theo tháng, theo quý hoặc cuối kỳ."
)

st.divider()

# =========================
# NHẬP DỮ LIỆU
# =========================
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

# =========================
# NÚT TÍNH
# =========================
if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if tien_gui <= 0:
        st.error("⚠️ Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("⚠️ Lãi suất không được âm.")
        st.stop()

    # Lãi suất năm dạng thập phân
    lai_suat_nam = lai_suat / 100

    # Thời gian gửi tính theo năm
    thoi_gian_nam = ky_han_thang / 12

    # =========================
    # TÍNH LÃI ĐƠN
    # =========================
    if loai_lai == "Lãi đơn":

        tong_tien_lai = tien_gui * lai_suat_nam * thoi_gian_nam

        tong_tien = tien_gui + tong_tien_lai

        # Lãi mỗi tháng
        lai_thang = tien_gui * lai_suat_nam / 12

        # Lãi mỗi quý
        lai_quy = tien_gui * lai_suat_nam / 4

        # =========================
        # TẠO BẢNG CHI TIẾT
        # =========================
        bang_chi_tiet = []

        for thang in range(1, ky_han_thang + 1):

            lai_ky = lai_thang

            bang_chi_tiet.append({
                "Kỳ": f"Tháng {thang}",
                "Tiền gốc": tien_gui,
                "Tiền lãi": lai_ky,
                "Tổng tiền": tien_gui + lai_thang * thang
            })

    # =========================
    # TÍNH LÃI KÉP
    # =========================
    else:

        # Lãi suất theo tháng
        lai_suat_thang = lai_suat_nam / 12

        # Số kỳ nhập lãi
        so_ky = ky_han_thang

        # Công thức lãi kép
        tong_tien = tien_gui * (1 + lai_suat_thang) ** so_ky

        tong_tien_lai = tong_tien - tien_gui

        lai_thang = None

        # =========================
        # TẠO BẢNG CHI TIẾT
        # =========================
        bang_chi_tiet = []

        so_du = tien_gui

        for thang in range(1, ky_han_thang + 1):

            lai_ky = so_du * lai_suat_thang
            so_du = so_du + lai_ky

            bang_chi_tiet.append({
                "Kỳ": f"Tháng {thang}",
                "Tiền gốc": so_du - lai_ky,
                "Tiền lãi": lai_ky,
                "Tổng tiền": so_du
            })

        # Lãi theo quý
        lai_quy = None

    # =========================
    # TÍNH LÃI ĐỊNH KỲ
    # =========================
    if hinh_thuc == "Lãnh lãi hàng tháng":

        if loai_lai == "Lãi đơn":
            lai_dinh_ky = lai_thang
        else:
            # Với lãi kép, mỗi tháng tiền lãi thay đổi
            lai_dinh_ky = bang_chi_tiet[0]["Tiền lãi"]

        don_vi = "tháng"

    elif hinh_thuc == "Lãnh lãi hàng quý":

        if loai_lai == "Lãi đơn":
            lai_dinh_ky = lai_quy
        else:
            # Tính tiền lãi của quý đầu tiên
            so_du_quy = tien_gui
            lai_dinh_ky = 0

            for _ in range(3):
                lai_ky = so_du_quy * lai_suat_nam / 12
                lai_dinh_ky += lai_ky
                so_du_quy += lai_ky

        don_vi = "quý"

    else:

        lai_dinh_ky = tong_tien_lai
        don_vi = "cuối kỳ"

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.success("✅ Tính toán thành công!")

    st.subheader("📊 KẾT QUẢ")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            f"{lai_dinh_ky:,.0f} VNĐ"
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            f"{tong_tien_lai:,.0f} VNĐ"
        )

    with col3:
        st.metric(
            "💰 Tổng gốc + lãi",
            f"{tong_tien:,.0f} VNĐ"
        )

    st.divider()

    # =========================
    # THÔNG TIN TÓM TẮT
    # =========================
    st.subheader("📋 Thông tin khoản gửi")

    thong_tin = pd.DataFrame({
        "Thông tin": [
            "Số tiền gửi",
            "Kỳ hạn",
            "Lãi suất",
            "Phương pháp tính",
            "Hình thức lãnh lãi"
        ],
        "Giá trị": [
            f"{tien_gui:,.0f} VNĐ",
            f"{ky_han_thang} tháng",
            f"{lai_suat:.2f}%/năm",
            loai_lai,
            hinh_thuc
        ]
    })

    st.table(thong_tin)

    # =========================
    # BẢNG CHI TIẾT
    # =========================
    st.subheader("📑 Chi tiết tiền lãi theo từng tháng")

    df = pd.DataFrame(bang_chi_tiet)

    df["Tiền gốc"] = df["Tiền gốc"].apply(
        lambda x: f"{x:,.0f} VNĐ"
    )

    df["Tiền lãi"] = df["Tiền lãi"].apply(
        lambda x: f"{x:,.0f} VNĐ"
    )

    df["Tổng tiền"] = df["Tổng tiền"].apply(
        lambda x: f"{x:,.0f} VNĐ"
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # =========================
    # CÔNG THỨC
    # =========================
    with st.expander("📚 Xem công thức tính"):

        if loai_lai == "Lãi đơn":

            st.write("### Lãi đơn")

            st.latex(
                r"I = P \times r \times t"
            )

            st.write(
                "Trong đó: P là tiền gốc, r là lãi suất năm, "
                "t là thời gian gửi tính theo năm."
            )

        else:

            st.write("### Lãi kép")

            st.latex(
                r"A = P(1+r)^n"
            )

            st.write(
                "Trong đó: P là tiền gốc, r là lãi suất mỗi kỳ, "
                "n là số kỳ nhập lãi."
            )

    # =========================
    # GHI CHÚ
    # =========================
    st.info(
        "💡 Lưu ý: Đây là công cụ tính toán mô phỏng. "
        "Lãi suất thực tế của ngân hàng có thể áp dụng quy định "
        "và cách tính khác tùy sản phẩm tiền gửi."
    )
