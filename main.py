import numpy as np
import matplotlib.pyplot as plt
import estimation
import CRLB
import plotting
from constants import A, w_0, phi, T, N, n_0, SNR_db_list, standard_deviation_list, m_values
import Nelder_Mead_optimization

t = np.arange(n_0, n_0 + N) * T 
x_values = estimation.X(t, standard_deviation_list[3])  # Using a specific standard deviation for plotting

#w_estimate, phi_estimate, _ = estimation.Sim_estimation(m_values[5], standard_deviation_list[0])

#plotting.PlotEstimationOverlay(t, x_values, w_estimate, phi_estimate)

#plotting.PlotResults(m_values, standard_deviation_list, num_estimations=1000)

Nelder_Mead_optimization.task_b(num_estimations=1000)