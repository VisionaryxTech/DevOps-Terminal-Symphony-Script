#!/usr/bin/env python3
import csv
import os
import subprocess
from datetime import datetime
import argparse
import configparser
import logging
from pydub import AudioSegment
from threading import Thread
import time
import sys
import random

parser = argparse.ArgumentParser(description="DevOps Terminal Symphony Script")
parser.add_argument("--config", help="Path to configuration file", required=False)
parser.add_argument("--podcast_audio_path", help="Path to the podcast audio file", required=False)
parser.add_argument("--transcript_csv_path", help="Path to the transcript CSV file", required=False)
args = parser.parse_args()

if args.config:
    config = configparser.ConfigParser()
    config.read(args.config)
    podcast_audio_path = config.get("Settings", "podcast_audio_path")
    transcript_csv_path = config.get("Settings", "transcript_csv_path")
elif args.podcast_audio_path and args.transcript_csv_path:
    podcast_audio_path = args.podcast_audio_path
    transcript_csv_path = args.transcript_csv_path
else:
    raise ValueError("Please provide either a configuration file or all required arguments.")

# Output Paths
output_video_path = "output_video.mp4"
log_file_path = "terminal_symphony_log.txt"

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler(log_file_path)
])

logging.info("Script started.")

# Load Transcript
def load_transcript(csv_path):
    transcript = []
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            start_time = row.get('Start Timecode', '0:00:00.00')
            end_time = row.get('End Timecode', '0:00:00.00')
            try:
                start_seconds = sum(float(x) * 60 ** i for i, x in enumerate(reversed(start_time.split(':'))))
                end_seconds = sum(float(x) * 60 ** i for i, x in enumerate(reversed(end_time.split(':'))))
            except ValueError:
                start_seconds = 0
                end_seconds = 0
            transcript.append({
                "start": start_seconds,
                "end": end_seconds,
                "speaker": row.get('Speaker', 'Unknown'),
                "text": row.get('Transcript', ''),
                "code": row.get('Code', '')
            })
    return transcript

transcript = load_transcript(transcript_csv_path)
logging.info("Transcript loaded.")

# Color Settings for Speakers
speaker_colors = {
    "ArgoCD": ("\033[1;36m", "\033[0m"),  # Cyan for ArgoCD
    "Teleport": ("\033[1;35m", "\033[0m"),  # Magenta for Teleport
    "Unknown": ("\033[1;37m", "\033[0m")  # White for Unknown
}

# Font size settings for terminal output
font_size_start = "\033#6"  # Set double-height and double-width text (larger font)
font_size_reset = "\033#3"  # Reset to normal size

# Play Audio and Display Transcript
stop_threads = False

def play_audio():
    audio = AudioSegment.from_file(podcast_audio_path)
    audio.export("temp_audio.wav", format="wav")
    subprocess.run(["afplay", "temp_audio.wav"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

logging.info("Starting audio playback and transcript display.")

# Running Audio and Transcript Synchronization in Background
audio_thread = Thread(target=play_audio)
audio_thread.start()

start_time = time.time()
episode_number = 13  # Episode number

def type_text(text, color, reset_color, duration):
    char_count = len(text)
    typing_interval = min(0.05, duration / max(char_count, 1))
    for char in text:
        # Simulate human-like typing with slight randomness
        sys.stdout.write(f"{font_size_start}{color}{char}{reset_color}{font_size_reset}")
        sys.stdout.flush()
        time.sleep(typing_interval * random.uniform(0.8, 1.2))  # Adding randomness to the typing speed
        # Add cursor blinking effect
        sys.stdout.write("\033[5 q")  # Set blinking cursor
        sys.stdout.flush()

# Clear the screen once at the beginning
sys.stdout.write("\033[H\033[J")

for entry in transcript:
    # Wait until it's time to start this entry
    while time.time() - start_time < entry["start"]:
        time.sleep(0.01)

    if stop_threads:
        break

    speaker_color, reset_color = speaker_colors.get(entry['speaker'], ("\033[1;37m", "\033[0m"))
    shell_prompt = (f"{font_size_start}\033[1;32m{datetime.now().strftime('%H:%M:%S')}\033[0m "
                    f"Episode {episode_number} @ Visionaryx - {speaker_color}{entry['speaker']}{reset_color} "
                    f"\033[1;33m~\033[0m \033[1;34m(main) (git:master)\033[0m{font_size_reset}")
    print(f"{shell_prompt}")
    print()  # Add a blank line between shell prompt and dialogue
    sys.stdout.write(f"{font_size_start}\033[1m\033[38;5;15m$ \033[0m{font_size_reset}")  # Add a bold and bright white command prompt symbol
    sys.stdout.flush()
    logging.info(f"[{datetime.now().strftime('%H:%M:%S')}] {entry['speaker']}: {entry['text']}")

    # Type the text slightly faster than audio
    duration = entry["end"] - entry["start"]
    type_text(entry['text'], speaker_color, reset_color, duration)
    print("\033[0m")  # Reset to normal after the dialogue
    print()  # Add an extra blank line for readability

    # Check if there is non-empty code to display
    if entry['code'].strip():
        print(f"{font_size_start}\033[1m\033[38;5;214mCode Snippet:\033[0m{font_size_reset}")
        print(f"{font_size_start}\033[1;32m{entry['code']}\033[0m{font_size_reset}")  # Display the code in green color
        print()  # Add an extra blank line for readability

        # Simulate code execution
        execution_message = "\033[1;33m[Executing... Done]\033[0m"
        sys.stdout.write(f"{execution_message}\n")
        sys.stdout.flush()
        time.sleep(1)  # Pause to simulate code execution time

    # Wait until the end time of this entry
    while time.time() - start_time < entry["end"]:
        time.sleep(0.01)

# Stop the time display thread
stop_threads = True

logging.info("Transcript display completed.")

logging.info("Script finished.")

# Print completion message
print(f"\n\033[1mProcess complete. The generated video is saved at: {output_video_path}\033[0m")
