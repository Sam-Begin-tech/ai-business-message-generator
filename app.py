import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# --- Streamlit UI ---
st.set_page_config(page_title="AI Business Message Generator", layout="wide")
st.title("📣 AI-Powered Business Message Generator")

# --- Two Columns: Input on Left, Output on Right ---
left, right = st.columns(2)

with left:
    st.subheader("📝 Input Details")



    business_desc = st.text_area("About your Business (Give a brief description)")
    business_bio = st.text_area("Business Bio")
    prompt_input = st.text_area("Enter your prompt (Describe what the message should say)")

    tone = st.selectbox(
        "Message Tone",
        ["Punchy", "Informal", "Humorous", "Creative", "Minimal"]
    )
    Aimodel = st.selectbox(
        "AI Model",
        ["Gemini", "Openai"]
    )

    add_emoji = st.toggle("Add Emoji 😎")

    generate_btn = st.button("🚀 Generate Message")


        # API Key Inputs
    openai_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")
    google_key = st.text_input("🔑 Enter your Google API Key (for Gemini)", type="password")
with right:
    st.subheader("💡 Generated AI Message")
    if generate_btn:
        if Aimodel == "Gemini":
            if not google_key:
                st.error("Please enter your Google API Key.")
                st.stop()
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7, google_api_key=google_key)
        else:
            if not openai_key:
                st.error("Please enter your OpenAI API Key.")
                st.stop()
            llm = ChatOpenAI(openai_api_key=openai_key, temperature=0.7)

        # --- Constructing Prompt ---
        emoji_text = "Incorporate relevant emojis to enhance appeal and match the tone." if add_emoji else "Avoid using emojis in the message."

        template = f"""
        You're an expert copywriter and marketing strategist. Craft a high-converting, engaging, and brand-aligned business message with a {tone} tone. The message should be emotionally appealing, action-driven, and tailored for digital platforms (e.g., Whatsapp).

        Context:
        - Business Description: {business_desc}
        - Business Bio: {business_bio}
        - Message Objective: {prompt_input}

        Instructions:
        - {emoji_text}
        - Start with captivating headline or opening line. abd give a line gap between the headline and the message body.
        - Include a compelling hook or opening line
        - Add a clear and persuasive call-to-action (CTA)
        - Emphasize urgency, value, or exclusivity if applicable
        - Keep it concise (under 280 characters if possible)
        - Use simple, impactful language suitable for business communication
        - Generate only one message.
        - Avoid jargon or overly complex terms
        - Ensure the message aligns with the brand's voice and values
        - Use a friendly, approachable tone while maintaining professionalism
        - no hashtags
        
        Format the message so it is ready for direct publishing.
        just return the message without any additional text or explanation or subject.
        """

        prompt = PromptTemplate(
            input_variables=["business_desc", "business_bio", "prompt_input", "tone", "emoji_text"],
            template=template
        )

        chain = LLMChain(llm=llm, prompt=prompt)

        with st.spinner("Crafting your message..."):
            output = chain.run({
                "business_desc": business_desc,
                "business_bio": business_bio,
                "prompt_input": prompt_input,
                "tone": tone.lower(),
                "emoji_text": emoji_text
            })

            st.success("Here’s your message!")
            st.write(output)
