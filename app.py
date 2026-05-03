import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
# Use non-interactive backend to avoid GUI/backend issues on servers/macOS
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO

def calculate_cpk(data, usl, lsl):
    mean = np.mean(data)
    std_dev = np.std(data)
    cpk_usl = (usl - mean) / (3 * std_dev)
    cpk_lsl = (mean - lsl) / (3 * std_dev)
    return min(cpk_usl, cpk_lsl)

def generate_imr_chart(data):
    fig, axs = plt.subplots(2, 1, figsize=(10, 6))

    # I Chart
    axs[0].plot(data, marker='o', linestyle='-', color='b')
    axs[0].set_title('I Chart')
    axs[0].axhline(np.mean(data), color='r', linestyle='--')
    axs[0].set_ylabel('Individual Values')

    # MR Chart
    moving_range = [abs(data[i] - data[i - 1]) for i in range(1, len(data))]
    axs[1].plot(moving_range, marker='o', linestyle='-', color='g')
    axs[1].set_title('MR Chart')
    axs[1].axhline(np.mean(moving_range), color='r', linestyle='--')
    axs[1].set_ylabel('Moving Range')

    plt.tight_layout()
    return fig

def generate_histogram_capacity(data, usl, lsl):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(data, bins='auto', color='#4C72B0', edgecolor='white', alpha=0.9)
    ax.set_title('Histogram')
    ax.set_xlabel('Value')
    ax.set_ylabel('Frequency')

    mean = np.mean(data)
    std = np.std(data)

    # USL/LSL lines
    if not np.isnan(usl):
        ax.axvline(usl, color='r', linestyle='--', linewidth=2, label='USL')
    if not np.isnan(lsl):
        ax.axvline(lsl, color='r', linestyle='--', linewidth=2, label='LSL')

    # Mean line
    ax.axvline(mean, color='k', linestyle='-', linewidth=1, label='Mean')

    # Cp line positions (show +/- 3 sigma)
    ax.axvline(mean + 3*std, color='gray', linestyle=':', linewidth=1)
    ax.axvline(mean - 3*std, color='gray', linestyle=':', linewidth=1)

    ax.legend()
    plt.tight_layout()
    return fig

st.title("Cpk 분석 및 IMR 차트 생성")

uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])
if uploaded_file is not None:
    df = pd.ExcelFile(uploaded_file)
    sheet_names = df.sheet_names

    selected_sheet = st.selectbox("분석할 시트를 선택하세요", sheet_names)
    data = df.parse(selected_sheet)

    st.write("업로드된 데이터:")
    st.dataframe(data)

    column = st.selectbox("분석할 열을 선택하세요", data.columns)
    usl = st.number_input("USL (상한값)", value=0.0)
    lsl = st.number_input("LSL (하한값)", value=0.0)

    if st.button("Cpk 계산 및 IMR 차트 생성"):
        measurement_data = data[column].dropna()
        # convert usl/lsl to float or NaN
        usl_val = float(usl) if usl is not None else np.nan
        lsl_val = float(lsl) if lsl is not None else np.nan

        mean = np.mean(measurement_data)
        std = np.std(measurement_data)
        n = len(measurement_data)
        cp = (usl_val - lsl_val) / (6*std) if (not np.isnan(usl_val) and not np.isnan(lsl_val) and std>0) else np.nan
        cpu = (usl_val - mean) / (3*std) if (not np.isnan(usl_val) and std>0) else np.nan
        cpl = (mean - lsl_val) / (3*std) if (not np.isnan(lsl_val) and std>0) else np.nan
        cpk = min(cpu, cpl)

        # Top-level metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("N", f"{n}")
        m2.metric("Mean", f"{mean:.4f}")
        m3.metric("Std Dev", f"{std:.4f}")
        m4.metric("Cpk", f"{cpk:.4f}" if not np.isnan(cpk) else "N/A")

        # Layout: left histogram+capability table, right IMR
        left, right = st.columns([2, 2])

        with left:
            st.subheader("Histogram & Capability")
            hist_fig = generate_histogram_capacity(measurement_data, usl_val, lsl_val)
            st.pyplot(hist_fig)

            # capability table
            cap_df = pd.DataFrame({
                'Statistic': ['N', 'Mean', 'Std Dev', 'Cp', 'Cpu', 'Cpl', 'Cpk', 'USL', 'LSL'],
                'Value': [n, mean, std, cp, cpu, cpl, cpk, usl_val, lsl_val]
            })
            st.table(cap_df.set_index('Statistic'))

            # Download measurement CSV
            csv_bytes = measurement_data.to_csv(index=False).encode('utf-8')
            st.download_button("Download data (CSV)", data=csv_bytes, file_name=f"{selected_sheet}_{column}.csv", mime='text/csv')

        with right:
            st.subheader("I-MR Chart")
            imr_fig = generate_imr_chart(measurement_data)
            st.pyplot(imr_fig)

            # Download images
            buf = BytesIO()
            hist_fig.savefig(buf, format='png')
            buf.seek(0)
            st.download_button("Download histogram (PNG)", data=buf, file_name='histogram.png', mime='image/png')

            buf2 = BytesIO()
            imr_fig.savefig(buf2, format='png')
            buf2.seek(0)
            st.download_button("Download IMR chart (PNG)", data=buf2, file_name='imr_chart.png', mime='image/png')