from svg_generation import generate_svg_code, extract_svg_code, get_image_feedback
from image_processing import convert_svg_to_png, encode_image, delete_files_in_folder
from clip import get_clip_probability
import config
  
# Function to request user for text input
def get_user_input():
    user_input = input("Please describe the object you would like generated: ")
    return user_input

# Function to request user for the number of iterations
def get_number_of_iterations():
    iterations = input("Please enter the number of iterations: ")
    return iterations

def main():
    # OpenAI API Key
    api_key = config.API_KEY 

    # Conversation history
    conversation_history = []

    # Delete existing files in the folders
    delete_files_in_folder("./svg-output")
    delete_files_in_folder("./png-output")

    # Obtain user input and number of iterations
    user_input = get_user_input()
    iterations = int(get_number_of_iterations())
    print("\n")
    clip_input = ["graphic of " + user_input, "not a graphic of " + user_input]

    # Initial feedback
    feedback = "Nothing"

    # Iteration count
    first_iteration = True

    # Reinforcement learning
    for i in range(iterations):
        print(f"========Iteration {i} has started========")

        # PNG and SVG file paths
        svg_folder = f"./svg-output/vector{i}.svg"
        png_folder = f"./png-output/raster{i}.png"

        # Generate the SVG content
        svg_content, tokens_one = generate_svg_code(user_input, first_iteration, conversation_history, feedback, api_key)
        # Extract svg code from GPT output
        svg_content = extract_svg_code(svg_content)
        with open(svg_folder, 'w') as file:
            file.write(svg_content)

        # Convert SVG to PNG
        convert_svg_to_png(svg_folder, png_folder)
        # Encode the PNG to base64
        base64_image = encode_image(png_folder)
        # Get the feedback
        feedback, tokens_two = get_image_feedback(base64_image, user_input, api_key)

        # CLIP Model
        probability_value = get_clip_probability(clip_input, png_folder)

        first_iteration = False
        print("Feedback: " + feedback)
        print("Tokens used: " + str(tokens_one + tokens_two))
        print("CLIP Probability: " + str(probability_value))
        print("\n")
        

if __name__ == "__main__":
    main()
