from transformers import CLIPProcessor, CLIPModel
from PIL import Image

def get_clip_probability(clip_input, png_folder):
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32") 

    clip_image = Image.open(png_folder)
    inputs = processor(text=clip_input, images=clip_image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    # Raw Similarity Score
    logits_per_image = outputs.logits_per_image 
    # Probability
    probability_tensor = logits_per_image.softmax(dim=1) 
    probability_value = probability_tensor[0][0].item()

    return probability_value
