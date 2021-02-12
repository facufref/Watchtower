import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np


def get_recording(sample_rate=44100, duration=3.5):
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
    sd.wait()  # Wait until recording is finished
    return recording


def write_recording(recording, file_address, sample_rate=44100):
    write(file_address, sample_rate, recording)  # Save as WAV file


def get_rms(signal):
    return np.sqrt(np.mean(signal ** 2))


def get_dbs(rms_signal):
    return 20 * np.log10(rms_signal)


def get_mean_amplitude(signal):
    return np.mean(np.abs(signal))
