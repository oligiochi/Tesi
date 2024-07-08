import numpy as np

def calculate_1_3_octave_levels(frequencies, magnitudes, ref_pressure=20e-6):
    """
    Calculate the Sound Pressure Level (SPL) for each 1/3 octave band.

    Parameters:
    frequencies (array-like): Array of frequency values in Hz.
    magnitudes (array-like): Array of magnitude values corresponding to the frequencies.
    ref_pressure (float): Reference sound pressure in Pascals. Default is 20 µPa (20e-6).

    Returns:
    tuple: A tuple containing:
        - center_frequencies (list of float): Center frequencies for each 1/3 octave band.
        - spl_values (list of float): Calculated SPL values for each 1/3 octave band.
    """
    # Define the center frequencies for 1/3 octave bands
    center_frequencies = [
        12.5, 16, 20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000,
        1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000
    ]

    # Calculate the lower and upper limits for each 1/3 octave band
    lower_limits = [f / (2 ** (1 / 6)) for f in center_frequencies]
    upper_limits = [f * (2 ** (1 / 6)) for f in center_frequencies]

    # Initialize an array to store the SPL values for each band
    spl_values = []

    # Compute the sound pressure level for each 1/3 octave band
    for lower, upper in zip(lower_limits, upper_limits):
        # Find indices corresponding to the current 1/3 octave band
        band_indices = (frequencies >= lower) & (frequencies < upper)

        # Calculate the RMS pressure in the band
        band_rms_pressure = np.sqrt(np.sum(magnitudes[band_indices] ** 2))

        # Convert to sound pressure level (SPL)
        if band_rms_pressure > 0:
            band_spl = 20 * np.log10(band_rms_pressure / ref_pressure)
        else:
            band_spl = -np.inf  # If no energy in this band, set SPL to negative infinity

        spl_values.append(band_spl)

    return center_frequencies, spl_values

def calculate_N_fs(duration=None, sampling_frequency=None, number_of_samples=None):
    """
    Calculate missing parameters (duration, sampling_frequency, number_of_samples) 
    based on the provided ones.

    At least two out of the three parameters must be provided. If only one is provided,
    the other two will be calculated accordingly.

    Parameters:
    - duration (float or None): Duration of the signal in seconds.
    - sampling_frequency (float or None): Sampling frequency of the signal in Hz.
    - number_of_samples (int or None): Number of samples in the signal.

    Returns:
    tuple: A tuple containing:
        - number_of_samples (int): Calculated or provided number of samples.
        - sampling_frequency (float): Calculated or provided sampling frequency.
    Raises:
    - ValueError: If less than two out of the three parameters are provided.

    Example:
    >>> calculate_N_fs(duration=10, sampling_frequency=None, number_of_samples=1000)
    (1000, 100.0)
    """
    # Check which parameters are provided
    provided_params = {"d": duration is not None, "f": sampling_frequency is not None, "n": number_of_samples is not None}
    
    # Ensure at least two parameters are provided
    if sum(provided_params.values()) < 2:
        raise ValueError("At least two out of (duration, sampling_frequency, number_of_samples) must be provided.")
    
    # Calculate missing parameters based on provided ones
    if "d" not in provided_params:
        duration = int(number_of_samples / sampling_frequency)
    if "f" not in provided_params:
        sampling_frequency = number_of_samples / duration
    if "n" not in provided_params:
        number_of_samples = int(duration * sampling_frequency)
    
    return number_of_samples, sampling_frequency

def calculate_frequencies_fft(signal,number_of_samples=None,sampling_frequency=None,duration=None):
    """
    Calculate the frequency values for the FFT of a signal.

    Parameters:
    signal (array-like): Input signal for which to calculate the FFT.
    sample_rate (float): Sampling rate of the input signal.

    Returns:
    tuple: A tuple containing:
        - frequencies (array-like): Array of frequency values corresponding to the FFT.
        - magnitudes (array-like): Magnitude values of the FFT.
    """
    N,fs = calculate_N_fs(duration=duration, sampling_frequency=sampling_frequency, number_of_samples=number_of_samples)
    # Compute the FFT of the signal
    fft_values = np.fft.fft(signal)
    fft_freqs = np.fft.fftfreq(N, d=1/fs)
    # Compute the magnitudes of the FFT
    magnitudes = np.abs(fft_values)/N

    return fft_freqs, magnitudes

def analyze_audio_spectrum(signal, fs=None, duration=None,number_of_samples=None, frequency_band_limit=3000):
    """
    Analyze the audio spectrum of a signal by calculating FFT and 1/3 octave band SPL.

    Parameters:
    signal (array-like): Input signal for which to analyze the spectrum.
    fs (int): Sampling frequency in Hz.
    duration (float): Duration of the signal in seconds.
    frequency_band_limit (float): Frequency band of interest in Hz.

    Returns:
    tuple: A tuple containing:
        - center_frequencies (list of float): Center frequencies for each 1/3 octave band.
        - spl_values (list of float): Calculated SPL values for each 1/3 octave band.
        - fft_freqs (array-like): Array of frequency values corresponding to the FFT.
        - magnitudes (array-like): Magnitude values of the FFT.
    """
    # Perform FFT calculation
    fft_freqs, magnitudes = calculate_frequencies_fft(signal, number_of_samples=number_of_samples, sampling_frequency=fs, duration=duration)
    
    # Calculate SPL for each 1/3 octave band
    center_frequencies, spl_values = calculate_1_3_octave_levels(fft_freqs, magnitudes)
    
    return center_frequencies, spl_values, fft_freqs, magnitudes