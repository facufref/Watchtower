import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def get_recording(sample_rate=44100, duration=3.5):
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
    sd.wait()  # Wait until recording is finished
    return recording


def write_recording(recording, file_address, sample_rate=44100):
    write(file_address, sample_rate, recording)  # Save as WAV file


def get_cross_correlation_lag(y1, y1_name, y2, y2_name, sr):
    n = len(y1)
    corr = signal.correlate(y2, y1, mode='same') / np.sqrt(signal.correlate(y1, y1, mode='same')[int(n/2)] * signal.correlate(y2, y2, mode='same')[int(n/2)])
    delay_arr = np.linspace(-0.5*n/sr, 0.5*n/sr, n)
    delay = delay_arr[np.argmax(corr)]
    print(f'{ y2_name } is { str(delay) } behind { y1_name }')
    plt.figure()
    plt.plot(delay_arr, corr)
    plt.title('Lag: ' + str(np.round(delay, 3)) + ' s')
    plt.xlabel('Lag')
    plt.ylabel('Correlation coeff')
    plt.show()
    return delay
