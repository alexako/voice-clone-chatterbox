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
    
    def synthesize(self, text, output_path=None, play_audio=True, exaggeration=0.5, cfg_weight=0.5):
        """Generate speech from text
        
        Args:
            text: Text to synthesize
            output_path: Optional path to save audio file
            play_audio: Whether to play the audio
            exaggeration: Emotion intensity (0.0-1.0, higher = more expressive)
            cfg_weight: Guidance scale (0.0-1.0, lower = more dramatic pacing)
        """
        
        print(f"\n📝 Text: '{text[:80]}{'...' if len(text) > 80 else ''}'")
        print(f"🎭 Settings: exaggeration={exaggeration}, cfg={cfg_weight}")
        print("🔄 Generating speech...")
        
        if self.voice_sample:
            wav = self.model.generate(
                text, 
                audio_prompt_path=self.voice_sample,
                exaggeration=exaggeration,
                cfg_weight=cfg_weight
            )
        else:
            wav = self.model.generate(
                text,
                exaggeration=exaggeration,
                cfg_weight=cfg_weight
            )
        
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
                subprocess.run(["ffplay", "-nodisp", "-autoexit", audio_file], check=True, capture_output=True)
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
    parser.add_argument("-e", "--exaggeration", type=float, default=0.5, 
                       help="Emotion intensity (0.0-1.0, default: 0.5, higher = more expressive)")
    parser.add_argument("-c", "--cfg", type=float, default=0.5,
                       help="CFG weight (0.0-1.0, default: 0.5, lower = more dramatic pacing)")
    parser.add_argument("--dramatic", action="store_true",
                       help="Preset for dramatic speech (exaggeration=0.7, cfg=0.3)")
    parser.add_argument("--calm", action="store_true",
                       help="Preset for calm speech (exaggeration=0.3, cfg=0.6)")
    
    args = parser.parse_args()
    
    # Apply presets if specified
    if args.dramatic:
        args.exaggeration = 0.7
        args.cfg = 0.3
        print("🎭 Using dramatic preset (exaggeration=0.7, cfg=0.3)")
    elif args.calm:
        args.exaggeration = 0.3
        args.cfg = 0.6
        print("😌 Using calm preset (exaggeration=0.3, cfg=0.6)")
    
    # Validate ranges
    if not 0.0 <= args.exaggeration <= 1.0:
        print("⚠️ Exaggeration must be between 0.0 and 1.0")
        args.exaggeration = max(0.0, min(1.0, args.exaggeration))
    if not 0.0 <= args.cfg <= 1.0:
        print("⚠️ CFG weight must be between 0.0 and 1.0")
        args.cfg = max(0.0, min(1.0, args.cfg))
    
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
        print("Type '!help' for commands")
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
                # Check for inline commands
                if text.startswith("!"):
                    parts = text[1:].split()
                    if parts[0] == "exaggeration" and len(parts) > 1:
                        try:
                            args.exaggeration = float(parts[1])
                            print(f"🎭 Exaggeration set to {args.exaggeration}")
                        except ValueError:
                            print("⚠️ Invalid value for exaggeration")
                        continue
                    elif parts[0] == "cfg" and len(parts) > 1:
                        try:
                            args.cfg = float(parts[1])
                            print(f"🎯 CFG weight set to {args.cfg}")
                        except ValueError:
                            print("⚠️ Invalid value for cfg")
                        continue
                    elif parts[0] == "help":
                        print("\n📚 Interactive commands:")
                        print("  !exaggeration <0.0-1.0> - Set emotion intensity")
                        print("  !cfg <0.0-1.0> - Set CFG weight")
                        print("  !help - Show this help")
                        continue
                
                cloner.synthesize(
                    text, 
                    output_path=None, 
                    play_audio=True,
                    exaggeration=args.exaggeration,
                    cfg_weight=args.cfg
                )
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    # Single synthesis mode
    else:
        play = not args.no_play
        cloner.synthesize(
            args.text, 
            output_path=args.output, 
            play_audio=play,
            exaggeration=args.exaggeration,
            cfg_weight=args.cfg
        )

if __name__ == "__main__":
    main()
