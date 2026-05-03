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
        cpk = calculate_cpk(measurement_data, usl, lsl)
        st.write(f"Cpk: {cpk}")

        fig = generate_imr_chart(measurement_data)
        st.pyplot(fig)