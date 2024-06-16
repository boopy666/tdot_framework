# script.py
import os
import sys
import gradio as gr
# Find the path to the 'modules' directory relative to the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the script directory to the Python path
sys.path.append(current_dir)

# Now import the 'classes' module
from classes import Character
from classes import Time
from classes import Mind
from classes import Relationship

parent_dir = os.path.dirname(current_dir)  # Move up to the 'extensions' directory
base_dir = os.path.dirname(parent_dir)  # Move up to the base 'text-generation-webui' directory
modules_path = os.path.join(base_dir, 'modules')

if modules_path not in sys.path:
    sys.path.append(modules_path)

from chat import generate_chat_prompt

ch = Character("Maddy", 19, 300, 67)
time = Time(ch, birth_day=6, birth_month=5)
mind = Mind()
relationship = Relationship()

# extension parameters
params = {
    "display_name": "tdot_framework",
    "is_tab": False
}

UI = {
    "activate_stats": True
}


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
Description("{name} loves indulging in food" + "{name} enjoys teasing others with her growing curves" + "{name} wants to satisfy her cravings" + "{name} uses her playful nature to captivate others" + "{name} is oblivious to {name}'s motives" + "{name} follows her impulses without understanding the consequences")
}}]"""

    return string_block1


# Define the state modifier function
def state_modifier(state):

    if len(state['history']['internal']) == 1: #NEW CHAT
        print()

    state['context'] = generate_context_prompt(state['name2'], state['name1']) + "\n" + state['context']

    print(state['context'])

    return state

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
        if ch.current_date.month == 4 and ch.current_date.day == 16:
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
        visible_text += "\n".join(food_message)


    return text, visible_text

def output_modifier(string, state, is_chat=True):
    """
    Modifies the LLM output before it gets presented.

    In chat mode, the modified version goes into history['visible'],
    and the original version goes into history['internal'].
    """
    if len(state['history']['internal']) != 1:
        relationship.calculate_sentiment_score(string)

    return string


# Assuming `ch` is defined somewhere else in your code
def weight_stat(weight_adjustment=None):
    if weight_adjustment is not None:
        ch.set_weight(weight_adjustment)
    return ch.get_weight()

def ui():
    def update_character(name, age, weight, height, eye_color, nose, lips, cheeks, face, smile, hair, skin):
        ch.set_name(name)
        ch.set_age(age)
        ch.set_weight(weight)
        ch.set_height(height)
        ch.set_eye_color(eye_color)
        ch.set_nose(nose)
        ch.set_lips(lips)
        ch.set_cheeks(cheeks)
        ch.set_face(face)
        ch.set_smile(smile)
        ch.set_hair(hair)
        ch.set_skin(skin)
        return f"Character updated: {ch.get_name()}"

    def toggle_visibility(activate_stats):
        update = gr.update(visible=activate_stats)
        return update, update, update, update, update, update, update, update, update, update, update, update, update

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

                with gr.Column():
                    eye_color_input = gr.Dropdown(label="Eye Color", choices=Character.EYE_COLORS)
                    nose_input = gr.Dropdown(label="Nose", choices=[feature for d in Character.FACIAL_FEATURES if d["type"] == "Nose" for feature in d["features"]])
                    lips_input = gr.Dropdown(label="Lips", choices=[feature for d in Character.FACIAL_FEATURES if d["type"] == "Lips" for feature in d["features"]])
                    cheeks_input = gr.Dropdown(label="Cheeks", choices=[feature for d in Character.FACIAL_FEATURES if d["type"] == "Cheeks" for feature in d["features"]])
                    face_input = gr.Dropdown(label="Face", choices=[feature for d in Character.FACIAL_FEATURES if d["type"] == "Face" for feature in d["features"]])
                    smile_input = gr.Dropdown(label="Smile", choices=[feature for d in Character.FACIAL_FEATURES if d["type"] == "Smile" for feature in d["features"]])

                with gr.Column():
                    skin_input = gr.Dropdown(label="Skin Tone", choices=Character.SKIN_TONES)
                    hair_input = gr.Dropdown(label="Hair Color", choices=Character.HAIR_COLORS)

            update_button = gr.Button("Update Character")
            output_text = gr.Textbox(label="Output")

            character_activate.change(
                fn=toggle_visibility,
                inputs=character_activate,
                outputs=[
                    name_input, age_input, weight_input, height_input,
                    eye_color_input, nose_input, lips_input, cheeks_input,
                    face_input, smile_input, skin_input, hair_input, update_button
                ]
            )

            update_button.click(
                fn=update_character,
                inputs=[
                    name_input, age_input, weight_input, height_input,
                    eye_color_input, nose_input, lips_input, cheeks_input,
                    face_input, smile_input, skin_input, hair_input
                ],
                outputs=output_text
            )

        commit_button = gr.Button("Commit")
        commit_button.click(fn=lambda: None, inputs=None, outputs=None)

    return demo

if __name__ == '__main__':
    ui = ui()
    ui.launch()
