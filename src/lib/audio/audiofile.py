
from soundfile import SoundFile

class AudioFile(SoundFile):
    def __init__(self, path):
        self.path = path
        self.is_playing = False
        self.is_finished = False
        super(AudioFile, self).__init__(path, 'r')

    def play(self):
        self.is_playing = True
        self.is_finished = False

    def pause(self):
        self.is_playing = not self.is_playing

    def stop(self):
        self.is_playing = False
        self.is_finished = True
        self.seek(0) # Go back to the beginning

    def read(self, num_frames):
        data =  super(AudioFile, self).read(num_frames, 'int16', always_2d=True)
        if len(data) == 0:
            self.stop()
        return data
