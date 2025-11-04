# Voice Clone Project

A voice cloning project with PyTorch, optimized for NVIDIA RTX 5070 Ti (Blackwell architecture).

## System Requirements

- **GPU**: NVIDIA RTX 5070 Ti (Blackwell architecture, sm_120)
- **OS**: EndeavourOS Linux (Arch-based)
- **Python**: 3.11.13 (managed via pyenv)
- **CUDA Driver**: 12.8+ (check with `nvidia-smi`)

## Setup Instructions

### Prerequisites

This project uses Python 3.11.13 managed by pyenv. The Python version is already configured in `.python-version`.

### Installation Steps

#### 1. Verify Python Version

First, ensure you're using the correct Python version:

```bash
python --version
# Output: Python 3.11.13
```

If you need to set up Python 3.11.13 with pyenv:

```bash
pyenv install 3.11.13
pyenv local 3.11.13
```

#### 2. Upgrade pip

Ensure you have the latest version of pip:

```bash
pip install --upgrade pip
```

#### 3. Install PyTorch with CUDA 12.8 Support

The RTX 5070 Ti uses NVIDIA's Blackwell architecture with compute capability sm_120. Standard PyTorch wheels don't support this architecture, so we need to install PyTorch with CUDA 12.8:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

This will install:
- PyTorch 2.8.0+cu128
- torchvision 0.23.0+cu128
- torchaudio 2.8.0+cu128
- All necessary CUDA 12.8 libraries

**Note**: This download is approximately 3.5GB in total.

#### 4. Verify Installation

Run the following to confirm everything is working:

```bash
python -c "
import torch
print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
print(f'CUDA version: {torch.version.cuda}')
print(f'GPU: {torch.cuda.get_device_name(0)}')
print(f'Compute capability: sm_{torch.cuda.get_device_capability(0)[0]}{torch.cuda.get_device_capability(0)[1]}')

# Test CUDA operations
x = torch.randn(1000, 1000).cuda()
y = torch.randn(1000, 1000).cuda()
z = torch.matmul(x, y)
print(f'✓ CUDA operations working! Result shape: {z.shape}')
"
```

Expected output:
```
PyTorch version: 2.8.0+cu128
CUDA available: True
CUDA version: 12.8
GPU: NVIDIA GeForce RTX 5070 Ti
Compute capability: sm_120
✓ CUDA operations working! Result shape: torch.Size([1000, 1000])
```

#### 5. Performance Verification (Optional)

Test GPU performance to ensure everything is running optimally:

```bash
python -c "
import torch
import time

print('Testing GPU performance...')
x = torch.randn(5000, 5000).cuda()
y = torch.randn(5000, 5000).cuda()

# Warm up
for _ in range(3):
    _ = torch.matmul(x, y)
torch.cuda.synchronize()

# Benchmark
start = time.time()
for _ in range(10):
    z = torch.matmul(x, y)
torch.cuda.synchronize()
end = time.time()

print(f'10x matrix multiplication (5000x5000): {end-start:.2f} seconds')
print(f'Performance: ~{10 * 2 * 5000**3 / (end-start) / 1e12:.2f} TFLOPS')
"
```

Expected performance for RTX 5070 Ti: ~30-35 TFLOPS

## Installed Packages

The setup includes the following key packages:

- **torch** 2.8.0+cu128 - PyTorch with CUDA 12.8 support
- **torchvision** 0.23.0+cu128 - Computer vision library for PyTorch
- **torchaudio** 2.8.0+cu128 - Audio processing library for PyTorch
- **numpy** 2.1.2 - Numerical computing library
- **pillow** 11.0.0 - Image processing library
- **CUDA libraries** - Full suite of NVIDIA CUDA 12.8 runtime libraries

## Troubleshooting

### Common Issues

1. **sm_120 Compatibility Warning**
   - If you see warnings about sm_120 not being supported, ensure you've installed PyTorch from the cu128 index URL as shown above.

2. **CUDA Not Available**
   - Check NVIDIA drivers: `nvidia-smi`
   - Ensure CUDA driver version is 12.8 or higher

3. **Import Errors**
   - Make sure you're in the correct Python environment
   - Verify with: `which python` and `python --version`

4. **Performance Issues**
   - Check GPU utilization: `nvidia-smi`
   - Ensure no other processes are using the GPU heavily

## Project Structure

```
voice-clone/
├── README.md           # This file
└── .python-version     # Python version specification (3.11.13)
```

## Voice Cloning with Chatterbox TTS

### Quick Start

This project uses ResembleAI's Chatterbox TTS model for high-quality voice cloning.

#### Basic Usage

```bash
# Play synthesized speech immediately (no file saved)
python clone_voice.py "Hello, this is my cloned voice!"

# Save to file and play
python clone_voice.py "Save this message" -o output.wav

# Save without playing
python clone_voice.py "Just save this" -o output.wav --no-play

# Use a specific voice sample
python clone_voice.py "Custom voice" -v ~/voice-samples/1.wav

# List available voice samples
python clone_voice.py -l
```

#### Emotion and Pacing Control

```bash
# Custom emotion settings
python clone_voice.py "I'm so excited!" -e 0.8 -c 0.3

# Dramatic preset (high emotion, deliberate pacing)
python clone_voice.py "This is AMAZING!" --dramatic

# Calm preset (low emotion, steady pacing)  
python clone_voice.py "Everything is peaceful" --calm

# Fine-tune parameters
# -e/--exaggeration: 0.0-1.0 (higher = more expressive)
# -c/--cfg: 0.0-1.0 (lower = more dramatic pacing)
```

#### Interactive Mode

Run without arguments for interactive text-to-speech. In this mode, you can dynamically adjust the `exaggeration` and `cfg` parameters on the fly to fine-tune the voice output.

```bash
python clone_voice.py
# Then type text and press Enter to hear it spoken

# Interactive commands:
!exaggeration <value>   # Set emotion intensity (0.0-1.0, e.g., !exaggeration 0.8)
!cfg <value>            # Set pacing/guidance (0.0-1.0, e.g., !cfg 0.3)
!help                   # Show available commands
!quit or !exit          # Exit interactive mode
```

### Script

**`clone_voice.py`** - Complete voice cloning tool with:
  - Audio playback by default (no file saved)
  - Optional file saving with `-o` flag
  - Interactive mode for continuous TTS
  - Dynamic emotion and pacing controls
  - Preset modes for quick access

### Voice Samples

Place your voice samples in `~/voice-samples/` as WAV files. The model will use these for voice cloning.

### Features

- 🚀 GPU accelerated with RTX 5070 Ti support
- 🎭 Zero-shot voice cloning
- 🎵 High-quality speech synthesis
- 💬 Interactive mode for real-time TTS
- 📂 Automatic voice sample detection
- 🎆 Dynamic emotion control (exaggeration)
- ⏱️ Adjustable pacing (CFG weight)
- 🎨 Preset modes for dramatic and calm speech

## Additional Resources

- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
- [CUDA Toolkit Documentation](https://docs.nvidia.com/cuda/)
- [RTX 5070 Ti sm_120 Compatibility Guide](file:///home/alex/README_SM_120_ERROR.md)

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

---

*Setup completed: September 7, 2025*  
*Environment: EndeavourOS Linux with RTX 5070 Ti*
