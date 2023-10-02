import math
import matplotlib.pyplot as plt
import numpy as np

def generate_input_signal():
    f_signal = 7.1773 * 10**6
    f_sampling = 150 * 10**6
    num_samples = 1024
    time_values = np.arange(num_samples) / f_sampling
    input_signal = np.sin(2 * np.pi * f_signal * time_values)
    return input_signal

def pipeline_adc(v_in):
    D1 = 0
    D2 = 0
    v_ref = 1
    digital_word = []
    while len(digital_word) < 12:
        if v_in < 1 / 4 * v_ref:
            (D1, D2) = (0, 0)
        elif 1 / 4 * v_ref <= v_in < 1 / 2 * v_ref:
            (D1, D2) = (0, 1)
        elif 1 / 2 * v_ref <= v_in < 3 / 4 * v_ref:
            (D1, D2) = (1, 0)
        else:
            (D1, D2) = (1, 1)
        digital_word.append(str(D1))
        digital_word.append(str(D2))
        v_in = 4* (v_in - D1 * 1 / 2 * v_ref - D2 * 1 / 4 * v_ref)
    return digital_word

def binary_to_decimal(binary_word):
    decimal_number = 0
    for i in range(1, 13):
        decimal_number += int(binary_word[i]) * 1 / 2**i
    if binary_word[0] == "+":
        return decimal_number
    else:
        return -decimal_number

def plot_results(input_signal, digital_words, errors):
    num_samples = len(input_signal)
    sample_indices = np.arange(num_samples)
    
    # 修改第一张图的线条颜色和样式
    plt.plot(sample_indices, input_signal, marker="1", ms=3, linestyle="-", color="red", label="Input Signal")
    
    decimal_numbers = [binary_to_decimal(word) for word in digital_words]
    
    # 修改第一张图的线条颜色和样式
    plt.plot(sample_indices, decimal_numbers, marker="2", ms=3, linestyle="--", color="black", label="Converted Signal")
    
    plt.title("Input Signal vs Converted Signal")
    plt.xlabel("Sample Index")
    plt.ylabel("Voltage (V)")  # 修改纵坐标标签
    plt.legend()
    plt.show()
    
    # 修改第二张图的散点颜色
    plt.scatter(sample_indices, errors, s=3, color="red")
    plt.axhline(y=0.000244140625, color='green', linestyle='-', label='y = +0.000244140625')
    plt.axhline(y=-0.000244140625, color='green', linestyle='-', label='y = -0.000244140625')
    plt.title("Error Plot")
    plt.xlabel("Sample Index")
    plt.ylabel("Error")
    plt.show()
    
input_signal = generate_input_signal()
digital_word_list = []
decimal_number_list = []
error_list = []

for v_in in input_signal:
    if v_in >= 0:
        digital_word = ["+"] + pipeline_adc(v_in)
    else:
        digital_word = ["-"] + pipeline_adc(-v_in)
    digital_word_list.append(digital_word)
    decimal_number = binary_to_decimal(digital_word)
    decimal_number_list.append(decimal_number)

for i in range(len(input_signal)):
    error = decimal_number_list[i] - input_signal[i]
    error_list.append(error)

plot_results(input_signal, digital_word_list, error_list)
