from constants import m_values, standard_deviation_list, SNR_db_list, A, T, N, n_0, P, Q, w_0, phi
import estimation
import CRLB
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import plotting
import scipy.optimize as optimize

def task_b(num_estimations=1000):
    m = m_values[0]

    w_CRLB = CRLB.W_CRLB(standard_deviation_list)
    phi_CRLB = CRLB.Phi_CRLB(standard_deviation_list)

    errors_w = []
    phi_variance_list = []
    w_variance_list, phi_variance_list  = [], []

    #Creates a progress bar for the outer loop iterating over standard deviations
    for sd in tqdm(standard_deviation_list, leave=False):
        errors_w, errors_phi = [], []
            
        for _ in range(num_estimations):

            coarse_w_estimate, phi_estimate, x_values = estimation.Sim_estimation(m, sd)

            refined_w_estimate = refine_frequency(x_values, coarse_w_estimate)

            errors_w.append(refined_w_estimate - w_0)
            errors_phi.append(phi_estimate - phi)
                
        w_variance_list.append(plotting.variance(errors_w))
        phi_variance_list.append(plotting.variance(errors_phi))


    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle(f"Nelder–Mead Optimized Estimator vs CRLB (M = {m})", fontsize=14, fontweight='bold')

    axes[0].semilogy(SNR_db_list, w_variance_list, marker='o', color='blue', label='Estimator Variance')
    axes[0].semilogy(SNR_db_list, w_CRLB, marker='o', color='red',  label='CRLB')
    axes[0].set(title='Frequency', xlabel='SNR (dB)', ylabel='Variance')
    axes[0].grid(True)
    axes[0].legend()

    axes[1].semilogy(SNR_db_list, phi_variance_list, marker='o', color='blue', label='Estimator Variance')
    axes[1].semilogy(SNR_db_list, phi_CRLB, marker='o', color='red',  label='CRLB')
    axes[1].set(title='Phase', xlabel='SNR (dB)', ylabel='Variance')
    axes[1].grid(True)
    axes[1].legend()

    plt.tight_layout()
    plt.show()


def DTFT(x, omega):
    n = np.arange(n_0, n_0 + N)
    return np.sum(x * np.exp(-1j * omega * n * T))

def objective_function(omega, x):
    F = DTFT(x, omega)
    return -np.abs(F)**2

def refine_frequency(x, omega_init,):
    result = optimize.minimize(
        objective_function, 
        omega_init, args=(x,), 
        method='Nelder-Mead',
        options={'xatol': 1e-8,
                'fatol': 1e-8, 
                'maxiter': 1000}
        )
    return result.x[0]