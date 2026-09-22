import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import time
from ocr_module import extract_text_from_pil
from chatbot_module import get_definition_wikipedia
from tts_module import create_tts_audio_bytes
from visual_module import get_youtube_video_link, to_embed_url
from attentiveness_module import AttentivenessThread, status

st.set_page_config(
    page_title="AI-Powered Interactive System",
    page_icon="🎓",
    layout="wide"
)

if "att_thread" not in st.session_state:

    st.session_state.att_thread = AttentivenessThread()
    st.session_state.att_thread.start()

if "processed_topic" not in st.session_state:
    st.session_state.processed_topic = ""

if "definition" not in st.session_state:
    st.session_state.definition = ""

if "last_video" not in st.session_state:
    st.session_state.last_video = None

st.title("🎓 AI-Powered Interactive System")

st.caption(
    "Write, upload, or type a topic and learn through "
    "explanations, audio, and educational videos."
)

if st.session_state.att_thread.attentive:

    st.success("✅ Student is attentive")

else:

    st.error("⚠️ Student is not attentive")


left_col, right_col = st.columns(
    [1, 1.2],
    gap="large"
)

with left_col:

    st.subheader("📝 Enter a Topic")

    st.write(
        "Choose how you want to provide the topic."
    )


    # Input Method

    input_method = st.radio(
        "Input method",
        [
            "⌨️ Type",
            "🖼️ Upload",
            "✏️ Canvas"
        ],
        horizontal=True,
        key="input_method"
    )


    topic = ""


    if input_method == "⌨️ Type":

        typed_topic = st.text_input(
            "Topic",
            placeholder=(
                "Example: Gravity, Photosynthesis, "
                "Newton's Laws..."
            ),
            key="typed_topic"
        )


    elif input_method == "🖼️ Upload":

        uploaded = st.file_uploader(
            "Upload handwriting",
            type=[
                "png",
                "jpg",
                "jpeg"
            ],
            key="topic_image"
        )

    elif input_method == "✏️ Canvas":

        st.caption(
            "Draw or write your topic on the canvas."
        )

        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 0)",
            stroke_width=8,
            stroke_color="#000000",
            background_color="#FFFFFF",
            height=220,
            width=600,
            drawing_mode="freedraw",
            key="topic_canvas"
        )

    if st.button(
        "🚀 Process Topic",
        use_container_width=True
    ):

        topic = ""

        if input_method == "⌨️ Type":

            topic = typed_topic.strip()

        elif input_method == "🖼️ Upload":

            if uploaded is not None:

                try:

                    image_to_process = Image.open(
                        uploaded
                    ).convert("RGB")

                    with st.spinner(
                        "🔍 Reading handwriting..."
                    ):

                        topic = extract_text_from_pil(
                            image_to_process
                        ).strip()

                except Exception as e:

                    st.error(
                        f"Could not process image: {e}"
                    )

        elif input_method == "✏️ Canvas":

            if canvas_result.image_data is not None:

                try:

                    image_to_process = Image.fromarray(
                        canvas_result.image_data.astype(
                            "uint8"
                        ),
                        "RGBA"
                    ).convert("RGB")

                    with st.spinner(
                        "🔍 Reading handwriting..."
                    ):

                        topic = extract_text_from_pil(
                            image_to_process
                        ).strip()

                except Exception as e:

                    st.error(
                        f"Could not process canvas: {e}"
                    )

        if not topic:

            st.warning(
                "⚠️ Please enter, upload, or write a topic."
            )

        else:

            # Saving the newly detected/typed topic
            st.session_state.processed_topic = topic

            # Clearing old learning results
            st.session_state.definition = ""

            st.session_state.last_video = None

            st.rerun()


    if st.session_state.processed_topic:

        st.markdown("---")

        st.markdown("### ✅ Confirm Topic")


        current_topic = (
            st.session_state.processed_topic
        )

        confirmed_key = (
            "confirmed_topic_"
            + str(hash(current_topic))
        )


        confirmed_topic = st.text_input(

            "Correct the topic if needed",

            value=current_topic,

            key=confirmed_key
        )


        if st.button(
            "📚 Explain This Topic",
            use_container_width=True
        ):

            final_topic = confirmed_topic.strip()


            if not final_topic:

                st.warning(
                    "⚠️ Please enter a valid topic."
                )


            else:

                # Save final confirmed topic
                st.session_state.processed_topic = (
                    final_topic
                )

                st.markdown("### 📖 Definition")


                with st.spinner(
                    "🔎 Finding an explanation..."
                ):

                    definition = (
                        get_definition_wikipedia(
                            final_topic,
                            sentences=3
                        )
                    )


                st.session_state.definition = (
                    definition
                )


                st.write(definition)

                st.markdown("### 🔊 Listen")


                with st.spinner(
                    "Generating audio..."
                ):

                    audio_bytes = (
                        create_tts_audio_bytes(
                            definition
                        )
                    )


                if audio_bytes:

                    st.audio(
                        audio_bytes,
                        format="audio/mp3"
                    )

                else:

                    st.info(
                        "Audio could not be generated."
                    )


                st.markdown(
                    "### 🎥 Educational Video"
                )


                with st.spinner(
                    "Finding an educational video..."
                ):

                    try:

                        video_link = (
                            get_youtube_video_link(
                                final_topic
                            )
                        )

                        embed = to_embed_url(
                            video_link
                        )

                    except Exception as e:

                        embed = None

                        st.warning(
                            f"Video search failed: {e}"
                        )


                if embed:

                    st.success(
                        "🎥 Educational video found!"
                    )

                    st.session_state.last_video = (
                        embed
                    )

                else:

                    st.info(
                        "No educational video found."
                    )

