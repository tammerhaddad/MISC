import torch
import torchaudio
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voice
import os
import re

def split_text_into_chunks(text, max_chars=300):
    """Split text into chunks at sentence boundaries, keeping under max_chars"""
    if max_chars < 1:
        raise ValueError(f"max_chars must be at least 1, got {max_chars}")

    # Split by sentence endings
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # A sentence can be longer than max_chars all by itself -- epub text often
    # has headings and passages with no terminal punctuation -- so break those
    # at the last word boundary that fits. Any whitespace counts, not just
    # " ": the chapter files this reads are newline-separated.
    pieces = []
    for sentence in sentences:
        sentence = sentence.strip()
        while len(sentence) > max_chars:
            boundary = re.search(r'\s\S*$', sentence[:max_chars + 1])
            # no boundary to use means a single word longer than max_chars
            cut = boundary.start() if boundary and boundary.start() > 0 else max_chars
            pieces.append(sentence[:cut].strip())
            sentence = sentence[cut:].lstrip()
        if sentence:
            pieces.append(sentence)

    chunks = []
    current_chunk = ""

    for sentence in pieces:
        # If adding this sentence would exceed max_chars, start a new chunk.
        # The +1 is the space joined in below; without it chunks ran one over.
        if current_chunk and len(current_chunk) + 1 + len(sentence) > max_chars:
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
    
    # Split text into manageable chunks first, so an empty input fails here
    # rather than after the model and voice have finished loading
    text_chunks = split_text_into_chunks(text)
    print(f"Split text into {len(text_chunks)} chunks")
    if not text_chunks:
        raise ValueError(f"{input_path} has no text to synthesize")

    # Check for GPU availability
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Initialize TTS with GPU support
    tts = TextToSpeech(use_deepspeed=False, kv_cache=True, device=device)
    
    # Load voice
    voice_samples, conditioning_latents = load_voice(voice)
    
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
    
    # Save as wav. splitext rather than replace('.mp3', '.wav') so that an
    # output name without a .mp3 suffix still lands on a .wav file.
    wav_path = os.path.splitext(output_path)[0] + '.wav'
    out_dir = os.path.dirname(os.path.abspath(wav_path))
    os.makedirs(out_dir, exist_ok=True)
    torchaudio.save(wav_path, full_audio_cpu, 24000)
    print(f"Saved {wav_path}")
    
    # # Convert wav to mp3
    # import subprocess
    # subprocess.run(['ffmpeg', '-y', '-i', wav_path, output_path], check=True)
    
    # # Optionally remove wav file
    # os.remove(wav_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python epubToMp3.py <input_text_file> <output_file>")
        print("Example: python epubToMp3.py input.txt output.wav")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    print(f"Converting {input_file} to {output_file}...")
    text_file_to_mp3(input_file, output_file)
    print("Conversion complete!")
