import os
import streamlit as st 
import requests
import time
from openai import OpenAI
from IPython.display import Image, display

#my-api-key-here
OpenAI.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI() 

# create a wrapper function
def get_completion(prompt, model="gpt-3.5-turbo"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role": "system", "content": f"You are a career advisor and video game developer who provides video game-based resources that help \
            university students explore potential careers based on their field of study. Name the student {character} and use emojis for a more \
            engaging and informative experience.  Based on the student's grade level and experience, write a video game plot that includes a \
            complete ten-year roadmap with details for all ten years.  Incorporate undergraduate general education requirements and include important \
            and specific resources that will aid in the student's journey. Organize the information by milestones into these categories: objectives, skills gained, \
            experience points, and unconventional advice.  For each experience point, include a specific experience point value.  Most importantly, do not leave out any information." },
        {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content

def get_image(response):
    response = client.images.generate(
        model="dall-e-3",
        prompt=major,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    
    return response.data[0].url

# create our streamlit app
with st.form(key = "chat"):
    # add questions here
    major = st.text_input("What is your major?")
    years = st.text_input("How many years of work experience do you have in your field?")
    struggles = st.text_area("What are you currently struggling with in your job search?")
    roles = st.text_area("What roles are you currently considering, if any?")
    character = st.text_input("Choose your character: Type a name!")
    submitted = st.form_submit_button("Submit")

    prompt = f"For a student studying {major}, with {years} of experience, struggling in {struggles}, and is looking for {roles}"
    response = f"Based on the student's {prompt} generate an image that represents the challenges of their journey."

    with st.spinner("Are you ready?"):
            time.sleep(5)

    if submitted:
        st.success("Starting your journey...")
        st.write(get_completion(prompt))
        st.image(get_image(response), caption="Your journey may be filled with winding paths and challenging quests. Have confidence in \
            yourself and don't give up! It's ok to ask for help along the way.")


