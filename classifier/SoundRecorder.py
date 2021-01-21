import sounddevice as sd
from scipy.io.wavfile import write


def get_recording(sample_rate=44100, duration=3.5):
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
    sd.wait()  # Wait until recording is finished
    return recording


def write_recording(recording, file_address, sample_rate=44100):
    write(file_address, sample_rate, recording)  # Save as WAV file

