# GEMINI Project Overview: Voice Clone

## Project Overview

This project is a Python-based voice cloning command-line application. It utilizes deep learning models to synthesize speech that mimics a provided voice sample. The project is optimized for NVIDIA GPUs, specifically the RTX 5070 Ti with the Blackwell architecture, and uses PyTorch with a specific CUDA version for acceleration.

The project includes two different implementations for voice cloning:
1.  **Chatterbox TTS**: The `clone_voice.py` script uses the `chatterbox-tts` library for voice cloning. It offers interactive and command-line modes, with controls for emotion and pacing.
2.  **Coqui TTS**: The `clone_voice_coqui.py` script uses the Coqui TTS library (`xtts_v2` model). It provides features like streaming for lower latency and control over voice characteristics like temperature and speed.

A third script, `voice_chat.py`, provides an interactive chat experience using the Coqui TTS implementation.

## Building and Running

### Prerequisites

*   **Python:** 3.11 (as specified in `.python-version`)
*   **NVIDIA GPU:** An NVIDIA GPU with CUDA support is recommended for performance. The project is optimized for the RTX 5070 Ti (Blackwell architecture).
*   **CUDA Driver:** 12.8+

### Installation

1.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    This will install all necessary packages, including the specific PyTorch version required for CUDA 12.8.

### Running the Application

The project provides three main scripts:

**1. `clone_voice.py` (Chatterbox TTS)**

*   **Interactive Mode:**
    ```bash
    python clone_voice.py
    ```
*   **Synthesize from command line:**
    ```bash
    python clone_voice.py "Hello, this is my cloned voice."
    ```
*   **Save to file:**
    ```bash
    python clone_voice.py "Save this message to a file." -o output.wav
    ```
*   **List available voice samples:**
    ```bash
    python clone_voice.py -l
    ```

**2. `clone_voice_coqui.py` (Coqui TTS)**

*   **Interactive Mode:**
    ```bash
    python clone_voice_coqui.py
    ```
*   **Synthesize from command line:**
    ```bash
    python clone_voice_coqui.py "This is a test using Coqui TTS."
    ```
*   **Use a specific voice sample:**
    ```bash
    python clone_voice_coqui.py "A different voice." -v /path/to/your/voice.wav
    ```

**3. `voice_chat.py`**

*   **Start an interactive voice chat session:**
    ```bash
    python voice_chat.py
    ```

## Development Conventions

*   **Dependency Management:** Project dependencies are managed in the `requirements.txt` file.
*   **Python Version:** The project uses a specific Python version (3.11), which is defined in the `.python-version` file for use with tools like `pyenv`.
*   **Modular Design:** The project is structured with separate scripts for different functionalities and TTS engines, making it easy to extend or modify.
*   **Command-line Interface:** All scripts provide a user-friendly command-line interface with clear arguments and help messages.
*   **Voice Samples:** The scripts expect voice samples to be located in the `~/voice-samples` directory.
