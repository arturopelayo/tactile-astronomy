
import numpy

class AudioMixer(object):

    def mixdown(self, voices):
        active_voices = filter(lambda x: x is not None, voices)
        if len(active_voices) == 1:
            combined = active_voices[0]
        else:
            lengths = [len(v) for v in active_voices]
            max_len = max(lengths)
            min_len = min(lengths)
            # if there are differences in lengths, we need to pad
            if max_len != min_len:
                for i in range(len(active_voices)):
                    len_diff = max_len - len(active_voices[i])
                    if len_diff > 0:
                        # pad difference with zeroes
                        active_voices[i] = numpy.pad(active_voices[i],
                                                     ((0, len_diff), (0, 0)),
                                                     'constant',
                                                     constant_values=(0, 0))
            combined =  numpy.mean(active_voices, axis=0, dtype=numpy.int16)
        return combined
