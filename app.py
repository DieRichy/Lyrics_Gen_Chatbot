import os
import streamlit as st
from src.slot_manager import SlotManager
from src.lyric_generator import LyricGenerator

# ================== 1. 页面设置 ==================
# 设置网页标题
st.set_page_config(page_title="AI Lyric Generator 🎵")

# ================== 2. 模型与管理器加载 ==================
# 获取当前目录并拼接出模型路径
current_dir = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.abspath(os.path.join(current_dir, "models", "reinforce_finetuned_generator_best_no3"))

# 初始化 session 中的 slot 管理器（收集用户输入）和歌词生成器（GPT-2）
if "slot_manager" not in st.session_state:
    st.session_state.slot_manager = SlotManager()

if "lyric_generator" not in st.session_state:
    st.session_state.lyric_generator = LyricGenerator(MODEL_PATH)

# 聊天记录初始化
if "messages" not in st.session_state:
    st.session_state.messages = []

slot_manager = st.session_state.slot_manager

# ================== 3. 定义引导性问题 ==================
# 用于引导用户逐步回答 genre / topic / emotion / length
questions = {
    "genre": "What genre do you prefer for the lyrics? (e.g., pop, hiphop)",
    "topic": "What theme or topic would you like the lyrics to revolve around?",
    "emotion": "What emotion do you want the song to convey? (e.g. joy, nervousness, anger)",
    "length": "Approximately how many words would you like the lyrics to have? (e.g., 200-1200)"
}

# ================== 4. 展示历史聊天记录 ==================
# 遍历存储在 session_state 中的聊天消息并显示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ================== 5. 用户聊天逻辑：逐步收集槽位信息 ==================
if not slot_manager.is_filled():
    # 获取当前尚未填写的 slot 名称（如 genre、emotion）
    slot_to_ask = slot_manager.next_unfilled_slot()

    # 如果当前最后一条是用户输入或首次加载，显示问题
    if (len(st.session_state.messages) == 0) or (st.session_state.messages[-1]["role"] == "user"):
        st.session_state.messages.append({"role": "assistant", "content": questions[slot_to_ask]})
        st.rerun()

    # === topic 使用 dropdown 控件供用户选择 ===
    if slot_to_ask == "topic":
        topic_options = slot_manager.allowed_topics
        user_input = st.selectbox("🎯 Choose a topic for your lyrics:", topic_options)

        if st.button("Confirm Topic"):
            # 更新 slot 并显示确认信息
            slot_manager.update_slot("topic", user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Got it! Topic set to '{user_input}'."
            })

            # 如果还没填完，继续问下一个 slot
            if not slot_manager.is_filled():
                next_slot = slot_manager.next_unfilled_slot()
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": questions[next_slot]
                })
            st.rerun()

    # === 其他 slot 使用文本输入框 ===
    else:
        user_input = st.chat_input("Type your answer...")

        if user_input:
            # 用户输入展示在聊天框
            st.session_state.messages.append({"role": "user", "content": user_input})

            # length 单独处理：要求为数字
            if slot_to_ask == "length":
                try:
                    user_input = int(user_input)
                except ValueError:
                    st.error("Please enter a valid number for word count.")
                    st.rerun()

            # 调用 slot_manager 更新 slot，如果无效会抛出 ValueError
            try:
                slot_manager.update_slot(slot_to_ask, user_input)
                final_value = slot_manager.get_slots()[slot_to_ask]

                # 构造反馈信息
                if slot_to_ask == "length":
                    reply = f"Got it! Desired lyrics length is about {final_value} words."
                else:
                    reply = f"Got it! {slot_to_ask.capitalize()} set to '{final_value}'."

                # 如果还有未填写的 slot，则继续提问
                if not slot_manager.is_filled():
                    next_slot = slot_manager.next_unfilled_slot()
                    reply += f"\n\n{questions[next_slot]}"

                st.session_state.messages.append({"role": "assistant", "content": reply})

            except ValueError as ve:
                # 统一处理所有非法输入
                st.session_state.messages.append({"role": "assistant", "content": str(ve)})

            st.rerun()

# ================== 6. 所有槽位填完，生成歌词 ==================
else:
    if "lyrics_generated" not in st.session_state:
        slots = slot_manager.get_slots()

        # 🎶 调用 GPT-2 模型生成歌词
        with st.spinner("🎶 Generating lyrics, please wait..."):
            lyrics = st.session_state.lyric_generator.generate(slots)

        # 展示选定的属性和生成的歌词
        attr_display = (
            f"**🎼 Genre:** {slots['genre'].capitalize()}  \n"
            f"**🎯 Topic:** {slots['topic'].capitalize()}  \n"
            f"**🎭 Emotion:** {slots['emotion'].capitalize()}"
        )

        lyrics_block = f"{attr_display}\n\n---\n\n**📝 Generated Lyrics:**\n\n```text\n{lyrics}\n```"

        st.session_state.messages.append({
            "role": "assistant",
            "content": lyrics_block
        })

        st.session_state.lyrics_generated = True
        st.rerun()

# ================== 7. 重置按钮 ==================
# 提供“重置”按钮以清除状态并重新开始
if st.button("Reset"):
    for key in ["slot_manager", "lyric_generator", "messages", "lyrics_generated"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
