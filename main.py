import streamlit as st
import json
import os
import shutil  # To delete directories and their contents
from story import load_api_key, get_openai_response, clean_response_content
from get_history_voices import generate_full_audio_from_json

# Load API Key
api_key = load_api_key()
if not api_key:
    st.error("Error: API Key not found. Make sure it's set in the .env file.")
    st.stop()

# Load voices from the JSON file
def load_voices():
    """
    Loads available voice configurations from a JSON file.
    """
    try:
        with open("voices.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading voices.json: {e}")
        st.stop()

# Function to generate the story
def generate_story(main_character_name, user_message):
    """
    Generates a story in JSON format based on user inputs and the available voices.

    Args:
        main_character_name (str): Name of the main character.
        user_message (str): Instructions or story details from the user.

    Returns:
        list: The story in JSON format with character details and assigned voices.
    """
    # Load voices from the JSON file
    voices = load_voices()

    # Convert voices.json into a structured list for the prompt
    voices_list = "\n".join([f"- {voice['name']}" for voice in voices])

    # Create the system prompt
    system_prompt = f"""
    Crea un cuento para niños en formato JSON con las siguientes características:

    0. Indicación del usuario: {user_message}

    1. **Estilo del cuento**:
    - El cuento debe ser entretenido, fácil de seguir y lleno de descripciones visuales para captar la atención de un niño.
    - Usa un lenguaje claro y palabras simples, pero incluye detalles que permitan imaginar la escena.
    - La narrativa debe ser educativa o dejar una enseñanza positiva al final.
    - El narrador debe explicar cuando un prsonaje hablará y usar textos como 'y {main_character_name} dijo'.

    2. **Personajes**:
    - **Narrador**: Desarrolla la historia de manera descriptiva, utilizando un tono cálido y amigable. Describe con detalle los lugares, emociones y acciones de los personajes para que el niño pueda imaginar cada escena con claridad.
    - **Personaje principal**: El cuento debe centrarse en el personaje principal llamado {main_character_name}.
    - Personajes secundarios: Añade personajes secundarios que apoyen la narrativa, fomenten la interacción y enriquezcan la historia.

    3. **Estructura de cada línea** del JSON:
    - `"personaje"`: Nombre del personaje o "Narrador".
    - `"genero"`: Género del personaje (femenino, masculino, neutro).
    - `"edad"`: Edad del personaje (en años o "indefinida" si no aplica).
    - `"emocion"`: La emoción predominante del personaje en esa línea.
    - `"fondo"`: Sonidos ambientales adecuados que acompañen la escena (por ejemplo, "canto de pájaros", "viento suave entre los árboles").
    - `"texto"`: Diálogo o narración correspondiente. Si es el narrador, describe de manera detallada la escena, los sentimientos o las acciones. Si es un personaje, mantén el diálogo simple y directo.
    - `"voz"`: Nombre de la voz asignada para este personaje. La misma voz debe ser utilizada consistentemente para el mismo personaje en todo el cuento. Usa una de las siguientes voces disponibles:

    {voices_list}

    4. **Estructura del cuento**:
    - **Introducción**: Presenta el mundo del cuento, el personaje principal y el conflicto o meta de la historia. Describe visualmente el entorno y las emociones iniciales.
    - **Desarrollo**: Incluye los eventos principales, los desafíos o aventuras del personaje principal. Mantén una narrativa progresiva que involucre a los personajes secundarios.
    - **Clímax**: Presenta el momento más emocionante o crucial del cuento, donde el personaje principal enfrenta y resuelve el desafío.
    - **Desenlace**: Cierra la historia con una resolución satisfactoria. Añade un mensaje positivo o una reflexión que el niño pueda recordar.

    5. **Ejemplo de salida** (no incluyas la palabra 'json' al principio, escribe directamente la información del json):
    [{{
        "personaje": "Narrador",
        "genero": "neutro",
        "edad": "indefinida",
        "emocion": "neutral",
        "fondo": "suave música de arpa",
        "texto": "En un pequeño pueblo rodeado de montañas verdes y cielos azules, vivía una joven llamada {main_character_name}. Era conocida por su curiosidad y su amor por la naturaleza.",
        "voz": "Aria"
    }}, {{
        "personaje": "{main_character_name}",
        "genero": "femenino",
        "edad": 16,
        "emocion": "curiosa",
        "fondo": "canto de pájaros",
        "texto": "Siempre me he preguntado qué hay más allá del bosque. Tal vez hoy sea el día de descubrirlo.",
        "voz": "Laura"
    }}, {{
        "personaje": "Narrador",
        "genero": "neutro",
        "edad": "indefinida",
        "emocion": "neutral",
        "fondo": "viento suave entre los árboles",
        "texto": "Con una canasta en la mano y mucha valentía, {main_character_name} se adentró en el bosque, donde los árboles se alzaban altos como gigantes y las hojas susurraban secretos al viento.",
        "voz": "Aria"
    }}]
    """


    # Call the model to generate the story
    model = "gpt-4o"
    try:
        response = get_openai_response(api_key, model, system_prompt, user_message)
        response_content = response.choices[0].message.content.strip()
        story_json = clean_response_content(response_content)

        return story_json
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Save story to file
def save_story_to_file(story_json, story_name):
    """
    Saves the generated story to a JSON file.

    Args:
        story_json (list): The story content in JSON format.
        story_name (str): The name of the file to save.

    Returns:
        str: The file path where the story was saved.
    """
    directory = "Cuentos"
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, f"{story_name}.json")
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(story_json, file, ensure_ascii=False, indent=4)
        return file_path
    except Exception as e:
        st.error(f"Error saving the file: {e}")
        return None

