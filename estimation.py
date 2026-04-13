import numpy as np
from constants import A, w_0, phi, T, N, n_0, P, Q


def X(t, standard_deviation):

    if type(t) != np.ndarray:
        t = np.array(t)

    real_noise = np.random.normal(0, standard_deviation, t.shape)
    imaginary_noise = np.random.normal(0, standard_deviation, t.shape)

    complex_noise = real_noise + 1j * imaginary_noise

    return A * np.exp(1j * (w_0 * t + phi)) + complex_noise


def Sim_estimation(m, standard_deviation):

    t = np.arange(n_0, n_0 + N) * T
    x_values = X(t, standard_deviation)

    w_hat = W_hat_FFT(x_values, m)
    
    phi_hat = Phi_hat_FFT(x_values, w_hat)

    return w_hat, phi_hat

def FindMaxFFTIndex(x, M):
    fft_x = np.fft.fft(x, M)
    k = np.argmax(np.abs(fft_x))
    return k

def W_hat_FFT(x, M):
    k = FindMaxFFTIndex(x, M)
    omega_fft = 2 * np.pi * k / (M * T)
    return omega_fft

def Phi_hat_FFT(x, w_hat):

    N = len(x)
    n = np.arange(n_0, n_0 + N)

    exp_terms = np.exp(-1j * w_hat * n * T)
    phi_hat = np.angle(np.mean(x * exp_terms))

    return phi_hat
