from constants import A, w_0, phi, T, N, n_0, P, Q, SNR_db_list, standard_deviation_list, m_values


def W_CRLB(standard_deviation):

    CRLB = (12 * standard_deviation**2) / (A**2 * T**2 * N * (N**2 - 1))
    return CRLB

def Phi_CRLB(standard_deviation):
   
    CRLB = (12 * standard_deviation**2 * (n_0**2 * N + 2 * n_0 * P + Q)) / (A**2 * N**2 * (N**2 - 1))
    return CRLB