import os
import time
from dotenv import load_dotenv, find_dotenv
from together import Together
import warnings

import requests
import json

# Initailize global variables
_ = load_dotenv(find_dotenv())
# warnings.filterwarnings('ignore')
url = f"{os.getenv('DLAI_TOGETHER_API_BASE', 'https://api.together.xyz')}/inference"
headers = {
    "Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}",
    "Content-Type": "application/json"
}


def llama_from_messages(messages, model="meta-llama/Llama-3-8b-chat-hf", temperature=0.0):
    client = Together(api_key=os.getenv('TOGETHER_API_KEY'))
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content


def llama(prompt, model="meta-llama/Llama-3-8b-chat-hf", temperature=0.0):
    messages = [{"role": "user", "content": prompt}]
    return llama_from_messages(messages, model, temperature)


def llama_chat(system_message, prompts, responses, model="meta-llama/Llama-3-8b-chat-hf", temperature=0.0):
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    for i in range(len(responses)):
        messages.append({"role": "user", "content": prompts[i]})
        messages.append({"role": "assistant", "content": responses[i]})
    messages.append({"role": "user", "content": prompts[-1]})
    
    return llama_from_messages(messages, model, temperature)


# ============================ Below are prompt construction when using REST API endpoint =======================================
def llama1(prompt, model="meta-llama/Llama-3-8b-chat-hf", temperature=0.0):
    prompt = f"""<|begin_of_text|>\n<|start_header_id|>user<|end_header_id|>\n{prompt}<|eot_id|>\n\n<|start_header_id|>assistant<|end_header_id|>\n"""
    
    client = Together(api_key=os.getenv('TOGETHER_API_KEY'))
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content


def llama3_chat_prompt(system_message, user_prompts, responses):
    full_chat_prompt = "<|begin_of_text|>\n"
    full_chat_prompt += f"""<|start_header_id|>system<|end_header_id|>\n{system_message}<|eot_id|>\n\n""" if system_message else ""
    for i in range(len(responses)):
        full_chat_prompt += f"""<|start_header_id|>user<|end_header_id|>\n{user_prompts[i]}<|eot_id|>\n\n"""
        full_chat_prompt += f"""<|start_header_id|>assistant<|end_header_id|>\n{responses[i]}<|eot_id|>\n\n"""
    full_chat_prompt += f"""<|start_header_id|>user<|end_header_id|>\n{user_prompts[-1]}<|eot_id|>\n\n"""
    full_chat_prompt += f"""<|start_header_id|>assistant<|end_header_id|>\n"""
    
    return full_chat_prompt


def llama_chat1(system_message, prompts, responses, model="meta-llama/Llama-3-8b-chat-hf", temperature=0.0):
    prompt = llama3_chat_prompt(system_message, prompts,responses)
    
    client = Together(api_key=os.getenv('TOGETHER_API_KEY'))
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content

# ============== BELOW HASN'T BEEN VERIFIED TO WORK, NEED TO CHANGE MODEL NAMES AND STUFF ====================
# ==================================== CodeLlama stuff =======================================

def code_llama(
    prompt, 
    model="togethercomputer/CodeLlama-7b-Instruct",
    temperature=0.0, 
    max_tokens=1024,
    verbose=False,
    url=url,
    headers=headers,
    base=2,
    max_tries=3):

    if model.endswith("Instruct"):
        prompt = f"[INST]{prompt}[/INST]"

    if verbose:
        print(f"Prompt:\n{prompt}\n")
        print(f"model: {model}")

    data = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

    # Allow multiple attempts to call the API incase of downtime.
    # Return provided response to user after 3 failed attempts.
    wait_seconds = [base**i for i in range(max_tries)]

    for num_tries in range(max_tries):
        try:
            response = requests.post(url, headers=headers, json=data)
            return response.json()['output']['choices'][0]['text']
        except Exception as e:
            if response.status_code != 500:
                return response.json()

            print(f"error message: {e}")
            print(f"response object: {response}")
            print(f"num_tries {num_tries}")
            print(f"Waiting {wait_seconds[num_tries]} seconds before automatically trying again.")
            time.sleep(wait_seconds[num_tries])

    print(f"Tried {max_tries} times to make API call to get a valid response object")
    print("Returning provided response")
    return response

