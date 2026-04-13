import numpy as np

T = 10 ** (-6)
f_0 = 10 ** 3
w_0 = 2 * np.pi * f_0
phi = np.pi / 8
A = 1
N = 513
n_0 = int( - (N - 1) / 2)

P = (N * (N - 1)) / 2
Q = (N * (N - 1) * (2*N - 1)) / 6

SNR_db_list = np.array([-10, 0, 10, 20, 30, 40, 50, 60])
SNR_list = 10 ** (SNR_db_list / 20)
variance_list = A ** 2 / (2 * SNR_list)
standard_deviation_list = np.sqrt(variance_list)

k = np.array([10, 12, 14, 16, 18, 20])
m_values = 2 ** k