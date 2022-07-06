# pylint: disable=C0103,E0401,W0631
import pywt
import numpy
from PIL import Image
# import utils as util


def extract_rgb_coeff(img):
    """
    Returns RGB dwt applied coefficients tuple
    Parameters
    ----------
    img: PIL Image
    Returns
    -------
    (coeffs_r, coeffs_g, coeffs_b):
        RGB coefficients with Discrete Wavelet Transform Applied
    """
    (width, height) = img.size
    img = img.copy()

    mat_r = numpy.empty((width, height))
    mat_g = numpy.empty((width, height))
    mat_b = numpy.empty((width, height))

    for i in range(width):
        for j in range(height):
            (r, g, b) = img.getpixel((i, j))
            mat_r[i, j] = r
            mat_g[i, j] = g
            mat_b[i, j] = b

    coeffs_r = pywt.dwt2(mat_r, 'haar')
   
    coeffs_g = pywt.dwt2(mat_g, 'haar')
    
    coeffs_b = pywt.dwt2(mat_b, 'haar')
    
    return coeffs_r, coeffs_g, coeffs_b


def max_ndarray(mat):
    """
    Returns maximum value within a given 2D Matrix, otherwise 0
    Parameters
    ----------
    mat: numpy.ndarray
        matrix from which we want to compute the max value
    Returns
    -------
    int32:
        matrix maximum value
    """
    return numpy.amax(mat) if type(mat).__name__ == 'ndarray' else 0


def img_from_dwt_coeff(coeff_dwt):
    """
    Returns Image recreated from dwt coefficients
    Parameters
    ----------
    (coeffs_r, coeffs_g, coeffs_b):
        RGB coefficients with Discrete Wavelet Transform Applied
    Returns
    -------
    Image from dwt coefficients
    """
    # Channel Red
    (coeffs_r, coeffs_g, coeffs_b) = coeff_dwt

    # cc = numpy.array((coeffs_r, coeffs_g, coeffs_b))

    (width, height) = (len(coeffs_r[0]), len(coeffs_r[0][0]))

    cARed = numpy.array(coeffs_r[0])
    cHRed = numpy.array(coeffs_r[1][0])
    cVRed = numpy.array(coeffs_r[1][1])
    cDRed = numpy.array(coeffs_r[1][2])
    # Channel Green
    cAGreen = numpy.array(coeffs_g[0])
    cHGreen = numpy.array(coeffs_g[1][0])
    cVGreen = numpy.array(coeffs_g[1][1])
    cDGreen = numpy.array(coeffs_g[1][2])
    # Channel Blue
    cABlue = numpy.array(coeffs_b[0])
    cHBlue = numpy.array(coeffs_b[1][0])
    cVBlue = numpy.array(coeffs_b[1][1])
    cDBlue = numpy.array(coeffs_b[1][2])

    # maxValue per channel par matrix
    cAMaxRed = max_ndarray(cARed)
    cAMaxGreen = max_ndarray(cAGreen)
    cAMaxBlue = max_ndarray(cABlue)

    cHMaxRed = max_ndarray(cHRed)
    cHMaxGreen = max_ndarray(cHGreen)
    cHMaxBlue = max_ndarray(cHBlue)

    cVMaxRed = max_ndarray(cVRed)
    cVMaxGreen = max_ndarray(cVGreen)
    cVMaxBlue = max_ndarray(cVBlue)

    cDMaxRed = max_ndarray(cDRed)
    cDMaxGreen = max_ndarray(cDGreen)
    cDMaxBlue = max_ndarray(cDBlue)

    # Image object init
    dwt_img = Image.new('RGB', (width, height), (0, 0, 20))
    # cA reconstruction

    '''
    The image formed from the low frequency of the images which contains the main content of the image
    '''
    for i in range(width):
        for j in range(height):
            R = cARed[i][j]
            R = (R/cAMaxRed)*100.0
            G = cAGreen[i][j]
            G = (G/cAMaxGreen)*100.0
            B = cABlue[i][j]
            B = (B/cAMaxBlue)*100.0
            new_value = (int(R), int(G), int(B))
            dwt_img.putpixel((i, j), new_value)
   
    return dwt_img
