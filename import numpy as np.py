import numpy as np
import matplotlib.pyplot as plt

def comparator(v_in, gain=4.0, total_bits=12, stages=6, bits_per_stage=2):
    word = []  # 用于存储二进制输出的列表

    for i in range(stages):
        # 计算比较器的阈值（中点）
        threshold = gain / 2
        
        # 比较输入电压和阈值
        if v_in >= threshold:
            word.extend([1, 1])  # 大于阈值，输出2位的 '11'
            v_in -= threshold  # 减去阈值
        else:
            word.extend([0, 0])  # 小于阈值，输出2位的 '00'
        
        # 位移输入电压
        v_in *= 2

    # 限制输出为指定总位数（例如，12位）
    if len(word) < total_bits:
        word.extend([0] * (total_bits - len(word)))
    else:
        word = word[:total_bits]

    return word

# 设置参数
total_bits = 12
stages = 6
bits_per_stage = 2
input_frequency = 7.1773e6  # 7.1773 MHz
sampling_rate = 150e6  # 150 MHz
duration = 1.0  # 模拟的时间长度（秒）

# 生成时间点
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# 生成输入正弦波信号
input_signal = np.sin(2 * np.pi * input_frequency * t)

# 初始化ADC输出
adc_output = np.zeros_like(input_signal)

# 模拟ADC流水线
for i in range(len(input_signal)):
    input_voltage = input_signal[i]
    output_word = comparator(input_voltage, total_bits=total_bits, stages=stages, bits_per_stage=bits_per_stage)
    
    # 将二进制输出转换为十进制，用于绘制
    output_decimal = sum(bit * (2**(total_bits - 1 - idx)) for idx, bit in enumerate(output_word))
    adc_output[i] = output_decimal

# 显示ADC输出
plt.figure(figsize=(10, 4))
plt.plot(t, adc_output)
plt.xlabel('时间 (秒)')
plt.ylabel('ADC输出')
plt.title('流水线ADC模拟输出')
plt.grid(True)
plt.show()
