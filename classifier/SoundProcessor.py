import numpy as np
from scipy.fftpack import dct


def get_processed_mfcc(sample_rate, signal, chunk_size_in_seconds):
    filter_banks_list = get_filter_banks_from_file(sample_rate, signal, chunk_size_in_seconds)
    mfcc_list = []
    for filter_banks in filter_banks_list:
        mfcc = apply_mfcc(filter_banks)  # Mel-frequency Cepstral Coefficients (MFCCs)
        mean_normalize(mfcc)  # Mean Normalization
        mfcc_list.append(mfcc)
    return mfcc_list


def get_processed_filter_banks(sample_rate, signal, chunk_size_in_seconds):
    filter_banks_list = get_filter_banks_from_file(sample_rate, signal, chunk_size_in_seconds)
    for filter_banks in filter_banks_list:
        mean_normalize(filter_banks)  # Mean Normalization
    return filter_banks_list


def get_filter_banks_from_file(sample_rate, signal, chunk_size_in_seconds):
    chunk_size = int(chunk_size_in_seconds * sample_rate)
    signals = list(chunks(signal, chunk_size))
    if len(signals[-1]) < chunk_size:  # Remove last element if it is not the same size than the others
        signals.remove(signals[-1])
    filter_banks_list = []
    for signal in signals:
        emphasized_signal = pre_emphasize_signal(signal)  # Pre-Emphasis
        frame_length, frames = frame_signal(emphasized_signal, sample_rate)  # Framing
        frames = apply_hamming_window(frame_length, frames)  # Window
        nfft, pow_frames = apply_stft(frames)  # Fourier-Transform and Power Spectrum
        filter_banks = apply_filter_banks(nfft, pow_frames, sample_rate)  # Filter Banks
        filter_banks_list.append(filter_banks)
    return filter_banks_list


def pre_emphasize_signal(signal, filter_coefficient=0.97):
    emphasized_signal = np.append(signal[0], signal[1:] - filter_coefficient * signal[:-1])
    return emphasized_signal


def frame_signal(emphasized_signal, sample_rate, frame_size=0.025, frame_stride=0.01):
    frame_length, frame_step = frame_size * sample_rate, frame_stride * sample_rate  # Convert from seconds to samples
    signal_length = len(emphasized_signal)
    frame_length = int(round(frame_length))
    frame_step = int(round(frame_step))
    num_frames = int(np.ceil(float(np.abs(signal_length - frame_length)) / frame_step))  # Make sure that we have at least 1 frame
    pad_signal_length = num_frames * frame_step + frame_length
    z = np.zeros((pad_signal_length - signal_length))
    pad_signal = np.append(emphasized_signal, z)  # Pad Signal to make sure that all frames have equal number of samples without truncating any samples from the original signal
    indices = np.tile(np.arange(0, frame_length), (num_frames, 1)) + np.tile(np.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T
    frames = pad_signal[indices.astype(np.int32, copy=False)]
    return frame_length, frames


def apply_hamming_window(frame_length, frames):
    frames *= np.hamming(frame_length)
    # frames *= 0.54 - 0.46 * numpy.cos((2 * numpy.pi * n) / (frame_length - 1))  # Explicit Implementation **
    return frames


def apply_stft(frames, nfft=512):
    mag_frames = np.absolute(np.fft.rfft(frames, nfft))  # Magnitude of the FFT
    pow_frames = ((1.0 / nfft) * ((mag_frames) ** 2))  # Power Spectrum
    return nfft, pow_frames


def apply_filter_banks(nfft, pow_frames, sample_rate, nfilt=40, low_freq_mel=0):
    high_freq_mel = (2595 * np.log10(1 + (sample_rate / 2) / 700))  # Convert Hz to Mel
    mel_points = np.linspace(low_freq_mel, high_freq_mel, nfilt + 2)  # Equally spaced in Mel scale
    hz_points = (700 * (10 ** (mel_points / 2595) - 1))  # Convert Mel to Hz
    bin = np.floor((nfft + 1) * hz_points / sample_rate)
    fbank = np.zeros((nfilt, int(np.floor(nfft / 2 + 1))))
    for m in range(1, nfilt + 1):
        f_m_minus = int(bin[m - 1])  # left
        f_m = int(bin[m])  # center
        f_m_plus = int(bin[m + 1])  # right

        for k in range(f_m_minus, f_m):
            fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
        for k in range(f_m, f_m_plus):
            fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])
    filter_banks = np.dot(pow_frames, fbank.T)
    filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)  # Numerical Stability
    filter_banks = 20 * np.log10(filter_banks)  # dB
    return filter_banks


def apply_mfcc(filter_banks, num_ceps=12):
    mfcc = dct(filter_banks, type=2, axis=1, norm='ortho')[:, 1: (num_ceps + 1)]  # Keep 2-13
    mfcc = apply_sinusoidal_liftering(mfcc)
    return mfcc


def apply_sinusoidal_liftering(mfcc, cep_lifter=22):
    (nframes, ncoeff) = mfcc.shape
    n = np.arange(ncoeff)
    lift = 1 + (cep_lifter / 2) * np.sin(np.pi * n / cep_lifter)
    mfcc *= lift
    return mfcc


def mean_normalize(frames):
    frames -= (np.mean(frames, axis=0) + 1e-8)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]