# Clean up audio parts
def cleanup_audio_parts(directory):
    """
    Deletes temporary audio files from a specified directory.

    Args:
        directory (str): The directory containing temporary audio files.
    """
    if os.path.exists(directory):
        try:
            shutil.rmtree(directory)
            print(f"Temporary audio parts in `{directory}` have been deleted.")
        except Exception as e:
            print(f"Error deleting temporary audio parts: {e}")

# Streamlit UI
st.title("Story Generator with AI 🚀")

# Input fields
main_character_name = st.text_input("Enter the name of the main character:", "Nisha")
user_message = st.text_area("What story do you want to generate?", "Crea una cuento sobre ....")

# Generate button
if st.button("Generate Story"):
    with st.spinner("Generating story... Please wait!"):
        story_result = generate_story(main_character_name, user_message)

        if story_result:
            st.success("Story successfully generated!")
            
            # Show the story
            st.subheader("Story:")
            for part in story_result:
                if part["personaje"] != "Narrador":
                    st.write(f"**{part['personaje']}:** {part['texto']} (Voice: {part['voz']})")
                else:
                    st.write(f"{part['texto']} (Voice: {part['voz']})")

            # Generate audio for the story
            output_dir = "Cuentos/audio_parts"
            final_audio_path = "Cuentos/temp_story.mp3"
            with st.spinner("Generating audio... Please wait!"):
                audio_path = generate_full_audio_from_json(story_result, output_dir, final_audio_path)

            if audio_path:
                st.success("Audio successfully generated!")
                # Play the audio in Streamlit
                st.audio(audio_path, format="audio/mp3")

                # Clean up temporary audio parts
                cleanup_audio_parts(output_dir)

                # Ask if the user wants to save the story and audio
                if st.checkbox("Would you like to save the story and audio?"):
                    story_name = st.text_input("Enter a name for your story:", "my_story")
                    if st.button("Save Story and Audio"):
                        # Save JSON and rename the audio file
                        if story_name.strip():
                            save_story_to_file(story_result, story_name)
                            saved_audio_path = f"Cuentos/{story_name}.mp3"
                            os.rename(audio_path, saved_audio_path)
                            st.success(f"Story and audio saved successfully! 📂 Location: `Cuentos/{story_name}.json` and `Cuentos/{story_name}.mp3`")
                        else:
                            st.error("Please enter a valid name for the story.")
            else:
                st.error("Failed to generate the audio. Please try again.")
        else:
            st.error("Failed to generate the story. Please try again.")