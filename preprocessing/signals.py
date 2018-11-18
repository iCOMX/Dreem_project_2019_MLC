from typing import List
import numpy as np
from scipy.signal import iirfilter, sosfilt

__all__ = ["BandPass", "extract_bands"]


def extract_bands(signal, bands: List[str] = None):
    """
    Extract the different wave bands from the signal
    Args:
        signal: eeg signal
        bands: bands to get. If None, all available bands are returned.

    Returns:
        List of all bands from the signal
    """
    extractors = {
        'delta': BandPass(freq_min=0, freq_max=4),
        'theta': BandPass(freq_min=4, freq_max=8),
        'alpha': BandPass(freq_min=8, freq_max=13),
        'beta': BandPass(freq_min=13, freq_max=22)
    }
    bands = extractors.keys() if bands is None else bands
    signals = []
    for band in bands:
        signals.append(extractors[band](signal))
    return np.array(signals)


class BandPass:
    """
    Band pass filter
    """

    def __init__(self, freq_min: float, freq_max: float, sampl_freq: float = 50, order: int = 4):
        """
        Args:
            freq_min: min frequency
            freq_max: max frequency
            order: order of the filter
        """
        btype = 'band' if freq_min != 0 else 'low'
        nyquist_freq = 0.5 * sampl_freq
        freqs = [freq_min / nyquist_freq, freq_max / nyquist_freq] if btype == 'band' else freq_max / nyquist_freq
        self.sos = iirfilter(order, freqs, btype=btype, ftype='butter', output='sos')

    def __call__(self, signal):
        return sosfilt(self.sos, signal)