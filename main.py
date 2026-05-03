import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cpk 계산 함수
def calculate_cpk(data, usl, lsl):
    mean = np.mean(data)
    std_dev = np.std(data)
    cpk_usl = (usl - mean) / (3 * std_dev)
    cpk_lsl = (mean - lsl) / (3 * std_dev)
    return min(cpk_usl, cpk_lsl)

# IMR 차트 생성 함수
def generate_imr_chart(data, output_path):
    plt.figure(figsize=(10, 6))

    # I 차트
    plt.subplot(2, 1, 1)
    plt.plot(data, marker='o', linestyle='-', color='b')
    plt.title('I Chart')
    plt.axhline(np.mean(data), color='r', linestyle='--')
    plt.ylabel('Individual Values')

    # MR 차트
    moving_range = [abs(data[i] - data[i - 1]) for i in range(1, len(data))]
    plt.subplot(2, 1, 2)
    plt.plot(moving_range, marker='o', linestyle='-', color='g')
    plt.title('MR Chart')
    plt.axhline(np.mean(moving_range), color='r', linestyle='--')
    plt.ylabel('Moving Range')

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    # 테스트 데이터
    test_data = [10, 12, 11, 13, 12, 14, 13, 15, 14]
    usl = 16
    lsl = 8

    # Cpk 계산
    cpk = calculate_cpk(test_data, usl, lsl)
    print(f"Cpk: {cpk}")

    # IMR 차트 생성
    generate_imr_chart(test_data, "imr_chart.png")
    print("IMR 차트가 'imr_chart.png'에 저장되었습니다.")