with right_col:

    st.subheader("🎥 Learning Area")


    video_url = st.session_state.last_video


    if video_url:

        st.video(
            video_url,
            start_time=0
        )

    else:

        st.info(
            "🎬 Your educational video will appear "
            "here after processing a topic."
        )


    current_topic = (
        st.session_state.processed_topic
    )


    if current_topic:

        st.markdown("---")

        st.markdown(
            f"### 📌 Current Topic: **{current_topic}**"
        )


    st.markdown("---")

    st.subheader("💬 Ask a Question")

    st.caption(
        "Ask a question to clear your doubts."
    )


    user_q = st.text_input(
        "Your question",
        placeholder=(
            "Example: Why does gravity pull objects "
            "towards Earth?"
        ),
        key="user_question"
    )


    if user_q.strip():

        with st.spinner(
            "🔎 Finding an explanation..."
        ):

            answer = get_definition_wikipedia(
                user_q,
                sentences=3
            )


        st.markdown("### 💡 Answer")

        st.write(answer)

        with st.spinner(
            "Generating audio..."
        ):

            answer_audio = (
                create_tts_audio_bytes(
                    answer
                )
            )


        if answer_audio:

            st.audio(
                answer_audio,
                format="audio/mp3"
            )


st.sidebar.title("👀 Attentiveness")

stat = status

is_attentive = stat.get(
    "attentive",
    False
)

reason = stat.get(
    "reason",
    ""
)

last_update = stat.get(
    "last_update",
    0
)


st.sidebar.write(
    f"Attentive: "
    f"{'✅ Yes' if is_attentive else '❌ No'}"
)

st.sidebar.write(
    f"Status: {reason}"
)


if last_update:

    st.sidebar.write(
        "Last update: "
        + time.ctime(last_update)
    )

else:

    st.sidebar.write(
        "Last update: Not updated"
    )

st.sidebar.markdown("---")

st.sidebar.subheader("📌 How to Use")

st.sidebar.write(
    "1. Choose Type, Upload, or Canvas."
)

st.sidebar.write(
    "2. Enter your topic."
)

st.sidebar.write(
    "3. Click Process Topic."
)

st.sidebar.write(
    "4. Confirm or correct the topic."
)

st.sidebar.write(
    "5. Click Explain This Topic."
)

st.sidebar.write(
    "6. Read, listen, or watch the explanation."
)

st.sidebar.write(
    "7. Ask questions in the chat."
)

time.sleep(2)

st.rerun()