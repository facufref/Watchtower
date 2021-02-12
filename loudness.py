import pyloudnorm as pyln
from scipy.io import wavfile
import numpy as np


def run():
    f1_name = 'recordings/loud.wav'
    f1_file = wavfile.read(f1_name)
    f1_sample_rate, f1_signal = f1_file
    meter = pyln.Meter(f1_sample_rate) # create BS.1770 meter
    #loudness_f1 = meter.integrated_loudness(f1_signal) # measure loudness
    #print(f"Loudness {f1_name}: {loudness_f1}")
    amp_mean_f1 = np.mean(np.abs(f1_signal))
    print(f"Mean Amplitude of {f1_name}: {amp_mean_f1}")
    amp_max_f1 = np.max(np.abs(f1_signal))
    print(f"Max Amplitude of {f1_name}: {amp_max_f1}")
    dbs_f1 = 20 * np.log10(np.sqrt(np.mean(f1_signal ** 2)))
    print(f"dBs of {f1_name}: {dbs_f1}")
    print()

    f2_name = 'recordings/not_loud.wav'
    f2_file = wavfile.read(f2_name)
    f2_sample_rate, f2_signal = f2_file
    meter = pyln.Meter(f2_sample_rate) # create BS.1770 meter
    #loudness_f2 = meter.integrated_loudness(f2_signal) # measure loudness
    #print(f"Loudness {f2_name}: {loudness_f2}")
    amp_mean_f2 = np.mean(np.abs(f2_signal))
    print(f"Mean Amplitude of {f2_name}: {amp_mean_f2}")
    amp_max_f2 = np.max(np.abs(f2_signal))
    print(f"Max Amplitude of {f2_name}: {amp_max_f2}")
    dbs_f2 = 20 * np.log10(np.sqrt(np.mean(f2_signal ** 2)))
    print(f"dBs of {f2_name}: {dbs_f2}")
    print()

    #print(f"Proportion of Loudness: {f2_name} is the {loudness_f2*100/loudness_f1}% of {f1_name}")
    print(f"Proportion of Mean Amplitude: {f2_name} is the {amp_mean_f2*100/amp_mean_f1}% of {f1_name}")
    print(f"Proportion of Max Amplitude: {f2_name} is the {amp_max_f2*100/amp_max_f1}% of {f1_name}")
    print(f"Proportion of dBs: {f2_name} is the {dbs_f2*100/dbs_f1}% of {f1_name}")


if __name__ == '__main__':
    run()
