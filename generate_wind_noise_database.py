import numpy as np
from sc_wind_noise_generator import WindNoiseGenerator
import os
from multiprocessing import Pool

# Parameters
NUM_SAMPLES = 500 
DURATION = 10 # Duration in seconds
FS = 48000 # Sample rate in Hz
OUT_DIR = 'wind_noise_samples' # Output directory

GUSTINESS_range = list(range(1, 11)) # Number of speed points. One yields constant wind. High values yield gusty wind (more than 10 can sound unnatural).
open_seed = 1 # Seed for random sequence regeneration

def generate_wind_noise(i):
    # Generate wind noise 
    wn = WindNoiseGenerator(fs=FS, 
                            duration=DURATION,
                            generate=True,
                            wind_profile=None,
                            gustiness=np.random.choice(GUSTINESS_range),
                            short_term_var=True,
                            start_seed=open_seed+i)

    wn_signal, wind_profile = wn.generate_wind_noise()

    # Save wind noise audio 
    filename = os.path.join(OUT_DIR, f'wind_noise_{i}.wav')
    wn.save_signal(wn_signal, filename=filename, num_ch=1, fs=FS)

    print(f'Generated and saved {filename}')



if __name__ == '__main__':
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR) 

    with Pool(16) as p:
        p.map(generate_wind_noise, range(NUM_SAMPLES))

print('Done!')