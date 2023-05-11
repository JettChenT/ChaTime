import streamlit as st

# Copied from https://github.com/kaarthik108/snowChat/blob/main/utils/snowchat_ui.py

def message_func(text, is_user=False):
    '''
    This function is used to display the messages in the chatbot UI.
    
    Parameters:
    text (str): The text to be displayed.
    is_user (bool): Whether the message is from the user or the chatbot.
    key (str): The key to be used for the message.
    avatar_style (str): The style of the avatar to be used.
    '''
    if is_user:
        avatar_url = "https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortFlat&accessoriesType=Prescription01&hairColor=Auburn&facialHairType=BeardLight&facialHairColor=Black&clotheType=Hoodie&clotheColor=PastelBlue&eyeType=Squint&eyebrowType=DefaultNatural&mouthType=Smile&skinColor=Tanned"
        message_alignment = "flex-end"
        message_bg_color = "linear-gradient(135deg, #00B2FF 0%, #006AFF 100%)"
        avatar_class = "user-avatar"
        st.write(f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                    <div style="background: {message_bg_color}; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%;">
                        {text}
                    </div>
                            <img src="{avatar_url}" class="{avatar_class}" alt="avatar" style="width:40px; height:40px"/>

                </div>
                """, unsafe_allow_html=True)  
    else:
        avatar_url = "https://avataaars.io/?avatarStyle=Transparent&topType=LongHairFro&accessoriesType=Blank&hairColor=BrownDark&facialHairType=Blank&clotheType=BlazerShirt&eyeType=Default&eyebrowType=Default&mouthType=Default&skinColor=Light"
        message_alignment = "flex-start"
        message_bg_color = "#71797E"
        avatar_class = "bot-avatar"
        st.write(f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                    <img src="{avatar_url}" class="{avatar_class}" alt="avatar" style="width:40px; height:40px"/>
                    <div style="background: {message_bg_color}; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%;">
                        {text} \n </div>
                </div>
                """, unsafe_allow_html=True)  