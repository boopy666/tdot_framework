# script.py
import os
import sys
import re
import gradio as gr
import simpleaudio as sa
import requests
import json
import base64
import io
import wave
# Find the path to the 'modules' directory relative to the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the script directory to the Python path
sys.path.append(current_dir)

# Now import the 'classes' module
from classes import Character
from classes import Time
from classes import Mind
from classes import Relationship
from classes import Description

parent_dir = os.path.dirname(current_dir)  # Move up to the 'extensions' directory
base_dir = os.path.dirname(parent_dir)  # Move up to the base 'text-generation-webui' directory
modules_path = os.path.join(base_dir, 'modules')

if modules_path not in sys.path:
    sys.path.append(modules_path)

from chat import generate_chat_prompt

# Class calls
ch = Character("Maddy", 19, 300, 67)
time = Time(ch, birth_day=6, birth_month=5)
mind = Mind()
relationship = Relationship()
desc = Description(ch)

# extension parameters
params = {
    "display_name": "tdot_framework",
    "is_tab": False
}

tts_params = {
    "api_key": "",
    "is_active": False,
    "last_response_chunks": []
}

# Global variables to store slider values
max_new_tokens = 1028
temperature = 1
top_p = 0.9
min_p = 0


def generate_context_prompt(name, user):
    height = ch.calculate_height_feet()

    # Define the string block
    string_block1 = f"""[character("{name}")
{{
Species("Human")
Age("{ch.get_age()} years old")
Weight("{ch.get_weight()} lbs")
Obesity("BMI: {ch.calculate_bmi()}" + "Class: {ch.calculate_bmi_class()}")
Features("{ch.hair} hair" + "{ch.eye_color} eyes" + "{ch.skin} skin tone" + "{ch.nose}" + "{ch.eye_shape}" + "{ch.lips}" + "{ch.cheeks}" + "{ch.face}" + "{ch.smile}")
Height("{ch.calculate_height_cm()} cm" + "{int(height[0])} feet {height[1]} inches tall")
Body("Chest size {int(ch.get_chest())} inches around" + "Waist size {int(ch.get_waist())} inches around" + "Hips size {int(ch.get_hips())} inches around")
Clothing("Wears size {ch.get_clothing_size()} clothing")
Mind({mind.formatted_mind_traits()})
Personality({mind.formatted_personality_traits()})
Mood("{mind.get_mood()}")
Relationship("Relationship status with {user} is: {relationship.calculate_relationship()}")
Loves({mind.formatted_loves()})
Hates({mind.formatted_hates()})
Time("Today's date is {time.get_formatted_current_date()}" + "{name}'s birthday is {time.get_formatted_birth_date()}" + "In {time.get_day()} days {name} has gained {ch.get_weight_diff()} lbs")
Description({desc.formatted_all()})
}}]"""

    return string_block1


# Define the state modifier function
def state_modifier(state):

    ch.set_username(state['name1'])

    update_state_values(state)

    state['context'] = generate_context_prompt(state['name2'], state['name1']) + "\n" + state['context']

    print(state['context'])

    return state

def get_user_name(state):
    user_name = state['name1']
    return user_name

# Define a function to update the state values based on slider inputs
def update_state_values(state):
    global max_new_tokens, temperature, top_p, min_p

    state['max_new_tokens'] = max_new_tokens
    state['temperature'] = temperature
    state['top_p'] = top_p
    state['min_p'] = min_p


def chat_input_modifier(text, visible_text, state):
    """
    Modifies the user input string in chat mode (visible_text).
    You can also modify the internal representation of the user
    input (text) to change how it will appear in the prompt.
    """
    food_matches = re.findall(r"\{([^}]+):(\d+)\}", text)
    end_day_called = "==END_DAY==" in text
    relationship.calculate_sentiment_score(text)

    # Process end day command
    end_day_message = []
    if end_day_called:
        time.end_day()
        if time.current_date.month == 4 and time.current_date.day == 16:
            end_day_message.append(
                f"\n*It's the start of a new day... And it's {ch.name}'s birthday! You are now {ch.age}!*\n")
        else:
            end_day_message.append("\n*It's the start of a new day!*\n")
        visible_text = text.replace("==END_DAY==", "").strip()
        text = text.replace("==END_DAY==", "").strip()

    food_messages = []

    for food_item, calories in food_matches:
        ch.add_calories(int(calories))
        fullness_status = ch.calculate_fullness()
        food_messages.append(
            f"\n*[{ch.name} just ate {food_item}*\n*After eating this, {ch.name} is feeling {fullness_status}.*]")

    if end_day_message:
        text += "\n".join(end_day_message)
        visible_text += "\n".join(end_day_message)

    if food_messages:
        text += "\n".join(food_messages)
        visible_text += "\n".join(food_messages)


    return text, visible_text

