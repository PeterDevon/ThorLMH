from ollama import chat

def handle_text_input(user_input, attached_image=None):
    if attached_image:
        messages = [{'role': 'user', 'content': user_input, 'images': [attached_image]}]
    else:
        messages = [{'role': 'user', 'content': user_input}]
    
    return chat(model='gemma3:4b', messages=messages, stream=True)
