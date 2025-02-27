
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets["OpenAIAPI"]["openai_api_key"]

# 外部のテキストファイルを読み込む
def load_chatbot_setting():
    with open("chatbot_setting.txt", "r", encoding="utf-8") as file:
        return file.read().strip()  # 余計な空白や改行を削除

# 設定情報を読み込み
chatbot_setting = load_chatbot_setting()

# session_state に初期メッセージを設定
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": chatbot_setting}
    ]

st.write("Chatbot の設定: ", chatbot_setting)

# チャットボットとやりとりする関数
def communicate():
    if not st.session_state["user_input"]:  # 空の入力は処理しない
        return

    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages
    )

    bot_message = {"role": "assistant", "content": response["choices"][0]["message"]["content"]}
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("スーパービジネスマンの個別指導塾")
st.image("son.png")
st.write("困っていることは自力で解決しなさい。それが無理なら相談しなさい。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"] == "assistant":
            speaker = "♣️"

        st.write(speaker + ": " + message["content"])
