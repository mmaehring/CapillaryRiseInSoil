# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 17:32:37 2021

@author: mmaehring
"""

from iminuit import Minuit #, cost
import iminuit
import numpy as np
from scipy.optimize import curve_fit


def model_fitting_iminuit(cost_function, xdata, ydata, data_yerr, initial):
    # https://iminuit.readthedocs.io/en/stable/
    # https://indico.cern.ch/event/833895/contributions/3577808/attachments/1927550/3191336/iminuit_intro.html
    
    least_squares = iminuit.cost.LeastSquares(data_x, data_y, data_yerr, line)

    m = Minuit(least_squares, *initial)  # starting values for α and β -> unpacking operator
    
    m.migrad()  # finds minimum of least_squares function
    m.hesse()   # accurately computes uncertainties
    
    
    return m




def model_fitting_scipy(model, xdata, ydata, initial):
    """
    Parameters
    ----------
    model : function expression
        The general model given f(x,a,b...) with a, b... the parameters to be fitted.
    xdata : np array[n]
        array of independent data.
    ydata : np array[n]
        array of dependent data.
    initial : np array[length(a, b, ...)] 
        array of the initial guesses for the parameters a, b ...

    Returns
    -------
    fitted_params : array
        Fitted params.
    cov_mat_params : array (n x n) n number of parameters
        covariance matrix for the parameters. 
        
        Errors: 
        perr = np.sqrt(np.diag(pcov))
    """
    
    fitted_params, cov_mat_params = curve_fit(model, xdata, ydata, p0=initial)

    return fitted_params, cov_mat_params



if __name__ == "__main__":
    
    model = lambda x, a, b: a*np.exp(-b*x**2)
    
    initial_values = [0, 1] # a_0 = 0, b_0 = 1
    
    
    
    
    
    def line(x, α, β):
        return α + x * β

    # generate random toy data with random offsets in y
    np.random.seed(1)
    data_x = np.linspace(0, 1, 10)
    data_yerr = 0.1  # could also be an array
    data_y = line(data_x, 1, 2) + data_yerr * np.random.randn(len(data_x))
    initial = [0, 0]
    res = model_fitting_iminuit(line, data_x, data_y, data_yerr, initial)
    
    
    
    
    
    print("Hello World")
    
    