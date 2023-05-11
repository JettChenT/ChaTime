from chat import *
import streamlit as st
from fullcalendar_component import fullcalendar
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from ui import message_func

st.set_page_config(page_title="ChaTime")

with st.sidebar:
    st.title('ChaTime ⏰: Schedule your time with a chatbot')
    openai_key_inp = st.text_input("OpenAI API Key", type="password", value=st.session_state.get('OPENAI_KEY', ''))
    if openai_key_inp:
        st.session_state['OPENAI_KEY'] = openai_key_inp
    add_vertical_space(3)
    st.markdown('''
    ## About
    This app lets you schedule your time with a chatbot.
    ## Based on:
    - [Timeblok Langauage](https://github.com/JettChenT/timeblok)
    - gpt-3.5 turbo
    ''')
    add_vertical_space(3)

if 'generated' not in st.session_state:
    st.session_state['generated'] = [{
        "response": "Hi! I am ChaTime, and I can help you create and organize your schedules. Feel free to tell me what you want to do!", 
        "parsed": ""}
        ]
if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text

response_container = st.container()
colored_header(label='', description='', color_name='blue-30')
input_container = st.container()

with input_container:
    user_input = get_text()

with response_container:
    if user_input:
        key = st.session_state.get('OPENAI_KEY', '')
        if  key == '':
            st.error('Please enter your OpenAI API key in the sidebar')
        else:
            openai.api_key = key
            tmp = [c['response'] for c in st.session_state['generated']]
            resp, parsed = complete(get_prompt(st.session_state['past'], tmp, user_input))
            st.session_state['generated'].append({
                "response": resp,
                "parsed": parsed
            })
            st.session_state['past'].append(user_input)
            print(f"{parsed=}")
            if parsed:
                try:
                    compiled = compile(parsed)
                    st.session_state['last_compiled'] = compiled
                except:
                    st.error("Error compiling timeblok")
    
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message_func(st.session_state['generated'][i]['response'])
            if i==len(st.session_state['generated'])-1 and st.session_state['generated'][i]['parsed']:
                compiled = compile(st.session_state['generated'][i]['parsed'])
                if compiled is not None:
                    fullcalendar(compiled, 'timeGridDay')
                    st.download_button(
                        label="Download",
                        data=compiled,
                        file_name="exported.ics",
                )
            if i<len(st.session_state['past']):
                message_func(st.session_state['past'][i], is_user=True)
