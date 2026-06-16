import streamlit as st

st.set_page_config(page_title="할 일 관리", layout="centered")

if "todos" not in st.session_state:
    st.session_state["todos"] = []

def add_todo():
    text = st.session_state.get("new_todo", "").strip()
    if text:
        st.session_state.todos.append({"text": text, "done": False})
        st.session_state.new_todo = ""

def delete_todo(idx: int) -> None:
    if 0 <= idx < len(st.session_state.todos):
        st.session_state.todos.pop(idx)

def toggle_done(idx: int) -> None:
    key = f"todo_checkbox_{idx}"
    # sync checkbox state into the todos list
    if 0 <= idx < len(st.session_state.todos):
        st.session_state.todos[idx]["done"] = bool(st.session_state.get(key, False))


st.title("할 일(To-Do) 관리")
st.markdown("간단한 세션 기반 할 일 관리 앱")

with st.form(key="add_form", clear_on_submit=False):
    st.text_input("새 할 일", key="new_todo")
    st.form_submit_button("추가", on_click=add_todo)

done_count = sum(1 for t in st.session_state.todos if t.get("done"))
total_count = len(st.session_state.todos)

col1, col2 = st.columns(2)
col1.metric("전체", total_count)
col2.metric("완료", done_count)

st.divider()

for i, todo in enumerate(list(st.session_state.todos)):
    cols = st.columns([0.7, 0.2])
    key = f"todo_checkbox_{i}"
    # initialize checkbox key to current state
    if key not in st.session_state:
        st.session_state[key] = todo.get("done", False)

    cols[0].checkbox(label=todo.get("text", ""), value=st.session_state[key], key=key, on_change=toggle_done, args=(i,))
    if cols[1].button("삭제", key=f"delete_{i}"):
        delete_todo(i)
        st.experimental_rerun()
