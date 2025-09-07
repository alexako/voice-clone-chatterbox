#!/usr/bin/env python3
"""
Interactive Voice Cloning Script
Simple command-line tool for text-to-speech with voice cloning
"""

import torch
import torchaudio as ta
from pathlib import Path
import argparse
import sys
import warnings
import tempfile
import subprocess
import os
warnings.filterwarnings("ignore")

from chatterbox.tts import ChatterboxTTS

class VoiceCloner:
    def __init__(self, voice_sample_path=None):
        """Initialize the voice cloner with optional voice sample"""
        
        # Check device
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🎯 Using device: {self.device}")
        if self.device == "cuda":
            print(f"🚀 GPU: {torch.cuda.get_device_name(0)}")
        
        # Load model
        print("📥 Loading Chatterbox TTS model...")
        self.model = ChatterboxTTS.from_pretrained(device=self.device)
        print("✅ Model loaded!\n")
        
        # Set voice sample
        self.voice_sample = voice_sample_path
        if self.voice_sample:
            print(f"🎭 Using voice sample: {Path(self.voice_sample).name}")
        else:
            print("🎤 Using default voice")
    
    def synthesize(self, text, output_path=None, play_audio=True):
        """Generate speech from text"""
        
        print(f"\n📝 Text: '{text[:80]}{'...' if len(text) > 80 else ''}'")
        print("🔄 Generating speech...")
        
        if self.voice_sample:
            wav = self.model.generate(text, audio_prompt_path=self.voice_sample)
        else:
            wav = self.model.generate(text)
        
        # Use temp file if no output path specified
        if output_path:
            ta.save(output_path, wav, self.model.sr)
            print(f"💾 Saved to: {output_path}")
            audio_file = output_path
        else:
            # Create temp file for playback
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                ta.save(tmp.name, wav, self.model.sr)
                audio_file = tmp.name
        
        # Play audio if requested
        if play_audio:
            print("🔊 Playing audio...")
            try:
                subprocess.run(["aplay", audio_file], check=True, capture_output=True)
                print("✅ Playback complete")
            except subprocess.CalledProcessError:
                print("⚠️ Could not play audio (aplay not found or audio system issue)")
            except Exception as e:
                print(f"⚠️ Playback error: {e}")
        
        # Clean up temp file if used
        if not output_path and os.path.exists(audio_file):
            os.unlink(audio_file)
        
        return audio_file

def main():
    parser = argparse.ArgumentParser(description="Voice Cloning with Chatterbox TTS")
    parser.add_argument("text", nargs="?", help="Text to synthesize (optional for interactive mode)")
    parser.add_argument("-v", "--voice", help="Path to voice sample WAV file")
    parser.add_argument("-o", "--output", help="Save output to file (if not specified, only plays audio)")
    parser.add_argument("-l", "--list-voices", action="store_true", help="List available voice samples")
    parser.add_argument("--no-play", action="store_true", help="Don't play audio (useful with -o)")
    
    args = parser.parse_args()
    
    # List voice samples if requested
    if args.list_voices:
        voice_dir = Path("/home/alex/voice-samples")
        print("📂 Available voice samples:")
        for wav_file in voice_dir.glob("*.wav"):
            print(f"  - {wav_file.name}")
        return
    
    # If no voice specified, check for samples
    if not args.voice:
        voice_dir = Path("/home/alex/voice-samples")
        voice_samples = list(voice_dir.glob("*.wav"))
        if voice_samples:
            # Use first sample by default
            args.voice = str(voice_samples[0])
            print(f"📂 Auto-selected voice sample: {voice_samples[0].name}")
            print("   (Use -v flag to specify a different voice sample)")
    
    # Initialize cloner
    cloner = VoiceCloner(args.voice)
    
    # Interactive mode if no text provided
    if not args.text:
        print("\n" + "="*50)
        print("🎙️ Interactive Voice Cloning Mode")
        print("Type your text and press Enter to generate speech")
        print("Type 'quit' or 'exit' to stop")
        print("="*50)
        
        while True:
            try:
                text = input("\n> ").strip()
                
                if text.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not text:
                    print("⚠️ Please enter some text")
                    continue
                
                # In interactive mode, just play unless user specifies otherwise
                cloner.synthesize(text, output_path=None, play_audio=True)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    # Single synthesis mode
    else:
        play = not args.no_play
        cloner.synthesize(args.text, output_path=args.output, play_audio=play)

if __name__ == "__main__":
    main()
