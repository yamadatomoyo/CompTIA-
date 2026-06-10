import streamlit as st

# アプリのタイトル
st.title("一問一答アプリ")
st.caption("間違えた問題だけを復習できます")

# 問題リスト（問題と解答の辞書）
if "questions" not in st.session_state:
    st.session_state.questions = [
        {"q": "Pythonでコメントアウトを書く際に使用する記号は？", "a": "#"},
        {"q": "文字列の長さを取得するための組み込み関数は？", "a": "len"},
        {"q": "リストの末尾に要素を追加するメソッドは？", "a": "append"},
    ]

# アプリの状態を管理する変数（セッション状態）の初期化
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "incorrect_indices" not in st.session_state:
    st.session_state.incorrect_indices = []
if "mode" not in st.session_state:
    st.session_state.mode = "main"  # "main"（本番） または "review"（復習）

# 1. 本番モードの処理
if st.session_state.mode == "main":
    idx = st.session_state.current_index
    total = len(st.session_state.questions)
    
    if idx < total:
        q_data = st.session_state.questions[idx]
        st.subheader(f"Q{idx + 1}: {q_data['q']}")
        
        # テキスト入力フォーム
        with st.form(key=f"form_{idx}"):
            user_ans = st.text_input("回答を入力してください：", key=f"input_{idx}")
            submit = st.form_submit_button("送信")
            
            if submit:
                if user_ans.strip() == q_data["a"]:
                    st.success("正解！")
                else:
                    st.error(f"不正解... 正解は '{q_data['a']}'")
                    st.session_state.incorrect_indices.append(idx)
                
                # 次の問題へ進むボタンを表示
                st.session_state.current_index += 1
                st.button("次の問題へ")
                
    else:
        st.write("ーー 全問終了 ーー")
        if not st.session_state.incorrect_indices:
            st.balloons()
            st.success("素晴らしい！全問正解です！")
            if st.button("最初からやり直す"):
                st.session_state.current_index = 0
                st.session_state.incorrect_indices = []
                st.rerun()
        else:
            st.warning(f"{len(st.session_state.incorrect_indices)}問間違えました。")
            if st.button("間違えた問題だけ復習する"):
                st.session_state.mode = "review"
                st.session_state.current_index = 0
                st.rerun()

# 2. 復習モードの処理
elif st.session_state.mode == "review":
    incorrects = st.session_state.incorrect_indices
    idx = st.session_state.current_index
    total = len(incorrects)
    
    if idx < total:
        q_idx = incorrects[idx]
        q_data = st.session_state.questions[q_idx]
        st.subheader(f"復習Q{idx + 1}: {q_data['q']}")
        
        with st.form(key=f"review_form_{idx}"):
            user_ans = st.text_input("回答を入力してください：", key=f"review_input_{idx}")
            submit = st.form_submit_button("送信")
            
            if submit:
                if user_ans.strip() == q_data["a"]:
                    st.success("正解！")
                else:
                    st.error(f"不正解... 正解は '{q_data['a']}'")
                
                st.session_state.current_index += 1
                st.button("次の問題へ")
    else:
        st.write("ーー 復習終了 ーー")
        if st.button("もう一度最初から解く"):
            st.session_state.mode = "main"
            st.session_state.current_index = 0
            st.session_state.incorrect_indices = []
            st.rerun()
