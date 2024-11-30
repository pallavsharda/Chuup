import pyaudio
import numpy as np
import time

def test_mic_sensitivity():
    CHUNK = 2048
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 44100
    
    # Test different thresholds
    thresholds = [0.001, 0.002, 0.003, 0.005, 0.008, 0.01]
    current_threshold_idx = 2  # Start with 0.003
    
    print("\n=== Microphone Sensitivity Test ===")
    print("Press Ctrl+C to move to next threshold")
    print("=====================================")
    
    p = pyaudio.PyAudio()
    stream = None
    max_level_seen = 0
    
    try:
        # Configure input stream
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            stream_callback=None,
            start=False  # Don't start immediately
        )
        
        # Start the stream
        stream.start_stream()
        
        while current_threshold_idx < len(thresholds):
            threshold = thresholds[current_threshold_idx]
            print(f"\nTesting threshold: {threshold:.4f}")
            print("Speak at your normal distance...")
            
            try:
                while True:
                    if stream.is_active():
                        try:
                            data = stream.read(CHUNK, exception_on_overflow=False)
                            current_level = np.abs(np.frombuffer(data, dtype=np.float32)).mean()
                            max_level_seen = max(max_level_seen, current_level)
                            
                            # Visual representation
                            level_bar = "█" * min(int(current_level * 1000), 50)  # Limit bar length
                            threshold_bar = "▓" * min(int(threshold * 1000), 50)  # Limit bar length
                            
                            if current_level > threshold:
                                print(f"\rLevel: {current_level:.6f} {level_bar}")
                                print(f"Thresh: {threshold:.6f} {threshold_bar} SPEAKING", end="")
                            else:
                                print(f"\rLevel: {current_level:.6f} {level_bar}")
                                print(f"Thresh: {threshold:.6f} {threshold_bar} quiet", end="")
                                
                        except IOError as e:
                            print(f"\nStream error (retrying): {e}")
                            time.sleep(0.1)  # Short delay before retry
                            
            except KeyboardInterrupt:
                current_threshold_idx += 1
                print(f"\n\nMax level seen: {max_level_seen:.6f}")
                if current_threshold_idx < len(thresholds):
                    input("\nPress Enter to test next threshold...")
                
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        if stream is not None:
            if stream.is_active():
                stream.stop_stream()
            stream.close()
        p.terminate()
        
        print("\n\n=== Results ===")
        print(f"Maximum level detected: {max_level_seen:.6f}")
        print("\nRecommended thresholds:")
        print(f"Very sensitive: {max_level_seen * 0.1:.6f}")
        print(f"Moderate: {max_level_seen * 0.2:.6f}")
        print(f"Less sensitive: {max_level_seen * 0.3:.6f}")

if __name__ == "__main__":
    test_mic_sensitivity() 