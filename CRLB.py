import constants

A = constants.A
w_0 = constants.w_0
phi = constants.phi
T = constants.T
N = constants.N
n_0 = constants.n_0
P = constants.P
Q = constants.Q

def W_CRLB(standard_deviation):

    CRLB = (12 * standard_deviation**2) / (A**2 * T**2 * N * (N**2 - 1))

    return CRLB

def Phi_CRLB(standard_deviation):

    CRLB = (12 * standard_deviation**2 * (n_0**2 * N + 2 * n_0 * P + Q)) / (A**2 * N * (N**2 - 1))

    return CRLB