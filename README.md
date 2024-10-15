# DevOps Terminal Symphony Script

**DevOps Terminal Symphony Script** is an advanced Python script designed to create a synchronized multimedia experience for the Visionaryx DevOps podcast. The script synchronizes audio playback with terminal text display, giving an immersive visual and auditory experience of DevOps tools communicating with each other.

## Overview

This script aims to bring a unique experience by combining a podcast audio track with a real-time transcript display in the terminal. Using elements of anthropomorphism, DevOps tools such as ArgoCD and Teleport are portrayed as characters engaging in conversations. The transcript is shown character-by-character in a terminal-like interface, enhancing the storytelling by mimicking a live terminal interaction.

Key features include:

- **Synchronized Audio-Text Playback**: The script plays the podcast audio while simultaneously displaying the corresponding dialogue text, all perfectly synced.
- **Speaker Differentiation**: Each speaker is color-coded for easy identification, enhancing readability and engagement.
- **Interactive Terminal Experience**: Text appears character-by-character with a typing effect, similar to a real-time terminal input.
- **Logging**: Key actions are logged to provide a complete audit trail of the process.

## Features

1. **Input Management**: The script accepts configuration settings via command-line arguments or from a configuration file. This includes paths to the podcast audio file and transcript CSV.

2. **Transcript Loading**: The script reads a CSV file containing dialogue information, including start and end timestamps, speaker names, and dialogue text. This information is loaded into a list of dictionaries for further use.

3. **Audio Playback**: Audio playback is managed in a separate thread using the `pydub` library to convert the audio to WAV format, followed by playing it with `afplay` for macOS users.

4. **Terminal Display**: As the audio plays, the corresponding transcript is displayed in the terminal, character by character. Each speaker's dialogue is shown in a different color for visual distinction. A custom shell prompt precedes each dialogue to simulate a terminal environment.

5. **Code Snippet Display**: If the dialogue contains a code snippet, it is highlighted in a distinctive color, simulating a terminal command or configuration example.

## Requirements

- **Python 3.x**
- **pydub**: For audio processing
- **afplay** (macOS): For playing the audio file
- **FFmpeg**: Required by pydub for audio conversion

You can install the necessary Python libraries using:
```bash
pip install pydub
```

## Usage

The script can be run using either command-line arguments or a configuration file.

### Command-Line Arguments

```bash
python devops_terminal_symphony.py \
  --podcast_audio_path /path/to/podcast.mp3 \
  --transcript_csv_path /path/to/transcript.csv
```

### Configuration File

You can also use a configuration file to specify input paths:

```ini
[Settings]
podcast_audio_path = /path/to/podcast.mp3
transcript_csv_path = /path/to/transcript.csv
```
Then run the script as:
```bash
python devops_terminal_symphony.py --config /path/to/config.ini
```

## How It Works

1. **Load Configuration**: The script loads the required audio and transcript paths from command-line arguments or a config file.
2. **Transcript Parsing**: The CSV transcript is parsed, extracting information like start and end timecodes, speaker names, and dialogue.
3. **Audio Playback and Sync**: Audio is played while the script uses timestamps to synchronize the display of text in the terminal.
4. **Enhanced Terminal Display**: A shell prompt with timestamp, episode number, and speaker name precedes the dialogue to create a realistic terminal interaction feel.

## Suggested Improvements

To make the experience even richer and more interactive, here are some potential features that could be added in the future:

- **Inline Code Display**: Highlighting code snippets during technical discussions can help users better understand specific instructions or configurations.
- **Interactive Elements**: Adding terminal effects, such as screen shaking or ASCII visualizations, could enhance user engagement.

## Visionaryx Podcast Context

Visionaryx is a creative podcast that brings DevOps and Cloud tools to life by giving them human-like personas. Inspired by the BBC Learning English podcast format, Visionaryx aims to teach both technical and language skills through engaging dialogues between DevOps tools like Docker, Kubernetes, and others. By humanizing these tools, the podcast helps listeners grasp complex technical concepts in a more approachable way.

The "DevOps Terminal Symphony Script" forms part of this creative effort, turning audio content into a dynamic visual experience that not only entertains but also educates.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by **BBC Learning English - Real Easy English**
- Special thanks to **ChatGPT** and other AI tools for assisting in English grammar.
- **pydub** for making audio handling straightforward.

