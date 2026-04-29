import numpy as np
import matplotlib.pyplot as plt
from os.path import join
import sys
from time import perf_counter

def load_data(load_dir, bid):
    u = np.zeros((514, 514))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

#@profile
def jacobi(u, interior_mask, max_iter, atol=1e-4):
    u = np.copy(u)
    for i in range(max_iter):
        # The update rule: 0.25 * (Left + Right + Up + Down)
        u_new = 0.25 * (u[1:-1, :-2] + u[1:-1, 2:] + u[:-2, 1:-1] + u[2:, 1:-1])
        u_new_interior = u_new[interior_mask]
        
        # Check for convergence
        delta = np.abs(u[1:-1, 1:-1][interior_mask] - u_new_interior).max()
        u[1:-1, 1:-1][interior_mask] = u_new_interior
        
        if delta < atol:
            break
    return u, i

if __name__ == '__main__':
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()

    if len(sys.argv) < 2:
        N = 1
    else:
        N = int(sys.argv[1])

    subset = building_ids[:N]
    
    total_start = perf_counter()
    
    for bid in subset:
        u0, mask = load_data(LOAD_DIR, bid)
        
        # start = perf_counter()
        u_final, iters = jacobi(u0, mask, 20000)
        # end = perf_counter()
        
        # print(f"Building {bid}: {iters} iterations, Time: {end-start:.4f}s")
        
        # # Save a visualization for the first one as an example
        # if bid == subset[0]:
        #     plt.imshow(u_final, cmap='magma')
        #     plt.colorbar(label='Temp ºC')
        #     plt.title(f"Final Heat Distribution: {bid}")
        #     plt.savefig(f"result_{bid}.png")

    total_end = perf_counter()
    avg_time = (total_end - total_start) / N
    print(f"\nTotal time for {N} buildings: {total_end - total_start:.2f}s")
    print(f"Average time per building: {avg_time:.4f}s")