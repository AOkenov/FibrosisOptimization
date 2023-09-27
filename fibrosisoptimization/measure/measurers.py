import numpy as np


class ActivationTimesMeasurer:
    def __init__(self, reference):
        self.reference = reference

    def evaluate(self, signal):
        return np.argmin(np.diff(signal, axis=1), axis=1) - self.reference


class AmplitudeMeasurer:
    def __init__(self):
        pass

    def evaluate(self, signal):
        return signal.max(axis=1) - signal.min(axis=1)


class Measurer:
    def __init__(self):
        pass

    @staticmethod
    def evaluate(signals, lat_reference, fs):
        '''
        Measure amplitude and LAT of signals

        Args:
            signals (np.ndarray[M, N]): M EGMs with length N
            lat_reference (float): Reference value for measuring LAT -
                                   stimulation time (time units)
            fs (float): Sampling frequency (1 / time units)

        Returns:
            np.ndarray[M]: Amplitudes
            np.ndarray[M]: LATs
        '''
        amplitude = AmplitudeMeasurer().evaluate(signals)
        lat = 1 / fs * ActivationTimesMeasurer(lat_reference).evaluate(signals)
        return amplitude, lat
