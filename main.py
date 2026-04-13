import numpy as np
import matplotlib.pyplot as plt
import estimation
import CRLB
import plotting
from constants import A, w_0, phi, T, N, n_0, SNR_db_list, standard_deviation_list, m_values

t = np.arange(n_0, n_0 + N, 1) * T 

plotting.PlotResults(m_values, standard_deviation_list, num_estimations=10)

