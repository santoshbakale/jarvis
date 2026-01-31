import pyaudio

p = pyaudio.PyAudio()
print("Available Audio Devices:")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if info.get('maxInputChannels') > 0:
        print(f"  [{i}] INPUT: {info.get('name')}")
    else:
        print(f"  [{i}] OUTPUT: {info.get('name')}")
p.terminate()
