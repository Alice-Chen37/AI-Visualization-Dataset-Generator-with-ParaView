import numpy as np

def generate_3d_field(temp, wind):
    nx, ny, nz = 60, 60, 60

    x = np.linspace(-5, 5, nx)
    y = np.linspace(-5, 5, ny)
    z = np.linspace(0, 10, nz)

    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

    gaussian = np.exp(-(X**2 + Y**2 + Z**2/10))
    wave = 0.2 * np.sin(wind * X) * np.cos(wind * Y)

    field = gaussian * (temp / 20.0) + wave
    return field