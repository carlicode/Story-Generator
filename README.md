# Story-Generator
# AI-Powered Children's Story Generator

This project is a web application that generates children's stories with audio narration using OpenAI and ElevenLabs APIs. Users can input a story idea, customize characters, and get a complete story with descriptive narration and voices tailored to each character.

## Features

- **Story Generation**: Creates immersive stories with a clear narrative structure (Introduction, Development, Climax, and Resolution).
- **Character Voices**: Assigns consistent voices to characters using ElevenLabs API.
- **Audio Generation**: Converts text to audio, combines parts, and creates a final audio file of the entire story.
- **Customizable**: Allows users to save or discard the generated text and audio.

## Technologies Used

- **Streamlit**: Interactive web interface.
- **OpenAI API**: For generating stories.
- **ElevenLabs API**: For text-to-speech conversion.
- **Python**: Core programming language.
- **Pydub**: For combining and processing audio files.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/ai-story-generator.git
    cd ai-story-generator
    ```

2. Set up a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the `.env` file:
    Create a `.env` file in the root directory with the following keys:
    ```
    OPENAI_API_KEY=your_openai_api_key
    ELEVENLABS_API_KEY=your_elevenlabs_api_key
    ```

5. Run the application:
    ```bash
    streamlit run main.py
    ```

## Usage

1. Open the web application in your browser (usually at `http://localhost:8501`).
2. Enter the name of the main character and a story idea.
3. Generate the story and audio.
4. Decide whether to save the story and audio to the `Cuentos` directory.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