def output_modifier(string, state, is_chat=True):
    """
    Modifies the LLM output before it gets presented.

    In chat mode, the modified version goes into history['visible'],
    and the original version goes into history['internal'].
    """
    if len(state['history']['internal']) != 1:
        relationship.calculate_sentiment_score(string)

    api_key = tts_params.get('api_key', '')
    is_active = tts_params.get('is_active', False)

    if is_active and api_key:
        try:
            print("Fetching voices...")
            voices = fetch_voices(api_key)
            if voices:
                print("Voices fetched successfully.")
                print("Synthesizing speech...")
                tts_params["last_response_chunks"] = synthesize_speech_chunks(api_key, string)
                print("Speech synthesized and played successfully.")
            else:
                print("No voices found.")
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print("TTS functionality is not active or API key not provided.")

    return string


def fetch_voices(api_key):
    url = 'https://api.inworld.ai/tts/v1alpha/voices'
    headers = {
        'Authorization': 'Basic ' + api_key
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching voices: {str(e)}")


def synthesize_speech_chunks(api_key, text):
    # Sanitize the text
    text = sanitize_text(text)
    # Split the text into chunks of approximately 500 characters
    chunks = split_text_into_chunks(text, 100)

    audio_chunks = []
    for chunk in chunks:
        audio_chunk = synthesize_speech(api_key, chunk)
        if audio_chunk is not None:
            audio_chunks.append(audio_chunk)

    return audio_chunks


def split_text_into_chunks(text, chunk_size):
    # Split the text into sentences based on "!", "?", or "."
    sentences = re.split(r'(?<=[!?.])\s+', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def sanitize_text(text):
    # Remove text between asterisks or square brackets
    text = re.sub(r'\*[^*]*\*', '', text)
    text = re.sub(r'\[[^]]*\]', '', text)

    # Remove emoticons
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)

    # Unescape the input text
    print(f"\n\n\nDebug pre unescape: {text}\n\n\n")
    # Replace specific escaped characters with their original form
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&quot;', '"', text)
    text = re.sub(r'&#39;', "'", text)
    text = re.sub(r'&#x27;', "'", text)
    text = re.sub(r'&#33;', '!', text)
    text = re.sub(r'&#63;', '?', text)
    text = re.sub(r'&#44;', ',', text)
    text = re.sub(r'&#46;', '.', text)
    text = re.sub(r'&#58;', ':', text)
    text = re.sub(r'&#59;', ';', text)
    text = re.sub(r'&#40;', '(', text)
    text = re.sub(r'&#41;', ')', text)
    text = re.sub(r'&#91;', '[', text)
    text = re.sub(r'&#93;', ']', text)
    text = re.sub(r'&#123;', '{', text)
    text = re.sub(r'&#125;', '}', text)
    print(f"\n\n\nDebug POST unescape: {text}\n\n\n")

    return text


def synthesize_speech(api_key, text):
    print(f"\n\n\nCurrent chunk: {text}\n\n\n")

    url = 'https://api.inworld.ai/tts/v1alpha/text:synthesize'
    headers = {
        'Authorization': 'Basic ' + api_key,
        'Content-Type': 'application/json'
    }
    payload = {
        'input': {
            'text': json.dumps(str(text))
        },
        'voice': {
            'name': 'Rachel'
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()

        content_type = response.headers.get('Content-Type')
        if content_type == 'application/json':
            try:
                response_data = response.json()
                audio_content = response_data['result']['audioContent']
                audio_data = base64.b64decode(audio_content)
                play_audio(audio_data)
                return audio_data
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error parsing JSON response: {str(e)}")
                print(f"Response content: {response.text}")
                return None
        else:
            # Assuming the response content is the audio data
            audio_data = response.content
            return audio_data

    except requests.exceptions.RequestException as e:
        print(f"Error synthesizing speech: {str(e)}")
        return None
    except Exception as e:
        print(f"Error processing audio: {str(e)}")
        return None


def play_audio(audio_data):

    # Create a WAV file in memory from the audio data
    wav_file = io.BytesIO()
    with wave.open(wav_file, 'wb') as wave_writer:
        wave_writer.setnchannels(1)  # Mono audio
        wave_writer.setsampwidth(2)  # 16-bit audio
        wave_writer.setframerate(24000)  # Sampling rate of 24000Hz
        wave_writer.writeframes(audio_data)

    # Rewind the WAV file
    wav_file.seek(0)

    # Load the WAV file using simpleaudio
    wave_obj = sa.WaveObject.from_wave_file(wav_file)

    # Play the audio
    play_obj = wave_obj.play()
    play_obj.wait_done()


def replay_last_response():
    last_response_chunks = tts_params.get("last_response_chunks", [])
    for chunk in last_response_chunks:
        if chunk is not None:
            wav_file = io.BytesIO(chunk)
            wave_obj = sa.WaveObject.from_wave_file(wav_file)
            play_obj = wave_obj.play()
            play_obj.wait_done()


def ui():
    global max_new_tokens, temperature, top_p, min_p

    def update_character(name, age, weight, height):
        if name:
            ch.set_name(name)
        if age:
            ch.set_age(age)
        if weight:
            ch.set_weight(weight)
        if height:
            ch.set_height(height)
        return f"Character updated: {ch.get_name()}", "", "", "", ""

    def update_features(nose, lips, cheeks, face, smile):
        if nose:
            ch.set_nose(nose)
        if lips:
            ch.set_lips(lips)
        if cheeks:
            ch.set_cheeks(cheeks)
        if face:
            ch.set_face(face)
        if smile:
            ch.set_smile(smile)
        return f"Character features updated: {ch.get_name()}", "", "", "", "", ""

    def update_appearance(eye_color, hair, skin):
        if eye_color:
            ch.set_eye_color(eye_color)
        if hair:
            ch.set_hair(hair)
        if skin:
            ch.set_skin(skin)
        return f"Character appearance updated: {ch.get_name()}", "", "", ""

    def update_time(current_day, current_month, current_year, birth_day, birth_month, game_day):
        if current_day & current_month & current_year:
            time.set_current_day(current_year, current_month, current_day)
        if birth_day & birth_month:
            time.set_birth_date(birth_day, birth_month)
        if game_day:
            time.set_day(game_day)
        return f"Time updated: {ch.get_name()}", "", "", ""

    def toggle_visibility(activate_stats):
        update = gr.update(visible=activate_stats)
        return update, update, update, update, update, update, update, update, update, update, update, update, update, update, update

    def toggle_time_visibility(activate_stats):
        update = gr.update(visible=activate_stats)
        return update, update, update, update, update, update, update

    with gr.Blocks() as demo:
        with gr.Tab(label="Character"):
            character_activate = gr.Checkbox(label="Activate Character Stats", value=False)

            with gr.Row():
                with gr.Column():
                    with gr.Row():
                        name_input = gr.Textbox(label="Name")
                        age_input = gr.Number(label="Age")
                    with gr.Row():
                        weight_input = gr.Number(label="Weight")
                        height_input = gr.Number(label="Height")
                    update_character_button = gr.Button("Update Character")
                    character_output = gr.Textbox(label="Character Output")

                with gr.Column():
                    eye_color_input = gr.Dropdown(label="Eye Color", choices=Character.EYE_COLORS)
                    nose_input = gr.Dropdown(label="Nose", choices=[feature for d in Character.FACIAL_FEATURES if d["type"] == "Nose" for feature in d["features"]])
                    lips_input = gr.Dropdown(label="Lips", choices=[feature for d in Character.FACIAL_FEATURES if d["type"] == "Lips" for feature in d["features"]])
                    cheeks_input = gr.Dropdown(label="Cheeks", choices=[feature for d in Character.FACIAL_FEATURES if d["type"] == "Cheeks" for feature in d["features"]])
                    face_input = gr.Dropdown(label="Face", choices=[feature for d in Character.FACIAL_FEATURES if d["type"] == "Face" for feature in d["features"]])
                    smile_input = gr.Dropdown(label="Smile", choices=[feature for d in Character.FACIAL_FEATURES if d["type"] == "Smile" for feature in d["features"]])
                    update_features_button = gr.Button("Update Features")
                    features_output = gr.Textbox(label="Features Output")

                with gr.Column():
                    skin_input = gr.Dropdown(label="Skin Tone", choices=Character.SKIN_TONES)
                    hair_input = gr.Dropdown(label="Hair Color", choices=Character.HAIR_COLORS)
                    update_appearance_button = gr.Button("Update Appearance")
                    appearance_output = gr.Textbox(label="Appearance Output")

            character_activate.change(
                fn=toggle_visibility,
                inputs=character_activate,
                outputs=[
                    name_input, age_input, weight_input, height_input, update_character_button,
                    eye_color_input, nose_input, lips_input, cheeks_input, face_input, smile_input, update_features_button,
                    skin_input, hair_input, update_appearance_button
                ]
            )

            update_character_button.click(
                fn=update_character,
                inputs=[name_input, age_input, weight_input, height_input],
                outputs=[character_output, name_input, age_input, weight_input, height_input]
            )

            update_features_button.click(
                fn=update_features,
                inputs=[nose_input, lips_input, cheeks_input, face_input, smile_input],
                outputs=[features_output, nose_input, lips_input, cheeks_input, face_input, smile_input]
            )

            update_appearance_button.click(
                fn=update_appearance,
                inputs=[eye_color_input, hair_input, skin_input],
                outputs=[appearance_output, eye_color_input, hair_input, skin_input]
            )

        with gr.Tab("Mind"):
            mind_activate = gr.Checkbox(label="Activate Mind Stats", value=False)

            with gr.Row():
                moods_dropdown = gr.Dropdown(label="Moods", choices=mind.moods)
                positive_traits_dropdown = gr.Dropdown(label="Positive Mind Traits", choices=mind.positive_mind_traits)
                negative_traits_dropdown = gr.Dropdown(label="Negative Mind Traits", choices=mind.negative_mind_traits)

            with gr.Row():
                traits_dropdown = gr.Dropdown(label="Personality Traits", choices=mind.traits)
                loves_dropdown = gr.Dropdown(label="Loves", choices=mind.loves)
                hates_dropdown = gr.Dropdown(label="Hates", choices=mind.hates)

            with gr.Row():
                add_button = gr.Button("Add")
                remove_button = gr.Button("Remove")

            mind_output = gr.Textbox(label="Mind Output")

            def update_mind(add, remove, moods, positive_traits, negative_traits, traits, loves, hates):
                if add:
                    if moods:
                        mind.moods.append(moods)
                    if positive_traits:
                        mind.positive_mind_traits.append(positive_traits)
                    if negative_traits:
                        mind.negative_mind_traits.append(negative_traits)
                    if traits:
                        mind.traits.append(traits)
                    if loves:
                        mind.loves.append(loves)
                    if hates:
                        mind.hates.append(hates)
                if remove:
                    if moods and moods in mind.moods:
                        mind.moods.remove(moods)
                    if positive_traits and positive_traits in mind.positive_mind_traits:
                        mind.positive_mind_traits.remove(positive_traits)
                    if negative_traits and negative_traits in mind.negative_mind_traits:
                        mind.negative_mind_traits.remove(negative_traits)
                    if traits and traits in mind.traits:
                        mind.traits.remove(traits)
                    if loves and loves in mind.loves:
                        mind.loves.remove(loves)
                    if hates and hates in mind.hates:
                        mind.hates.remove(hates)

                output = f"Moods: {', '.join(mind.moods)}\n"
                output += f"Positive Mind Traits: {', '.join(mind.positive_mind_traits)}\n"
                output += f"Negative Mind Traits: {', '.join(mind.negative_mind_traits)}\n"
                output += f"Personality Traits: {', '.join(mind.traits)}\n"
                output += f"Loves: {', '.join(mind.loves)}\n"
                output += f"Hates: {', '.join(mind.hates)}"

                return output, "", "", "", "", "", ""

            mind_activate.change(
                fn=toggle_visibility,
                inputs=mind_activate,
                outputs=[
                    moods_dropdown, positive_traits_dropdown, negative_traits_dropdown,
                    traits_dropdown, loves_dropdown, hates_dropdown,
                    add_button, remove_button
                ]
            )

            add_button.click(
                fn=update_mind,
                inputs=[
                    gr.State(True), gr.State(False),
                    moods_dropdown, positive_traits_dropdown, negative_traits_dropdown,
                    traits_dropdown, loves_dropdown, hates_dropdown
                ],
                outputs=[
                    mind_output,
                    moods_dropdown, positive_traits_dropdown, negative_traits_dropdown,
                    traits_dropdown, loves_dropdown, hates_dropdown
                ]
            )

            remove_button.click(
                fn=update_mind,
                inputs=[
                    gr.State(False), gr.State(True),
                    moods_dropdown, positive_traits_dropdown, negative_traits_dropdown,
                    traits_dropdown, loves_dropdown, hates_dropdown
                ],
                outputs=[
                    mind_output,
                    moods_dropdown, positive_traits_dropdown, negative_traits_dropdown,
                    traits_dropdown, loves_dropdown, hates_dropdown
                ]
            )

        with gr.Tab(label="Time"):
            time_activate = gr.Checkbox(label="Activate Time Stats", value=False)

            with gr.Column():
                with gr.Row():
                    current_year_input = gr.Number(label="Current year", Min=0)
                    current_month_input = gr.Number(label="Current month", Min=1, Max=12)
                    current_day_input = gr.Number(label="Current day", Min=1, Max=31)

            with gr.Column():
                with gr.Row():
                    birth_month_input = gr.Number(label="Birth month", Min=1, Max=12)
                    birth_day_input = gr.Number(label="Birth Day", Min=0, Max=31)

            with gr.Column():
                game_day_input = gr.Number(label="Update Number of Game Days", Min=0)

            update_date_button = gr.Button(label="Update Time")
            update_date_output = gr.Textbox(label="Time Output")

            time_activate.change(
                fn=toggle_time_visibility,
                inputs=time_activate,
                outputs=[
                    current_year_input, current_month_input, current_day_input,
                    birth_month_input, birth_day_input, game_day_input
                ]
            )

            update_date_button.click(
                fn=update_time,
                inputs=[
                    current_year_input, current_month_input, current_day_input,
                    birth_month_input, birth_day_input, game_day_input
                ],
                outputs=[
                    update_date_output, current_day_input, current_month_input, current_year_input,
                    birth_month_input, birth_day_input, game_day_input
                ]
            )

        with gr.Tab(label="Inworld"):
            with gr.Row():
                api_key = gr.Textbox(
                    label="Inworld API Key",
                    value=tts_params["api_key"],
                    placeholder="Enter your API key here..."
                )
                is_active = gr.Checkbox(label="Activate TTS", value=tts_params["is_active"])
            with gr.Row():
                submit_button = gr.Button("Commit Settings")
                replay_button = gr.Button("Replay Last Response")

        def commit_settings(api_key_value, is_active_value):
            tts_params["api_key"] = api_key_value
            tts_params["is_active"] = is_active_value
            print("Settings committed successfully.")

        submit_button.click(
            fn=commit_settings,
            inputs=[api_key, is_active],
            outputs=[]
        )

        replay_button.click(
            fn=replay_last_response,
            inputs=[],
            outputs=[]
        )

        with gr.Tab(label="Parameters"):
            with gr.Row():
                max_new_tokens_slider = gr.Slider(minimum=1, maximum=4096, step=1, label="Max New Tokens",
                                                  value=max_new_tokens)
                temperature_slider = gr.Slider(minimum=0, maximum=5, step=0.05, label="Temperature", value=temperature)

            with gr.Row():
                top_p_slider = gr.Slider(minimum=0, maximum=1, step=0.01, label="Top P", value=top_p)
                min_p_slider = gr.Slider(minimum=0, maximum=1, step=0.01, label="Min P", value=min_p)

            def update_globals(max_new_tokens_value, temperature_value, top_p_value, min_p_value):
                global max_new_tokens, temperature, top_p, min_p
                max_new_tokens = max_new_tokens_value
                temperature = temperature_value
                top_p = top_p_value
                min_p = min_p_value

            with gr.Row():
                commit_button = gr.Button(value="Commit Changes")

            commit_button.click(update_globals,
                                inputs=[max_new_tokens_slider, temperature_slider, top_p_slider, min_p_slider])

    return demo

if __name__ == '__main__':
    ui = ui()
    ui.launch()