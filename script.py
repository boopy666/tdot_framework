# script.py
import os
import sys
import re
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
from classes import Description

parent_dir = os.path.dirname(current_dir)  # Move up to the 'extensions' directory
base_dir = os.path.dirname(parent_dir)  # Move up to the base 'text-generation-webui' directory
modules_path = os.path.join(base_dir, 'modules')

if modules_path not in sys.path:
    sys.path.append(modules_path)

from chat import generate_chat_prompt

# Class calls
ch = Character("Maddy", 19, 230, 62)
time = Time(ch, birth_day=6, birth_month=5, current_year=2024, current_month=6, current_day=20)
mind = Mind()
relationship = Relationship()
desc = Description(ch)

# extension parameters
params = {
    "display_name": "tdot_framework",
    "is_tab": False
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

def get_user_name(state):
    user_name = state['name1']
    return user_name

# Define the state modifier function
def state_modifier(state):

    if len(state['history']['internal']) == 1:
        weight_match = re.search(r'weight==(\d+)', state['context'])
        age_match = re.search(r'age==(\d+)', state['context'])
        height_match = re.search(r'height==(\d+)', state['context'])
        date_match = re.search(r'date==(\d{4}-\d{2}-\d{2})', state['context'])
        birth_match = re.search(r'birth==(\d{2}-\d{2})', state['context'])

        if weight_match:
            ch.set_weight(int(weight_match.group(1)))
            state['context'] = re.sub(r'weight==\d+', '', state['context'])
            state['context'] = state['context'].replace(weight_match.group(0), "").strip()
        if age_match:
            ch.set_age(int(age_match.group(1)))
            state['context'] = re.sub(r'age==\d+', '', state['context'])
            state['context'] = state['context'].replace(age_match.group(0), "").strip()
        if height_match:
            ch.set_height(int(height_match.group(1)))
            state['context'] = re.sub(r'height=\d+', '', state['context'])
            state['context'] = state['context'].replace(height_match.group(0), "").strip()
        if date_match:
            time.set_current_date(date_match.group(1), date_match.group(2), date_match.group(3))
            state['context'] = re.sub(r'date==\d{4}-\d{2}-\d{2}', '', state['context'])
            state['context'] = state['context'].replace(date_match.group(0), "").strip()
        if birth_match:
            time.set_birth_date(birth_match.group(1), birth_match.group(2))
            state['context'] = re.sub(r'birth==(\d{2}-\d{2})', state['context'])
            state['context'] = state['context'].replace(birth_match.group(0), "").strip()

    ch.set_username(get_user_name(state))

    update_state_values(state)

    state['context'] = generate_context_prompt(state['name2'], state['name1']) + "\n" + state['context']

    print(state['context'])

    return state





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
    weight_match = re.search(r'weight==(\d+)', text)
    age_match = re.search(r'age==(\d+)', text)
    height_match = re.search(r'height==(\d+)', text)
    date_match = re.search(r'date==(\d{4}-\d{2}-\d{2})', text)
    birth_match = re.search(r'birth==(\d{2}-\d{2})', text)

    if weight_match:
        ch.set_weight(int(weight_match.group(1)))
        text = re.sub(r'weight==\d+', '', text)
        text = text.replace(weight_match.group(0), "").strip()
    if age_match:
        ch.set_age(int(age_match.group(1)))
        text = re.sub(r'age==\d+', '', text)
        text = text.replace(age_match.group(0), "").strip()
    if height_match:
        ch.set_height(int(height_match.group(1)))
        text = re.sub(r'height=\d+', '', text)
        text = text.replace(height_match.group(0), "").strip()
    if date_match:
        time.set_current_date(date_match.group(1))
        text = re.sub(r'date==\d{4}-\d{2}-\d{2}', '', text)
        text = text.replace(date_match.group(0), "").strip()
    if birth_match:
        time.set_birth_date(birth_match.group(1))
        text = re.sub(r'birth==(\d{2}-\d{2})', text)
        text = text.replace(birth_match.group(0), "").strip()

    # Process end day command
    end_day_message = []
    if end_day_called:
        time.end_day()
        if time.current_month == time.birth_month and time.current_day == time.birth_day:
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

    return string


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

    def update_features(nose, eyes, lips, cheeks, face, smile):
        if nose:
            ch.set_nose(nose)
        if eyes:
            ch.set_eyes(eyes)
        if lips:
            ch.set_lips(lips)
        if cheeks:
            ch.set_cheeks(cheeks)
        if face:
            ch.set_face(face)
        if smile:
            ch.set_smile(smile)
        return f"Character features updated: {ch.get_name()}", "", "", "", "", "", ""

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
        return update, update, update, update, update, update, update, update, update, update, update, update, update, update, update, update

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
                    eye_input = gr.Dropdown(label="Eye Shape", choices=[feature for d in Character.FACIAL_FEATURES if d["type"] == "Eyes" for feature in d["features"]])
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
                    eye_color_input, nose_input, eye_input, lips_input, cheeks_input, face_input, smile_input,
                    update_features_button, skin_input, hair_input, update_appearance_button
                ]
            )

            update_character_button.click(
                fn=update_character,
                inputs=[name_input, age_input, weight_input, height_input],
                outputs=[character_output, name_input, age_input, weight_input, height_input]
            )

            update_features_button.click(
                fn=update_features,
                inputs=[nose_input, eye_input, lips_input, cheeks_input, face_input, smile_input],
                outputs=[features_output, nose_input, eye_input, lips_input, cheeks_input, face_input, smile_input]
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