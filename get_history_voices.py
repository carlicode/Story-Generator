import os
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment

# Initialize the ElevenLabs client
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

def generate_audio_for_text(text, voice_name, output_dir, part_index):
    """
    Generates an audio file for a specific text using the ElevenLabs API.

    Args:
        text (str): The text to convert into audio.
        voice_name (str): The name of the voice to use for the audio.
        output_dir (str): Directory where the audio file will be saved.
        part_index (int): The index of the story part, used for naming the file.

    Returns:
        str: Path to the generated audio file.
    """
    try:
        # Generate audio using ElevenLabs
        audio = client.generate(
            text=text,                 # Input text
            voice=voice_name,          # Voice to use
            model="eleven_multilingual_v2"  # Model for multilingual support
        )

        # Define the output file path
        output_file = os.path.join(output_dir, f"part_{part_index}.mp3")

        # Write the audio stream to the file
        with open(output_file, "wb") as f:
            for chunk in audio:  # Iterate through audio chunks
                if chunk:
                    f.write(chunk)

        print(f"Audio generated: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error generating audio for part {part_index}: {e}")
        return None

def combine_audio_files(audio_files, output_file):
    """
    Combines multiple audio files into a single file.

    Args:
        audio_files (list): List of file paths to the audio files to combine.
        output_file (str): Path where the combined audio file will be saved.

    Returns:
        str: Path to the combined audio file.
    """
    try:
        # Initialize an empty AudioSegment
        combined_audio = AudioSegment.empty()

        # Concatenate all audio files
        for file in audio_files:
            combined_audio += AudioSegment.from_file(file)

        # Export the combined audio to the specified path
        combined_audio.export(output_file, format="mp3")
        print(f"Combined audio saved at: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error combining audio files: {e}")
        return None

def generate_full_audio_from_json(story_json, output_dir, final_audio_path):
    """
    Generates a single audio file for a story based on a JSON structure.

    Args:
        story_json (list): A list of story parts in JSON format.
        output_dir (str): Directory to save the individual audio files.
        final_audio_path (str): Path to save the final combined audio file.

    Returns:
        str: Path to the final combined audio file.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    audio_files = []

    # Iterate through each part of the story
    for i, part in enumerate(story_json):
        print(f"Processing part {i}: {part['texto']}")
        # Generate audio for each part
        audio_file = generate_audio_for_text(
            text=part["texto"],          # Text of the story part
            voice_name=part["voz"],      # Voice assigned to the character
            output_dir=output_dir,       # Directory for temporary audio files
            part_index=i                 # Index for file naming
        )
        if audio_file:
            audio_files.append(audio_file)

    # Combine all generated audio files into a single file
    if audio_files:
        final_audio = combine_audio_files(audio_files, final_audio_path)
        return final_audio
    else:
        print("No audio files were generated.")
        return None
