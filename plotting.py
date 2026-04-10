import numpy as np
import matplotlib.pyplot as plt
from constants import A, w_0, phi, T, N, n_0, P, Q, SNR_db_list, standard_deviation_list, m_values
import estimation
import CRLB



t = np.arange(n_0, n_0 + N, 1) * T
x_values = estimation.X(t,standard_deviation_list[6]) # Using the highest SNR for visualization

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

standard_deviation = standard_deviation_list[0] # Using the lowest SNR for estimation
m = m_values[0] # Using the smallest m for estimation

w_estimate, phi_estimate = estimation.Sim_estimation(m, standard_deviation)

print(f"Estimated frequency: {w_estimate} rad/s")
print(f"Estimated phase: {phi_estimate} radians")

print(f"True frequency: {w_0} rad/s")
print(f"True phase: {phi} radians")

t = np.arange(n_0, n_0 + N, 1) * T
x_values = estimation.X(t,standard_deviation_list[0]) 

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle('Noisy Complex Exponential Signal', fontsize=14, fontweight='bold', y=1.02)

# Magnitude plot
ax1.plot(t, np.real(x_values), label='Real', color='steelblue', linewidth=1.5)
ax1.plot(t, np.real(recreate_signal(w_estimate, phi_estimate, t)), label='Estimated Real', color='red', linewidth=1.5)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Real Part')
ax1.set_title('Real Part')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Phase plot
ax2.plot(t, np.imag(x_values), label='Imaginary', color='coral', linewidth=1.5)
ax2.plot(t, np.imag(recreate_signal(w_estimate, phi_estimate, t)), label='Estimated Imaginary', color='red', linewidth=1.5)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Imaginary Part')
ax2.set_title('Imaginary Part')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

def mean(values):
    return np.sum(values) / len(values)

def variance(values, mean_value):
    return np.sum((values - mean_value) ** 2) / len(values)

w_CRLB = CRLB.W_CRLB(standard_deviation_list)
phi_CRLB = CRLB.Phi_CRLB(standard_deviation_list)

num_estimations = 1

for m in m_values:

    w_estimates, phi_estimates = [], []
    w0_variance_list = []
    phi_variance_list = []

    for sd in standard_deviation_list:

        for _ in range(num_estimations):

            w_estimate, phi_estimate = estimation.Sim_estimation(m, sd)

            w_estimates.append(w_estimate)
            phi_estimates.append(phi_estimate)
        
        #w_mean = mean(w_estimates)
        w_error = np.array(w_estimates) - w_0
        average_w_error = mean(w_error)
        w_error_variance = variance(w_error, average_w_error)
        print(f"Bias in frequency estimate for m = 2 ^ {int(np.log2(m))} and standard deviation = {sd}: {average_w_error}")

        #phi_mean = mean(phi_estimates)
        phi_error = np.array(phi_estimates) - phi
        average_phi_error = mean(phi_error)
        phi_error_variance = variance(phi_error, average_phi_error)
        print(f"Bias in phase estimate for m = 2 ^ {int(np.log2(m))} and standard deviation = {sd}: {average_phi_error}")

        print(f"Variance in frequency estimate for m = 2 ^ {int(np.log2(m))} and standard deviation = {sd}: {w_error_variance}")
        print(f"Variance in phase estimate for m = 2 ^ {int(np.log2(m))} and standard deviation = {sd}: {phi_error_variance}")

        w0_variance_list.append(w_error_variance)
        phi_variance_list.append(phi_error_variance)

    plt.figure(figsize=(12, 6))
    plt.title(f"Estimator variances vs CRLB for m = 2 ^ {int(np.log2(m))}", fontsize=14, fontweight='bold')
    
    # Frequency
    plt.subplot(1, 2, 1)
    plt.plot(SNR_db_list, w0_variance_list, marker='o', label = "Estimator Variance", color = "blue")
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
