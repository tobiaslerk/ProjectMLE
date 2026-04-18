import numpy as np
import matplotlib.pyplot as plt
from constants import A, w_0, phi, SNR_db_list
import estimation
import CRLB
from tqdm import tqdm

def PlotSignal(t, x_values):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle('Noisy Complex Exponential Signal', fontsize=14, fontweight='bold', y=1.02)

    # Real plot
    ax1.plot(t, np.real(x_values), label='Real', color='steelblue', linewidth=1.5)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Real Part')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Imaginary plot
    ax2.plot(t, np.imag(x_values), label='Imaginary', color='coral', linewidth=1.5)
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Amplitude')
    ax2.set_title('Imaginary Part')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def PlotEstimationOverlay(t, x_values, w_estimate, phi_estimate):
    plt.figure(figsize=(12, 6))
    plt.title('Noisy Signal with Estimated Signal Overlay', fontsize=14, fontweight='bold')

    # Plot the noisy signal
    plt.plot(t, np.real(x_values), label='Real (Noisy)', color='red', linewidth=1.5)
    plt.plot(t, np.imag(x_values), label='Imaginary (Noisy)', color='blue', linewidth=1.5)

    # Recreate the estimated signal
    estimated_signal = estimation.recreate_signal(w_estimate, phi_estimate, t)

    # Plot the estimated signal
    plt.plot(t, np.real(estimated_signal), label='Real (Estimated)', color='green', linewidth=2)
    plt.plot(t, np.imag(estimated_signal), label='Imaginary (Estimated)', color='yellow', linewidth=2)

    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def recreate_signal(w_estimate, phi_estimate, t):
    return A * np.exp(1j * (w_estimate * t + phi_estimate)) 

def mean(values):
    return np.mean(values)

def variance(values):
    return np.var(values)

def PlotResults(m_values, standard_deviation_list, num_estimations):
    w_CRLB = CRLB.W_CRLB(standard_deviation_list)
    phi_CRLB = CRLB.Phi_CRLB(standard_deviation_list)
    
    for m in m_values:
        print(f"Processing m = {m}...")
        
        errors_w = []
        phi_variance_list = []
        w_variance_list, phi_variance_list  = [], []

        #Creates a progress bar for the outer loop iterating over standard deviations
        for sd in tqdm(standard_deviation_list, leave=False):
            errors_w, errors_phi = [], []
            
            for _ in range(num_estimations):
                w_estimate, phi_estimate, _ = estimation.Sim_estimation(m, sd)
                errors_w.append(w_estimate - w_0)
                errors_phi.append(phi_estimate - phi)
                
            w_variance_list.append(variance(errors_w))
            phi_variance_list.append(variance(errors_phi))

        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        fig.suptitle(f"Estimator Variances vs CRLB for M = 2^{int(np.log2(m))}", fontsize=14, fontweight='bold')

        axes[0].semilogy(SNR_db_list, w_variance_list, marker='o', color='blue', label='Estimator Variance')
        axes[0].semilogy(SNR_db_list, w_CRLB,          marker='o', color='red',  label='CRLB')
        axes[0].set(title='Frequency', xlabel='SNR (dB)', ylabel='Variance')
        axes[0].grid(True)
        axes[0].legend()

        axes[1].semilogy(SNR_db_list, phi_variance_list, marker='o', color='blue', label='Estimator Variance')
        axes[1].semilogy(SNR_db_list, phi_CRLB,          marker='o', color='red',  label='CRLB')
        axes[1].set(title='Phase', xlabel='SNR (dB)', ylabel='Variance')
        axes[1].grid(True)
        axes[1].legend()

        plt.tight_layout()
    plt.show()
