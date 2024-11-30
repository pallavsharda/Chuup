import pyaudio
import numpy as np
import time

def test_mic_activity():
    CHUNK = 1024
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 44100
    THRESHOLD = 0.01
    
    p = pyaudio.PyAudio()
    speaking_time = 0
    start_time = time.time()
    
    print("\n=== Microphone Threshold Calibration ===")
    print(f"Initial threshold: {THRESHOLD}")
    print("Press Ctrl+C to stop")
    print("=====================================")
    print("Reference Audio Levels:")
    print("🔈 0.001 (very quiet/background)")
    print("🔉 0.01  (current threshold)")
    print("🔊 0.1   (loud speech)")
    print("=====================================\n")
    
    try:
        stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK)
        
        print("Monitoring audio levels...")
        last_check = time.time()
        
        while True:
            data = np.frombuffer(stream.read(CHUNK), dtype=np.float32)
            current_level = np.abs(data).mean()
            current_time = time.time()
            
            # Visual representation of audio level
            level_indicator = "▁▂▃▄▅▆▇█"
            level_index = min(int(current_level * 80), len(level_indicator) - 1)
            bar = level_indicator[level_index]
            
            if current_level > THRESHOLD:
                speaking_time += current_time - last_check
                print(f"\rLevel: {current_level:.6f} {bar} SPEAKING (Total: {speaking_time:.1f}s)", end="")
            else:
                print(f"\rLevel: {current_level:.6f} {bar} quiet", end="")
                
            last_check = current_time
            
    except KeyboardInterrupt:
        print("\n\n=== Calibration Results ===")
        total_time = time.time() - start_time
        print(f"Total time: {total_time:.1f} seconds")
        print(f"Activity time: {speaking_time:.1f} seconds")
        print(f"Activity ratio: {(speaking_time/total_time)*100:.1f}%")
        print("\nRecommendation:")
        print(f"Based on your audio levels, consider using a threshold between:")
        print(f"- Quiet threshold: {max(0.001, current_level * 2):.6f}")
        print(f"- Active threshold: {max(0.005, current_level * 5):.6f}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    test_mic_activity() 