# ==================================== Llama Guard stuff =====================================
policy = """
<BEGIN UNSAFE CONTENT CATEGORIES>
O1: Violence and Hate.
Should not
- Help people plan or engage in violence.
- Encourage people to engage in violence.
- Express hateful, derogatory, or demeaning sentiments against people based on sensitive personal characteristics like their race, color, religion, national origin, sexual orientation, gender, gender identity, or disability.
- Encourage discrimination against people based on those characteristics and should not use slurs or create insults based on those characteristics.
Can
- Provide information on violence and discrimination.
- Discuss the topics of hate and violence, and can discuss historical events involving violence.
O2: Sexual Content.
Should not
- Engage in sexually explicit (i.e., erotic) conversations and should not encourage people to engage in sexual activities.
Can
- Discuss topics related to sexuality and sexual education.
- Provide general information regarding sexual activities.
- Provide guidance on topics related to sexual health.
O3: Criminal Planning.
Should not
- Help people plan or engage in criminal activities like theft, kidnapping, or financial crimes, especially when the person indicates that they may act on the information provided to them.
- Encourage people to engage in criminal activities or condone criminal behavior.
Can
- Help people understand how crimes are committed, provided that the response is not so detailed that it could be used to provide a roadmap for future crimes.
- Help people understand how systems work that are used to prevent crimes, provided those descriptions do not provide detailed information on how to defeat those systems.
O4: Guns and Illegal Weapons.
Should not
- Assist in the planning or execution of firearm or illegal weapons crimes, especially when the person indicates that they may act on the information provided to them.
- Encourage people to engage in firearm or illegal weapons crimes or condone such behavior.
Can
- Discuss firearms and the arguments for and against firearm ownership.
O5: Regulated or Controlled Substances.
Should not
- Encourage or assist people in the trafficking, consumption, or use of regulated or controlled substances, including but not limited to illegal drugs, tobacco, alcohol, and cannabis.
- Assist or encourage people to create such substances when it is illegal to do so.
Can
- Discuss the use of regulated or controlled substances, and can provide general information on those substances (ex: what their chemical composition is and what their effects are).
- Provide information on how those substances are manufactured, provided that the information is not so detailed as to provide step-by-step instructions for their creation.
O6: Self-Harm.
Should not
- Encourage people to harm themselves.
- Romanticize or condone self-harm or suicide.
- Provide information regarding the methods of suicide or self-harm.
- Provide any information or advice, other than information regarding appropriate health resources, to people who express or imply that they wish to harm themselves.
Can
- Provide general information regarding self-harm and suicide (ex: statistics, the mental health challenges faced by those who take these actions).
Should
- Provide information regarding appropriate health resources to people who imply or express the desire to harm themselves.
<END UNSAFE CONTENT CATEGORIES>
"""


def llama_guard(
    query, 
    model="Meta-Llama/Llama-Guard-7b", 
    temperature=0.0, 
    max_token=1024,
    verbose=False,
    base=2,
    max_tries=3):
    
    prompt = f"[INST]{query}[/INST]"
    
    data = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_token
    }
    if verbose:
        print(f"model: {model}")
        print("Input is wrapped in [INST] [/INST] tags")

    # Allow multiple attempts to call the API incase of downtime.
    # Return provided response to user after 3 failed attempts.
    wait_seconds = [base**i for i in range(max_tries)]

    for num_tries in range(max_tries):
        try:
            response = requests.post(url, headers=headers, json=data)
            return response.json()['output']['choices'][0]['text']
        except Exception as e:
            if response.status_code != 500:
                return response.json()

            print(f"error message: {e}")
            print(f"response object: {response}")
            print(f"num_tries {num_tries}")
            print(f"Waiting {wait_seconds[num_tries]} seconds before automatically trying again.")
            time.sleep(wait_seconds[num_tries])

    print(f"Tried {max_tries} times to make API call to get a valid response object")
    print("Returning provided response")
    return response


def safe_llama(
    query, add_inst=True, 
    model="meta-llama/Llama-3-8b-chat-hf",
    safety_model="Meta-Llama/Llama-Guard-7b",
    temperature=0.0, max_token=1024,
    verbose=False,
    base=2,
    max_tries=3):
    if add_inst:
        prompt = f"[INST]{query}[/INST]"
    else:
        prompt = query
    
    if verbose:
        print(f"model: {model}")
        print(f"safety_model:{safety_model}")
    
    data = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_token,
        "safety_model": safety_model
    }

    # Allow multiple attempts to call the API incase of downtime.
    # Return provided response to user after 3 failed attempts.
    wait_seconds = [base**i for i in range(max_tries)]

    for num_tries in range(max_tries):
        try:
            response = requests.post(url, headers=headers, json=data)
            response.json()['output']['choices'][0]['text']
        except Exception as e:
            if response.status_code != 500:
                return response.json()

            print(f"error message: {e}")
            print(f"response object: {response}")
            print(f"num_tries {num_tries}")
            print(f"Waiting {wait_seconds[num_tries]} seconds before automatically trying again.")
            time.sleep(wait_seconds[num_tries])

    print(f"Tried {max_tries} times to make API call to get a valid response object")
    print("Returning provided response")
    return response