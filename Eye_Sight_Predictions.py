# ---------------------------------------------
# Project: Eye Sight Prediction App
# Author: [Penaganti Hari Sai Priya]
# Date: [2025-04-24]
# Description: My original project for predicting Myopia and Hypermetropia using Python + Streamlit
# ---------------------------------------------


import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import os

# --- Predict Result ---
def predict_eyesight(user_input, correct_lines, reverse=False):
    user_lines = [line.strip().upper().replace(' ', '') for line in user_input.strip().split('\n') if line.strip()]
    if reverse:
        correct_lines = list(reversed(correct_lines))
    correct_lines = [line.replace(' ', '') for line in correct_lines]

    for i, (user_line, correct_line) in enumerate(zip(user_lines, correct_lines)):
        if user_line != correct_line:
            return False, i + 1
    if len(user_lines) < len(correct_lines):
        return False, len(user_lines) + 1
    return True, len(correct_lines)

# --- Chart for Vision Accuracy ---
def show_line_chart(level, total_rows, title):
    steps = list(range(1, total_rows + 1))
    values = [i if i <= level else None for i in steps]

    fig, ax = plt.subplots()
    ax.plot(steps, values, marker='o', linestyle='-', color='green')
    ax.set_xlabel("Vision Steps")
    ax.set_ylabel("Vision Clarity Level")
    ax.set_title(title)
    ax.set_ylim(0, total_rows + 1)
    for i, val in enumerate(values):
        if val:
            ax.annotate(str(val), (steps[i], values[i]), textcoords="offset points", xytext=(0, 5), ha='center')
    st.pyplot(fig)

# --- Doctor Suggestion (Myopia) ---
def get_vision_advice(level, total, condition):
    missed = total - level

    if missed == 0:
        return f"""🎉 Excellent! Accuracy: 96.6% — You saw all lines clearly. No {condition} detected.  
🍏 Eat nutritious food and stay healthy"""
    elif missed == 1:
        return f"""🟡 Accuracy: 90%. You only missed the last line. Vision is good.  
✅ No need to worry  
😎 Very-low-power glasses (optional)  
🛋️ Avoid eye strain  
🧘‍♂️ Regular eye exercises  
💻 Take screen breaks"""
    elif missed == 2:
        return f"""🟡 Mild {condition} detected — You missed the last two lines.  
✅ Monitor yearly  
😎 Glasses may help  
🛋️ Avoid strain & take breaks"""
    elif missed == 3:
        return f"""🙂 You missed the bottom three lines.  
🔍 Mild {condition} suspected  
👓 Use glasses if needed  
💧 Keep eyes hydrated"""
    elif level >= total // 2:
        return f"""⚠️ You missed several lines. Moderate {condition} likely.  
👩‍⚕️ Eye checkup recommended  
🦸‍♀️ Glasses may be needed"""
    else:
        return f"""❗ Severe {condition} suspected.  
🚨 Visit an eye specialist soon"""

# --- Suggestion for Hypermetropia Based on 36 Letters ---
def get_hyper_suggestion(correct, total_letters):
    missed = total_letters - correct
    accuracy = (correct / total_letters) * 100

    if missed == 0:
        return f"""🎉 Perfect vision! Accuracy: {accuracy:.2f}%. No Hypermetropia detected.  
🥦 Eat nutritious food and maintain eye health."""
    elif missed <= 2:
        return f"""🟢 Accuracy: {accuracy:.2f}%
✅ No worry, very minor issues.
🍎 Eye health is good. Stay hydrated and reduce screen time."""
    elif missed <= 6:
        return f"""🟡 Mild Hypermetropia detected
📊 Accuracy: {accuracy:.2f}%
👓 Mild prescription may help
💤 Avoid long reading sessions and take regular breaks."""
    elif missed <= 10:
        return f"""🟠 Moderate Hypermetropia
📉 Accuracy: {accuracy:.2f}%
🩺 Eye checkup suggested
🧘 Eye relaxation exercises may help."""
    else:
        return f"""🔴 Severe Hypermetropia suspected
🚨 Accuracy: {accuracy:.2f}%
📅 Urgent eye specialist consultation recommended!"""

# --- Streamlit App Starts ---
st.set_page_config(page_title="EyeSight Prediction App", layout="centered")
st.title("🧿 EyeSight Prediction App")

