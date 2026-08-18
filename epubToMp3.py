import torch
import torchaudio
from tortoise.api import TextToSpeech, MODELS_DIR
from tortoise.utils.audio import load_voice
import os
import re

def split_text_into_chunks(text, max_chars=300):
    """Split text into chunks at sentence boundaries, keeping under max_chars"""
    # Split by sentence endings
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        # If adding this sentence would exceed max_chars, start a new chunk
        if len(current_chunk) + len(sentence) > max_chars and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += " " + sentence if current_chunk else sentence
    
    # Add the last chunk if it's not empty
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks

def text_file_to_mp3(input_path, output_path, voice='train_mouse', preset='high_quality'):
    # Read text from file
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Check for GPU availability
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Initialize TTS with GPU support
    tts = TextToSpeech(use_deepspeed=False, kv_cache=True, device=device)
    
    # Load voice
    voice_samples, conditioning_latents = load_voice(voice)
    
    # Split text into manageable chunks
    text_chunks = split_text_into_chunks(text)
    print(f"Split text into {len(text_chunks)} chunks")
    
    # Generate audio for each chunk
    audio_chunks = []
    for i, chunk in enumerate(text_chunks):
        print(f"Processing chunk {i+1}/{len(text_chunks)}...")
        
        gen = tts.tts_with_preset(
            chunk,
            voice_samples=voice_samples,
            conditioning_latents=conditioning_latents,
            preset=preset
        )
        
        audio_chunks.append(gen.squeeze(0))
    
    # Concatenate all audio chunks
    print("Concatenating audio chunks...")
    full_audio = torch.cat(audio_chunks, dim=1)
    
    # Move tensor to CPU for saving
    full_audio_cpu = full_audio.cpu()
    
    # Save as wav
    wav_path = output_path.replace('.mp3', '.wav')
    torchaudio.save(wav_path, full_audio_cpu, 24000)
    
    # # Convert wav to mp3
    # import subprocess
    # subprocess.run(['ffmpeg', '-y', '-i', wav_path, output_path], check=True)
    
    # # Optionally remove wav file
    # os.remove(wav_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python epubToMp3 <input_text_file> <output_mp3_file>")
        print("Example: python epubToMp3 input.txt output.mp3")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    print(f"Converting {input_file} to {output_file}...")
    text_file_to_mp3(input_file, output_file)
    print("Conversion complete!")
