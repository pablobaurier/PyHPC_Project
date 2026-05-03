from os.path import join
import sys

import numpy as np
from numba import cuda
import math
from time import perf_counter


def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

@cuda.jit
def jacobi_kernel(u, out, interior_mask):
    i, j = cuda.grid(2)
    
    # Ensure we are within the 514x514 grid 
    if 0 < i < u.shape[0] - 1 and 0 < j < u.shape[1] - 1:
        
        # Check the interior mask.
        if interior_mask[i-1, j-1]:
            out[i, j] = 0.25 * (u[i-1, j] + u[i+1, j] + u[i, j-1] + u[i, j+1])
        else:
            # If it's a wall or exterior, keep the original value
            out[i, j] = u[i, j]

def jacobi_cuda(u_host, interior_mask_host, max_iter):
    # Move data to the GPU 
    d_u = cuda.to_device(u_host)
    d_out = cuda.to_device(u_host) # Initialize out with same boundaries
    d_mask = cuda.to_device(interior_mask_host)
    
    # Define block and grid dimensions
    threads_per_block = (16, 16)
    blocks_per_grid_x = math.ceil(u_host.shape[0] / threads_per_block[0])
    blocks_per_grid_y = math.ceil(u_host.shape[1] / threads_per_block[1])
    grid_dims = (blocks_per_grid_x, blocks_per_grid_y)
    
    for i in range(max_iter):
        # Run the kernel
        jacobi_kernel[grid_dims, threads_per_block](d_u, d_out, d_mask)
        
        # Swap the pointers so what  was 'new' becomes 'old' for the next step
        d_u, d_out = d_out, d_u
        
    # Copy the final result back to the CPU 
    return d_u.copy_to_host()


    


def summary_stats(u, interior_mask):
    u_interior = u[1:-1, 1:-1][interior_mask]
    mean_temp = u_interior.mean()
    std_temp = u_interior.std()
    pct_above_18 = np.sum(u_interior > 18) / u_interior.size * 100
    pct_below_15 = np.sum(u_interior < 15) / u_interior.size * 100
    return {
        'mean_temp': mean_temp,
        'std_temp': std_temp,
        'pct_above_18': pct_above_18,
        'pct_below_15': pct_below_15,
    }


if __name__ == '__main__':
    # Load data
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()

    if len(sys.argv) < 2:
        N = 1
    else:
        N = int(sys.argv[1])
    building_ids = building_ids[:N]

    # Load floor plans
    all_u0 = np.empty((N, 514, 514))
    all_interior_mask = np.empty((N, 512, 512), dtype='bool')
    for i, bid in enumerate(building_ids):
        u0, interior_mask = load_data(LOAD_DIR, bid)
        all_u0[i] = u0
        all_interior_mask[i] = interior_mask

    # Run jacobi iterations for each floor plan
    MAX_ITER = 20_000
    all_u = np.empty_like(all_u0)
    
    total_start = perf_counter()
    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        u = jacobi_cuda(u0, interior_mask, MAX_ITER)
        all_u[i] = u
    
    total_end = perf_counter()
    
    avg_time = (total_end - total_start) / N
    print(f"\nTotal time for {N} buildings: {total_end - total_start:.2f}s")
    print(f"Average time per building: {avg_time:.4f}s")

    # Print summary statistics in CSV format
    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    print('building_id, ' + ', '.join(stat_keys))  # CSV header
    for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
        stats = summary_stats(u, interior_mask)
        print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))


        