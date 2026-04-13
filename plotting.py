import numpy as np
import matplotlib.pyplot as plt
from constants import A, w_0, phi, SNR_db_list
import estimation
import CRLB
from tqdm import tqdm

def PlotSignal(t, x_values):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle('Noisy Complex Exponential Signal', fontsize=14, fontweight='bold', y=1.02)

    # Magnitude plot
    ax1.plot(t, np.abs(x_values), label='Magnitude', color='steelblue', linewidth=1.5)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Magnitude')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Phase plot
    ax2.plot(t, np.angle(x_values), label='Phase', color='coral', linewidth=1.5)
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Phase (radians)')
    ax2.set_title('Phase')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def recreate_signal(w_estimate, phi_estimate, t):
    return A * np.exp(1j * (w_estimate * t + phi_estimate)) 

def SingelEstimation(m, standard_deviation):
    w_estimate, phi_estimate = estimation.Sim_estimation(m, standard_deviation)

    print(f"Estimated frequency: {w_estimate} rad/s")
    print(f"Estimated phase: {phi_estimate} radians")

    print(f"True frequency: {w_0} rad/s")
    print(f"True phase: {phi} radians")

def mean(values):
    return np.mean(values)

def variance(values):
    return np.var(values)

def PlotResults(m_values, standard_deviation_list, num_estimations):
    w_CRLB = CRLB.W_CRLB(standard_deviation_list)
    phi_CRLB = CRLB.Phi_CRLB(standard_deviation_list)
    
    for m in m_values:
        print(f"Processing m = {m}...")
        w_estimates, phi_estimates = [], []
        errors_w = []
        phi_variance_list = []
        w_variance_list, phi_variance_list  = [], []

        for sd in tqdm(standard_deviation_list, leave=False):
            errors_w, errors_phi = [], []
            
            for _ in range(num_estimations):
                w_estimate, phi_estimate = estimation.Sim_estimation(m, sd)
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
    plt.show()   # inside the loop
    
    """     print(f"m = {m} - Frequency Variance: {w_variance_list}")
        #plt.figure(figsize=(12, 6))
        plt.figure(m, figsize=(12, 6))
        plt.title(f"Estimator variances vs CRLB for m = 2 ^ {int(np.log2(m))}", fontsize=14, fontweight='bold')

        # Frequency
        plt.subplot(1, 2, 1)
        plt.plot(SNR_db_list, w_variance_list, marker='o', label = "Estimator Variance", color = "blue")
        plt.plot(SNR_db_list, w_CRLB, marker='o', label = "CRLB", color = "red")
        plt.xlabel('SNR (dB)')
        plt.ylabel('Variance')
        plt.grid(True)
        plt.legend()

        # Phase
        plt.subplot(1, 2, 2)
        plt.plot(SNR_db_list, phi_variance_list, marker='o', label = "Estimator Variance", color = "blue")
        plt.plot(SNR_db_list, phi_CRLB, marker='o', label = "CRLB", color = "red")
        plt.xlabel('SNR (dB)')
        plt.ylabel('Variance')
        plt.grid(True)
        plt.legend()
    plt.show() """




