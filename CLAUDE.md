# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Communication Language

All communication with the user should be in Brazilian Portuguese (pt-BR).

## Project Overview

This is a hand tracking project using MediaPipe and OpenCV to detect and track hands via webcam. The system can identify which hand (left/right) is visible and determine which fingers are raised.

## Environment Setup

The project uses a Python virtual environment located in `.venv/`. To set up dependencies:

```bash
pip install -r requirements.txt
```

Key dependencies:
- `mediapipe==0.10.21` - Hand detection and tracking
- `opencv-python==4.12.0.88` - Webcam capture and image processing
- `numpy==2.0.2` - Numerical operations
- `openai-whisper==20250625` - Local speech recognition
- `sounddevice==0.5.3` - Audio recording from microphone
- `scipy==1.13.1` - Scientific computing (required for audio processing)

## Running the Application

To run the hand tracking application:

```bash
python detect_webcam.py
```

Controls:
- Press `Esc` to exit the application

## Running Tests

To test the voice recognition module:

```bash
python test_voice.py
```

To test voice recording and transcription interactively:

```bash
python voice_recognition.py
```

## Architecture

### Core Components

**detect_webcam.py** - Main application file for hand tracking:

1. **Camera Configuration** (lines 9-13)
   - Default resolution: 1280x720
   - Uses OpenCV VideoCapture for webcam access

2. **find_coord_hand()** (lines 15-39)
   - Processes frames to detect hands using MediaPipe
   - Returns both the annotated image and hand data
   - Parameters:
     - `img`: Input frame
     - `side_inverted`: Boolean to correct hand side labeling when camera is mirrored
   - Returns: Dictionary with keys:
     - `coordenadas`: List of 21 landmarks as (x, y, z) tuples in pixel coordinates
     - `side`: "Left" or "Right"

3. **fingers_raised()** (lines 41-50)
   - Detects which fingers are raised for a given hand
   - Checks fingertips at indices [8, 12, 16, 20] (index, middle, ring, pinky)
   - Compares fingertip y-coordinate with y-coordinate 2 positions back
   - Returns: Boolean list indicating raised fingers [index, middle, ring, pinky]
   - Note: Thumb detection not implemented

### Hand Landmark Indices

MediaPipe provides 21 landmarks per hand:
- Fingertip indices: 4 (thumb), 8 (index), 12 (middle), 16 (ring), 20 (pinky)
- Finger detection compares tip position with landmark 2 positions back (e.g., index tip at 8 vs landmark at 6)

### Image Processing Flow

1. Frame captured from webcam and flipped horizontally (line 54) to mirror the view
2. Frame converted BGR → RGB for MediaPipe processing
3. MediaPipe detects hands and landmarks
4. Landmarks drawn on frame
5. Finger state calculated for detected hands
6. Results displayed in window

**voice_recognition.py** - Voice recording and transcription module:

1. **VoiceRecorder Class**
   - `__init__(sample_rate, model_size)`: Initializes recorder with configurable sample rate (default 16000 Hz) and Whisper model size
   - `load_model()`: Downloads and loads Whisper model (only needed once, cached afterward)
   - `record_audio(duration, device)`: Records audio from microphone for specified duration
   - `save_audio(audio_data, filename)`: Saves recorded audio as WAV file in `temp/` directory
   - `transcribe_audio(audio_file, language)`: Transcribes audio file to text using Whisper
   - `record_and_transcribe(duration, save_file, language)`: Convenience method that records and transcribes in one call
   - `list_audio_devices()`: Lists all available audio input devices

2. **Whisper Model Sizes**
   - `tiny`: Fastest, least accurate (~39M parameters)
   - `base`: Good balance (default, ~74M parameters)
   - `small`: Better accuracy (~244M parameters)
   - `medium`: High accuracy (~769M parameters)
   - `large`: Best accuracy, slowest (~1550M parameters)

3. **Audio Configuration**
   - Sample rate: 16000 Hz (optimal for Whisper)
   - Format: Mono WAV files
   - Default recording duration: 5 seconds
   - Output directory: `temp/` (auto-created)

## Development Notes

### Hand Tracking (detect_webcam.py)
- The camera frame is mirrored (flipped horizontally) at line 54, but `side_inverted` parameter is not used in the main loop, which may cause hand side mislabeling
- Currently only processes finger data when exactly 1 hand is detected (line 60)
- Z-coordinate is scaled by `resolution_x` instead of a depth-specific scale factor (line 26)

### Voice Recognition (voice_recognition.py)
- First execution downloads Whisper model (~100-500 MB depending on size)
- Models are cached in `~/.cache/whisper/` for subsequent use
- Audio files saved in `temp/` directory with timestamp
- Portuguese language set as default (`language="pt"`)
- Requires microphone access - Windows may prompt for permissions
