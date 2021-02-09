
from scipy.io import wavfile
from classifier.SoundDataManager import stereo_to_mono

from classifier.SoundRecorder import get_cross_correlation_lag


def run():
    pc_file = wavfile.read('recordings/comodoro_pc.wav')
    pc_sample_rate, pc_signal = pc_file

    pi_file = wavfile.read('recordings/comodoro_pi.wav')
    pi_sample_rate, pi_signal = pi_file

    lag = get_cross_correlation_lag(stereo_to_mono(pc_signal), 'Comodoro PC', stereo_to_mono(pi_signal), 'Comodoro Pi', pc_sample_rate)
    print(-1.485633)

if __name__ == '__main__':
    run()
