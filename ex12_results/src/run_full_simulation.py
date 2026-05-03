import numpy as np
import math
from numba import cuda
from os.path import join
import sys
from time import perf_counter


@cuda.jit
def jacobi_kernel(u, out, interior_mask):
    i, j = cuda.grid(2)
    if 0 < i < u.shape[0] - 1 and 0 < j < u.shape[1] - 1:
        if interior_mask[i-1, j-1]:
            out[i, j] = 0.25 * (u[i-1, j] + u[i+1, j] + u[i, j-1] + u[i, j+1])
        else:
            out[i, j] = u[i, j]

def jacobi_cuda(u_host, interior_mask_host, max_iter):
    d_u = cuda.to_device(u_host)
    d_out = cuda.to_device(u_host)
    d_mask = cuda.to_device(interior_mask_host)
    
    threads_per_block = (16, 16)
    grid_dims = (math.ceil(u_host.shape[0]/16), math.ceil(u_host.shape[1]/16))
    
    for _ in range(max_iter):
        jacobi_kernel[grid_dims, threads_per_block](d_u, d_out, d_mask)
        d_u, d_out = d_out, d_u
        
    return d_u.copy_to_host()

def summary_stats(u, interior_mask):
    u_interior = u[1:-1, 1:-1][interior_mask]
    return {
        'mean_temp': u_interior.mean(),
        'std_temp': u_interior.std(),
        'pct_above_18': np.sum(u_interior > 18) / u_interior.size * 100,
        'pct_below_15': np.sum(u_interior < 15) / u_interior.size * 100,
    }

if __name__ == '__main__':
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    MAX_ITER = 20_000
    
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()

    # CSV Header
    print('building_id,mean_temp,std_temp,pct_above_18,pct_below_15')

    for bid in building_ids:
        # Load single building
        u0 = np.zeros((514, 514))
        u0[1:-1, 1:-1] = np.load(join(LOAD_DIR, f"{bid}_domain.npy"))
        mask = np.load(join(LOAD_DIR, f"{bid}_interior.npy"))
        
        u_final = jacobi_cuda(u0, mask, MAX_ITER)
        
        stats = summary_stats(u_final, mask)
        
        print(f"{bid},{stats['mean_temp']},{stats['std_temp']},{stats['pct_above_18']},{stats['pct_below_15']}")