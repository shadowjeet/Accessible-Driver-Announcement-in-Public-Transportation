import pyaudio
from six.moves import queue


class StreamRecognition(object):

    def __init__(self, rate, chunk):
        self.new_rate = rate
        self.new_chunk = chunk
        self.buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self.pyaudio_interface = pyaudio.PyAudio()
        self.audio_stream = self.pyaudio_interface.open(
            format=pyaudio.paInt16,
            channels=1, rate=self.new_rate,
            input=True, frames_per_buffer=self.new_chunk,
            stream_callback=self.fill_buffer )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.closed = True
        self.buff.put(None)
        self.pyaudio_interface.terminate()

    def fill_buffer(self, in_data, frame_count, time_info, status_flag):
        self.buff.put(in_data)
        return None, pyaudio.paContinue

    def speech_generator(self):
        while not self.closed:
            chunk = self.buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self.buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b''.join(data)