# --- User Info ---
if "test_started" not in st.session_state:
    with st.form("user_info"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        submitted = st.form_submit_button("Start Test")
        if submitted:
            st.session_state["test_started"] = True
            st.session_state["user"] = {"name": name, "age": age, "gender": gender}

# === Begin Test After User Info ===
if st.session_state.get("test_started"):
    user = st.session_state["user"]
    st.success(f"Welcome {user['name']}, age {user['age']}, gender: {user['gender']}. Let's begin your test!")

    # === Myopia Test ===
    st.header("📄 Myopia Test")
    Myopia_img = Image.open("pdf_images/page_2.png")
    st.image(Myopia_img, caption="Myopia Chart", use_column_width=True)

    user_myopia_input = st.text_area("Enter the letters you see in the chart (Top to Bottom):", key="myopia_input")
    myopia_btn = st.button("Submit Myopia Test")

    correct_lines_myopia = [
        "E",
        "F P",
        "T O Z",
        "L P E D",
        "P E C F D",
        "E D F C Z P",
        "F E L O P Z D",
        "D E F P O T E C",
        "L E F O D P C T",
        "F D P L T C E O",
        "P E Z O L C F T D"
    ]
    total_rows_myopia = len(correct_lines_myopia)

    if myopia_btn:
        passed, level = predict_eyesight(user_myopia_input, correct_lines_myopia)
        st.session_state["myopia_level"] = level
        st.session_state["myopia_accuracy"] = (level / total_rows_myopia) * 100
        st.session_state["myopia_submitted"] = True
        st.success("✅ Myopia test submitted.")

    if st.session_state.get("myopia_submitted"):
        st.subheader("📈 Myopia Vision Analysis")
        show_line_chart(st.session_state["myopia_level"], total_rows_myopia, "Myopia Vision Clarity (Bottom to Top)")
        st.markdown(f"**Accuracy:** {st.session_state['myopia_accuracy']:.2f}%")
        st.info(get_vision_advice(st.session_state["myopia_level"], total_rows_myopia, "Myopia"))

    # === Hypermetropia Test ===
    st.header("📄 Hypermetropia Test")
    hyper_img_path = "pdf_images/fixed_hyper_chart_page1.png"
    if os.path.exists(hyper_img_path):
        hyper_img = Image.open(hyper_img_path)
        st.image(hyper_img, caption="Hypermetropia Chart", use_column_width=True)

        st.subheader("Test Instructions")
        st.write("Type exactly what you see in the chart, starting from the top row to bottom.")

        user_hyper_input = st.text_area("Enter the letters you see (Top to Bottom):", key="hyper_input")
        hyper_btn = st.button("Submit Hypermetropia Test")

        correct_lines_hyper = [
            "DFHJKL",
            "ASPOIU",
            "QWERTY",
            "ZXCVBN",
            "GHRTYU",
            "LMNBVC"
        ]
        total_letters = 36

        if hyper_btn:
            user_lines = [line.strip().upper().replace(" ", "") for line in user_hyper_input.strip().split('\n') if line.strip()]
            correct_flat = "".join(correct_lines_hyper)
            user_flat = "".join(user_lines)

            correct_count = sum(1 for u, c in zip(user_flat, correct_flat) if u == c)
            wrong_count = sum(1 for u, c in zip(user_flat, correct_flat) if u != c)
            missed_count = max(0, total_letters - len(user_flat))

            accuracy = (correct_count / total_letters) * 100
            passed, level = predict_eyesight(user_hyper_input, correct_lines_hyper)

            st.session_state["hyper_level"] = level
            st.session_state["hyper_accuracy"] = accuracy
            st.session_state["hyper_submitted"] = True

            st.success("✅ Hypermetropia test submitted.")
            st.markdown(f"""
            ### 🔍 Hypermetropia Detailed Analysis:
            - **Total letters:** {total_letters}  
            - ✅ Correct: {correct_count}  
            - ❌ Wrong: {wrong_count}  
            - ⭕ Missed: {missed_count}  
            - 📊 **Accuracy:** {accuracy:.2f}%
            """)

        if st.session_state.get("hyper_submitted"):
            st.subheader("📈 Hypermetropia Vision Analysis")
            show_line_chart(st.session_state["hyper_level"], len(correct_lines_hyper), "Hypermetropia Vision Clarity (Top to Bottom)")
            st.markdown(f"**Accuracy:** {st.session_state['hyper_accuracy']:.2f}%")
            st.info(get_hyper_suggestion(correct_count, total_letters))

# --- Ending Message Based on Test Results ---
if st.session_state.get("myopia_submitted") and st.session_state.get("hyper_submitted"):
    myopia_accuracy = st.session_state["myopia_accuracy"]
    hyper_accuracy = st.session_state["hyper_accuracy"]

    # Check if both tests passed
    if myopia_accuracy >= 90 and hyper_accuracy >= 90:
        st.success(f"✅ Your eyesight is normal. Myopia accuracy: {myopia_accuracy:.2f}%, Hypermetropia accuracy: {hyper_accuracy:.2f}%. Keep taking care of your eye health!")
    # Check if only one test is detected (either Myopia or Hypermetropia)
    elif myopia_accuracy >= 90:
        st.warning(f"⚠️ You have Myopia. Myopia accuracy: {myopia_accuracy:.2f}%. Mild correction may be needed.")
        st.info(f"Please consult an eye specialist if necessary. Your Hypermetropia test was normal.")
    elif hyper_accuracy >= 90:
        st.warning(f"⚠️ You have Hypermetropia. Hypermetropia accuracy: {hyper_accuracy:.2f}%. Mild correction may be needed.")
        st.info(f"Please consult an eye specialist if necessary. Your Myopia test was normal.")
    # Check if both tests failed
    else:
        st.error("❌ Both tests suggest possible vision issues.")
        st.warning(f"❗ Based on your results, you may need bifocal/progressive lenses. Accuracy: Myopia {myopia_accuracy:.2f}%, Hypermetropia {hyper_accuracy:.2f}%.")
        st.info("Please consult a doctor for a comprehensive eye examination.")
