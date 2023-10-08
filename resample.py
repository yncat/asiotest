import wave
import array
import struct

def resample_waveform(input_waveform, input_sample_rate, output_sample_rate):
    # Calculate the resampling ratio
    resample_ratio = output_sample_rate / input_sample_rate

    # Calculate the number of output samples
    output_length = int(len(input_waveform) * resample_ratio)

    # Create a new array for the output waveform
    output_waveform = array.array('h', [0] * output_length)

    # Perform resampling using simple linear interpolation
    for i in range(output_length):
        input_index = int(i / resample_ratio)
        output_waveform[i] = input_waveform[input_index]

    return output_waveform

# Example usage
if __name__ == "__main__":
    input_file = "fstest.wav"
    output_file = "output.wav"

    input_sample_rate = 22050
    output_sample_rate = 44100

    # Load the input waveform from a WAV file (requires the wave module)
    with wave.open(input_file, 'rb') as wav_in:
        input_waveform = array.array('h', wav_in.readframes(wav_in.getnframes()))

    # Resample the waveform
    output_waveform = resample_waveform(input_waveform, input_sample_rate, output_sample_rate)

    # Save the resampled waveform to a WAV file (requires the wave module)
    with wave.open(output_file, 'wb') as wav_out:
        wav_out.setparams((1, 2, output_sample_rate, 0, 'NONE', 'not compressed'))
        wav_out.writeframes(output_waveform.tobytes())
