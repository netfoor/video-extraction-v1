import wave 

def cut_audio(input_file, output_file, start_time, end_time):
    with wave.open(input_file, 'rb') as audio:
        frame_rate = audio.getframerate()
        start_frame = int(start_time * frame_rate)
        end_frame = int(end_time * frame_rate)
        
        audio.setpos(start_frame)
        frames = audio.readframes(end_frame - start_frame)
        
        with wave.open(output_file, 'wb') as output:
            output.setnchannels(audio.getnchannels())
            output.setsampwidth(audio.getsampwidth())
            output.setframerate(frame_rate)
            output.writeframes(frames)

if __name__ == "__main__":
    input_file = "/workspace/data/raw/100_Informal_Japanese_Phrases_for_Beginner-[ogqeb9TLO8A].wav"
    output_file = "/workspace/data/raw/cut_audio.wav"
    start_time = 145  # Start time in seconds
    end_time = 180    # End time in seconds
    
    cut_audio(input_file, output_file, start_time, end_time)
    print(f"Audio cut from {start_time} to {end_time} seconds and saved to {output_file}")