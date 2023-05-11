import datetime
import openai
import os
import re
import streamlit as st
import shutil

try:
    import timeblok_py
except ImportError:
    import os
    import subprocess
    if shutil.which("cargo") is None:
        print("installing rust to install timebloko compiler..")
        os.system("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")
    subprocess.run(["pip", "install", "timeblok_py"])
    import timeblok_py

def set_openai_api(key, base=None):
    openai.api_key = key
    if base is not None:
        openai.api_base = base

def load_examples():
    # read all files in examples/folder
    for filename in os.listdir('./examples'):
        lines = open(os.path.join('./examples', filename)).readlines()
        prompt = tb =  ""
        flag = 0
        for l in lines:
            if l == '---\n':
                flag=0
                yield (prompt, tb)
                prompt = tb = ""
            elif l == '+++\n':
                flag=1
            elif flag: tb+=l
            else: prompt+=l

def load_prompts():
    prompt = open('./prompt.md').read()
    today = datetime.date.today().strftime("%Y-%m-%d")
    prompt += f"\nToday's date is {today}"
    messages=[{"role": "system", "content": prompt}]
    for example in load_examples():
        messages.append({"role": "user", "content": example[0]})
        messages.append({"role": "assistant", "content": example[1]})
    messages.append({"role": "user", "content": "I will create a new schedule from the following messages."})
    return messages

def get_prompt(user, generated, new):
    prompts = load_prompts()
    for i in range(len(user)):
        prompts.append({"role": "user", "content": user[i]})
        prompts.append({"role": "assistant", "content": generated[i]})  
    prompts.append({"role": "user", "content": new})
    return prompts

def parse_results(markdown):
    code_blocks = re.findall("```(timeblok)\r?\n(.*?)```", markdown, flags=re.DOTALL)
    if code_blocks:
        return code_blocks[0][1]
    return None

def complete(messages):
    completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
    content = completion.choices[0].message.content
    print(repr(content))
    parsed = parse_results(content)
    content = "\r\n"+content.replace("\n", "\r\n")
    return content, parsed


def compile(tb:str):
    # get current year, month, date
    y,m,d = datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day
    return timeblok_py.compile_with_basedate(tb, y,m,d)
