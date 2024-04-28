import math
from scipy.special import gammaincc

def runs_test(bits):
    n = len(bits)
    ones_count = bits.count('1')
    e = ones_count / n
    
    if not abs(e - 0.5) < (2 / math.sqrt(n)):
        return 0
    
    Vn = 1
    for i in range(1, n):
        if bits[i] != bits[i - 1]:
            Vn += 1

    P_value = math.erfc(abs(Vn - 2 * n * e * (1 - e)) / (2 * math.sqrt(2 * n) * e * (1 - e)))
    
    return P_value


def longest_run_of_ones_test(bits):
    n = len(bits)
    block_size = 8
    num_blocks = n // block_size
    max_run_lengths = [0] * num_blocks
    Pi = [0.2148, 0.3672, 0.2305, 0.1875]
    for i in range(num_blocks):
        block = bits[i * block_size: (i + 1) * block_size]
        max_run = 0
        current_run = 0

        for bit in block:
            if bit == '1':
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0

        max_run_lengths[i] = max_run

    freq_count = [0, 0, 0, 0]
    for length in max_run_lengths:
        match length:
            case 0 | 1:
                freq_count[0] += 1
            case 2:
                freq_count[1] += 1
            case 3:
                freq_count[2] += 1
            case 4:
                freq_count[3] += 1


    chi_squared = sum([(freq_count[i] - 16 * Pi[i]) ** 2 / 16 * Pi[i] for i in range(4)])
    p_value = gammaincc(3 / 2, chi_squared / 2)

    return p_value

sequence = '1100110000010101011011000100110011100000000100101101010001000111101101000000110101111100110011001101100010110010'

# Тестирование
print("Longest run of ones test p-value for sequence:", longest_run_of_ones_test(sequence))