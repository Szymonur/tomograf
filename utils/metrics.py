import numpy as np

def calculate_rmse(original, reconstructed):
    original = np.array(original)
    reconstructed = np.array(reconstructed)
    
    # Calculate RMSE
    mse = np.mean((original - reconstructed) ** 2)
    rmse = np.sqrt(mse)
    
    return rmse
