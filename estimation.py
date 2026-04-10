import numpy as np
from constants import A, w_0, phi, T, N, n_0, P, Q


def X(t, standard_deviation):

    if type(t) != np.ndarray:
        t = np.array(t)

    real_noise = np.random.normal(0, standard_deviation, t.shape)
    imaginary_noise = np.random.normal(0, standard_deviation, t.shape)

    complex_noise = real_noise + 1j * imaginary_noise

    return A * np.exp(1j * (w_0 * t + phi)) + complex_noise

def Max_FFT(x, M):
    fft_x = np.fft.fft(x, M)
    k = np.argmax(fft_x)
    omega_fft = 2 * np.pi * k / (M * T)
    return omega_fft

def W_estimate(m, M):
    return (2 * np.pi * m) / (M * T)

def F(w_estimate, standard_deviation):

    sum = 0
    for n in range(n_0, n_0 + N, 1):
        sum += X(n*T, standard_deviation) * np.exp(- 1j * w_estimate * n * T)

    F = sum / N

    return F

def Phi_estimate(w_estimate, standard_deviation):

    phi_estimate = np.angle(np.exp(- 1j * w_estimate * n_0 * T) * F(w_estimate, standard_deviation))
    
    return phi_estimate



def Sim_estimation(m, standard_deviation):

    t = np.arange(n_0, n_0 + N, 1) * T
    x_values = X(t, standard_deviation)
    
    max_fft = Max_FFT(x_values, m)

    max_fft = Max_FFT(x_values, m)

    w_est = W_estimate(max_fft, m)
    phi_est = Phi_estimate(w_est, standard_deviation)

    return w_est, phi_est