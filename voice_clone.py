#!/usr/bin/env python3
"""
Simple Voice Cloning with Chatterbox TTS
Using ResembleAI's production-grade open source TTS model
"""

import torch
import torchaudio as ta
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

# Import Chatterbox
from chatterbox.tts import ChatterboxTTS

def main():
    """Main function to demonstrate voice cloning"""
    
    print("🎙️ Chatterbox Voice Cloning")
    print("=" * 50)
    
    # Check GPU availability
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🎯 Using device: {device}")
    if device == "cuda":
        print(f"🚀 GPU: {torch.cuda.get_device_name(0)}")
    
    # Initialize Chatterbox model
    print("\n📥 Loading Chatterbox TTS model...")
    model = ChatterboxTTS.from_pretrained(device=device)
    print("✅ Model loaded successfully!")
    
    # Voice samples directory
    voice_samples_dir = Path("/home/alex/voice-samples")
    
    # Test texts for synthesis
    test_texts = [
        "Hello! This is a test of the voice cloning system using Chatterbox.",
        "The quick brown fox jumps over the lazy dog.",
        "Welcome to Chatterbox TTS, powered by Resemble AI. This model supports emotion control and voice cloning."
    ]
    
    # First, generate with default voice
    print("\n🎤 Generating with default voice...")
    default_text = test_texts[0]
    wav = model.generate(default_text)
    ta.save("output_default.wav", wav, model.sr)
    print(f"✅ Saved: output_default.wav")
    
    # Now generate with voice cloning using your samples
    print("\n🎭 Generating with voice cloning...")
    
    # Get the first voice sample as reference
    voice_samples = list(voice_samples_dir.glob("*.wav"))
    
    if voice_samples:
        # Use the first voice sample for cloning
        audio_prompt_path = str(voice_samples[0])
        print(f"📂 Using voice sample: {voice_samples[0].name}")
        
        for i, text in enumerate(test_texts, 1):
            print(f"\n📝 Text {i}: '{text[:50]}...'")
            
            # Generate with voice cloning
            wav = model.generate(
                text, 
                audio_prompt_path=audio_prompt_path
            )
            
            output_file = f"output_cloned_{i}.wav"
            ta.save(output_file, wav, model.sr)
            print(f"✅ Saved: {output_file}")
    else:
        print("⚠️ No voice samples found in ~/voice-samples/")
    
    print("\n🎉 Voice cloning complete!")
    print("Generated files:")
    print("  - output_default.wav (default voice)")
    if voice_samples:
        print("  - output_cloned_1.wav (cloned voice)")
        print("  - output_cloned_2.wav (cloned voice)")
        print("  - output_cloned_3.wav (cloned voice)")

if __name__ == "__main__":
    main()
