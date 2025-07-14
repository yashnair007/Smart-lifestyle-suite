import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from Life_final import (
    add_transaction, show_finance_summary, generate_finance_advice,
    log_meal, show_food_summary, diet_advice_agent, smart_meal_suggester, answer_food_question,
    log_sleep, log_exercise, log_fit_exercise, show_wellness_summary,
    recovery_ai_agent, weekly_goal_recommender, recovery_schedule,
    budget_food_analysis, holistic_wellness_report,
    visualize_finance, visualize_food, visualize_sleep, visualize_exercise,
    reset_all_data, df_finance, food_log, sleep_log, exercise_log, food_db,
    show_daily_breakdown
)

# Streamlit page configuration
st.set_page_config(
    page_title="🌟 LifeSync: Wellness & Finance",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🌟"
)

# Custom CSS for a modern, vibrant, and professional UI
st.markdown("""
    <style>
        /* Global Styles */
        .main {
            background: linear-gradient(135deg, #1a1a3d 0%, #2a2a5e 50%, #3a3a7d 100%);
            color: #e6e6ff;
            font-family: 'Inter', sans-serif;
            padding: 30px;
            min-height: 100vh;
        }
        .stApp {
            background: transparent;
        }
        /* Header */
        .header {
            font-size: 3.2em;
            font-weight: 700;
            color: #ffffff;
            text-align: center;
            margin-bottom: 40px;
            letter-spacing: -0.5px;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.9; }
            100% { opacity: 1; }
        }
        /* Cards */
        .card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(12px);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            animation: slideIn 0.5s ease forwards;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(78, 205, 196, 0.2);
        }
        @keyframes slideIn {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        /* Buttons */
        .stButton>button {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 30px;
            font-weight: 600;
            font-size: 1.1em;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(78, 205, 196, 0.3);
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.5);
            background: linear-gradient(45deg, #ff8787, #6bf4e8);
        }
        /* Metrics */
        .metric {
            font-size: 1.3em;
            color: #e6e6ff;
            font-weight: 500;
            margin: 10px 0;
            display: flex;
            align-items: center;
        }
        .metric-label {
            font-weight: 700;
            color: #4ecdc4;
            margin-right: 10px;
        }
        /* Sidebar */
        .sidebar .stSelectbox, .sidebar .stTextInput, .sidebar .stNumberInput {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            color: #ffffff;
            border: 1px solid #4ecdc4;
        }
        .sidebar .stSelectbox select {
            color: #ffffff;
        }
        .sidebar .css-1d391kg {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        /* Inputs */
        .stTextInput input, .stTextArea textarea, .stSelectbox select, .stNumberInput input {
            background: rgba(255, 255, 255, 0.08);
            color: #ffffff;
            border: 1px solid #4ecdc4;
            border-radius: 10px;
            padding: 10px;
            transition: border-color 0.3s ease;
        }
        .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus, .stNumberInput input:focus {
            border-color: #ff6b6b;
            box-shadow: 0 0 8px rgba(255, 107, 107, 0.3);
        }
        .stDateInput input {
            background: rgba(255, 255, 255, 0.08);
            color: #ffffff;
            border: 1px solid #4ecdc4;
            border-radius: 10px;
        }
        /* Progress Bars */
        .stProgress .st-bo {
            background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
            border-radius: 10px;
        }
        /* Sliders */
        .stSlider .st-bv {
            background: #ff6b6b;
        }
        /* Toggle */
        .stToggle .st-d6 {
            background: #4ecdc4;
        }
        /* Badges */
        .badge {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            color: white;
            padding: 6px 12px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: 600;
            margin-left: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }
        /* Confetti Animation */
        .confetti {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9999;
        }
        /* Plotly Charts */
        .js-plotly-plot .plotly .main-svg {
            background: transparent !important;
        }
        .js-plotly-plot .plotly .modebar {
            background: rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px;
        }
        /* Dataframe */
        .stDataFrame table {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            color: #e6e6ff;
        }
        .stDataFrame th {
            background: rgba(78, 205, 196, 0.2);
            color: #ffffff;
            font-weight: 600;
        }
        .stDataFrame td {
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <script>
        function triggerConfetti() {
            confetti({
                particleCount: 200,
                spread: 90,
                origin: { y: 0.5 },
                colors: ['#ff6b6b', '#4ecdc4', '#ffffff'],
                shapes: ['circle', 'square', 'triangle'],
                disableForReducedMotion: true
            });
        }
    </script>
""", unsafe_allow_html=True)

def show_homepage():
    st.markdown('<div class="header">🌟 LifeSync: Wellness & Finance</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2em; color: #e6e6ff;">Empower your life with balance and style.</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")
    income = df_finance[df_finance["type"] == "income"]["amount"].sum()
    expense = df_finance[df_finance["type"] == "expense"]["amount"].sum()
    balance = income - expense
    with col1:
        st.markdown("""
            <div class="card">
                <h3 style="color: #4ecdc4;">💰 Finance Hub</h3>
                <p class="metric"><span class="metric-label">Income:</span> ₹{:.2f}</p>
                <p class="metric"><span class="metric-label">Expense:</span> ₹{:.2f}</p>
                <p class="metric"><span class="metric-label">Balance:</span> ₹{:.2f}</p>
            </div>
        """.format(income, expense, balance), unsafe_allow_html=True)
        if st.button("💸 Add Cash Flow", key="quick_finance"):
            st.session_state.option = "Add Transaction"
            st.rerun()

    total_calories = food_log["calories"].sum() if not food_log.empty else 0
    calorie_goal = 2200
    with col2:
        st.markdown("""
            <div class="card">
                <h3 style="color: #4ecdc4;">🍽️ Nutrition Zone</h3>
                <p class="metric"><span class="metric-label">Calories:</span> {} kcal</p>
                <p class="metric"><span class="metric-label">Meals Logged:</span> {}</p>
            </div>
        """.format(total_calories, food_log.shape[0] if not food_log.empty else 0), unsafe_allow_html=True)
        st.progress(min(total_calories / calorie_goal, 1.0))
        if st.button("🍴 Log a Meal", key="quick_meal"):
            st.session_state.option = "Log Meal"
            st.rerun()

    avg_sleep = sleep_log["hours"].mean() if not sleep_log.empty else 0
    total_ex_mins = exercise_log["duration"].sum() if not exercise_log.empty else 0
    with col3:
        st.markdown("""
            <div class="card">
                <h3 style="color: #4ecdc4;">🏋️‍♂️ Wellness Core</h3>
                <p class="metric"><span class="metric-label">Avg Sleep:</span> {:.1f} hrs</p>
                <p class="metric"><span class="metric-label">Exercise:</span> {} min</p>
            </div>
        """.format(avg_sleep, total_ex_mins), unsafe_allow_html=True)
        st.progress(min(avg_sleep / 8.0, 1.0))
        if st.button("😴 Log Wellness", key="quick_wellness"):
            st.session_state.option = "Log Sleep"
            st.rerun()

    categories = ["Finance", "Nutrition", "Sleep", "Exercise"]
    values = [
        max(balance / 50000, 0.1),
        max(total_calories / 2200, 0.1),
        max(avg_sleep / 8.0, 0.1),
        max(total_ex_mins / 150, 0.1)
    ]
    fig = go.Figure(data=[
        go.Scatter3d(
            x=[1, 2, 3, 4, 1],
            y=[0, 0, 0, 0, 0],
            z=values + [values[0]],
            mode='lines+markers',
            line=dict(color='#4ecdc4', width=5),
            marker=dict(size=10, color='#ff6b6b', symbol='circle')
        )
    ])
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='', ticktext=categories, tickvals=[1, 2, 3, 4], showgrid=False, color='#e6e6ff'),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            zaxis=dict(title='Score', range=[0, 1], showgrid=False, color='#e6e6ff'),
            bgcolor='rgba(0,0,0,0)'
        ),
        title=dict(text="Your Life Balance (3D View)", font=dict(color='#ffffff', size=20)),
        margin=dict(t=50, b=50, l=50, r=50),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e6e6ff'),
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

def display_daily_breakdown():
    st.markdown('<div class="header">📅 Your Daily Pulse</div>', unsafe_allow_html=True)
    selected_date = st.date_input("Pick a Day", value=datetime.now().date(),
                                 min_value=datetime(2025, 7, 1), max_value=datetime.now().date(),
                                 help="Explore your day's activities")
    result = show_daily_breakdown(selected_date)

    st.markdown('<h3 style="color: #4ecdc4;">📊 Day at a Glance</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        food_cal = result["summary"]["food_calories"]
        st.metric("🍽️ Calories", f"{food_cal} kcal",
                  delta="⚠️ Over 2200" if food_cal > 2200 else "✅ OK",
                  delta_color="normal")
    with col2:
        ex_mins = result["summary"]["exercise_minutes"]
        st.metric("🏋️‍♂️ Exercise", f"{ex_mins} min",
                  delta="💪 On Track" if ex_mins >= 30 else "⚠️ Move More",
                  delta_color="normal")
    with col3:
        fin_exp = result["summary"]["finance_expense"]
        st.metric("💰 Spending", f"₹{fin_exp:.2f}",
                  delta="✅ Frugal" if fin_exp < 5000 else "⚠️ High Spend",
                  delta_color="normal")

    st.markdown('<h3 style="color: #4ecdc4;">📋 All Activities</h3>', unsafe_allow_html=True)
    df_daily = result["table"]
    if not df_daily.empty:
        st.dataframe(df_daily, use_container_width=True, hide_index=True)
    else:
        st.info("⚠️ No data logged for this day yet. Start tracking! 🌟")

# Main UI
st.markdown('<div class="header">🌟 LifeSync: Wellness & Finance</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<h3 style="color: #4ecdc4;">🛠️ Control Center</h3>', unsafe_allow_html=True)
    option = st.selectbox(
        "Navigate",
        [
            "Home", "Add Transaction", "Show Finance Summary", "Get Finance Advice",
            "Log Meal", "Show Food Summary", "Get Diet Advice", "Suggest Meals", "Ask Food Questions",
            "Log Sleep", "Log Exercise", "Sync Google Fit", "Show Wellness Summary",
            "Get Recovery Advice", "Weekly Goal Recommender", "Recovery Schedule",
            "Budget vs. Food Analysis", "Holistic Wellness Report",
            "Visualize Data", "Reset All Data", "Daily Breakdown"
        ],
        key="main_option",
        help="Choose your adventure"
    )
    st.markdown("---")
    st.markdown('<h4 style="color: #4ecdc4;">Quick Stats</h4>', unsafe_allow_html=True)
    balance = df_finance[df_finance["type"] == "income"]["amount"].sum() - df_finance[df_finance["type"] == "expense"]["amount"].sum()
    st.markdown(f'<p class="metric"><span class="metric-label">💰 Balance:</span> ₹{balance:.2f} <span class="badge">{"+" if balance > 0 else "-"}</span></p>', unsafe_allow_html=True)
    st.markdown(f'<p class="metric"><span class="metric-label">🍽️ Calories:</span> {food_log["calories"].sum() if not food_log.empty else 0} kcal <span class="badge">{"🔥" if food_log["calories"].sum() > 2200 else "✅"}</span></p>', unsafe_allow_html=True)
    st.markdown(f'<p class="metric"><span class="metric-label">😴 Sleep:</span> {sleep_log["hours"].mean() if not sleep_log.empty else 0:.1f} hrs <span class="badge">{"🌙" if sleep_log["hours"].mean() >= 7 else "⚠️"}</span></p>', unsafe_allow_html=True)
    st.markdown(f'<p class="metric"><span class="metric-label">🏋️‍♂️ Exercise:</span> {exercise_log["duration"].sum() if not exercise_log.empty else 0} min <span class="badge">{"💪" if exercise_log["duration"].sum() >= 150 else "⚠️"}</span></p>', unsafe_allow_html=True)

# Main Content
with st.container():
    if option == "Home":
        show_homepage()
    elif option == "Add Transaction":
        st.markdown('<h3 style="color: #4ecdc4;">💰 Track Your Cash Flow</h3>', unsafe_allow_html=True)
        with st.form("finance_form"):
            col1, col2 = st.columns(2)
            with col1:
                t_type = st.selectbox("Type", ["Income", "Expense"], help="Income or expense?")
                amount = st.number_input("Amount (₹)", min_value=0.0, step=0.01, format="%.2f")
            with col2:
                category = st.text_input("Category", placeholder="e.g., rent, salary")
                note = st.text_input("Note (optional)", placeholder="What's this for?")
            submit = st.form_submit_button("Add Transaction")
            if submit:
                result = add_transaction(t_type, amount, category, note)
                st.success(result)
                st.markdown('<script>triggerConfetti();</script>', unsafe_allow_html=True)
    elif option == "Show Finance Summary":
        st.markdown('<h3 style="color: #4ecdc4;">💰 Finance Overview</h3>', unsafe_allow_html=True)
        summary = show_finance_summary()
        st.markdown(f'<p class="metric"><span class="metric-label">Total Income:</span> ₹{summary["income"]:.2f}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="metric"><span class="metric-label">Total Expense:</span> ₹{summary["expense"]:.2f}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="metric"><span class="metric-label">Available Balance:</span> ₹{summary["balance"]:.2f}</p>', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #4ecdc4;">Expense Breakdown:</h4>', unsafe_allow_html=True)
        st.markdown(summary["expense_breakdown"], unsafe_allow_html=True)
    elif option == "Get Finance Advice":
        st.markdown('<h3 style="color: #4ecdc4;">💡 Smart Money Tips</h3>', unsafe_allow_html=True)
        advice = generate_finance_advice()
        st.markdown(advice, unsafe_allow_html=True)
    elif option == "Log Meal":
        st.markdown('<h3 style="color: #4ecdc4;">🍽️ Log Your Meal</h3>', unsafe_allow_html=True)
        with st.form("meal_form"):
            col1, col2 = st.columns(2)
            with col1:
                meal_type = st.text_input("Meal Type", placeholder="e.g., breakfast, lunch")
                item = st.selectbox("Food Item", list(food_db.keys()), help="Pick your food")
            with col2:
                qty = st.slider("Quantity", 1, 10, 1, help="How many servings?")
            submit = st.form_submit_button("Log Meal")
            if submit:
                result = log_meal(meal_type, item, qty)
                st.success(result)
                st.markdown('<script>triggerConfetti();</script>', unsafe_allow_html=True)
    elif option == "Show Food Summary":
        st.markdown('<h3 style="color: #4ecdc4;">🍽️ Nutrition Snapshot</h3>', unsafe_allow_html=True)
        selected_date = st.date_input("Select a Day", value=datetime.now().date(),
                                      min_value=datetime(2025, 7, 1), max_value=datetime.now().date(),
                                      help="View nutrition data for a specific day")
        limit = st.slider("Calorie Limit", 1000, 3000, 2200, step=100, help="Set your daily goal")
        daily_food_log = food_log[pd.to_datetime(food_log["datetime"]).dt.date == selected_date] if not food_log.empty else pd.DataFrame()
        summary = show_food_summary(limit) if daily_food_log.empty else show_food_summary(limit, daily_food_log)
        if "error" in summary:
            st.error(summary["error"])
        else:
            st.markdown(f'<h4 style="color: #4ecdc4;">Meals Consumed on {selected_date.strftime("%Y-%m-%d")}:</h4>', unsafe_allow_html=True)
            st.dataframe(summary["data"], use_container_width=True)
            st.markdown(f'<p class="metric"><span class="metric-label">Total Calories:</span> {summary["total_calories"]:.0f} kcal <span class="badge">{summary["calorie_status"]}</span></p>', unsafe_allow_html=True)
            st.markdown('<h4 style="color: #4ecdc4;">Calories by Meal:</h4>', unsafe_allow_html=True)
            st.markdown(summary["calories_by_meal"], unsafe_allow_html=True)
            st.markdown('<h4 style="color: #4ecdc4;">Count by Macro:</h4>', unsafe_allow_html=True)
            st.markdown(summary["category_counts"], unsafe_allow_html=True)
            if summary["junk_warning"]:
                st.warning(summary["junk_warning"])
    elif option == "Get Diet Advice":
        st.markdown('<h3 style="color: #4ecdc4;">🥗 Nutrition Coach</h3>', unsafe_allow_html=True)
        advice = diet_advice_agent()
        st.markdown(advice, unsafe_allow_html=True)
    elif option == "Suggest Meals":
        st.markdown('<h3 style="color: #4ecdc4;">🍴 Meal Ideas</h3>', unsafe_allow_html=True)
        with st.form("meal_suggest_form"):
            ingredients = st.text_input("Ingredients (comma-separated)", value="rice, chicken, spinach, beans")
            calorie_target = st.slider("Calorie Target per Meal", 200, 1000, 500, step=50)
            reuse = st.checkbox("Reuse Ingredients", value=True)
            submit = st.form_submit_button("Suggest Meals")
            if submit:
                if not ingredients.strip():
                    st.error("Please enter at least one ingredient.")
                else:
                    meal_output = smart_meal_suggester(ingredients.split(","), calorie_target, reuse)
                    st.markdown('<h3 style="color: #4ecdc4;">🤖 Meal Suggestions</h3>', unsafe_allow_html=True)
                    st.markdown(meal_output, unsafe_allow_html=True)
    elif option == "Ask Food Questions":
        st.markdown('<h3 style="color: #4ecdc4;">❓ Food & Diet Q&A</h3>', unsafe_allow_html=True)
        with st.form("food_question_form"):
            question = st.text_area("Ask about meals, diet, or health", placeholder="What's on your mind?", height=100)
            submit = st.form_submit_button("Get Answer")
            if submit:
                if not question.strip():
                    st.error("Please enter a question.")
                else:
                    question_output = answer_food_question(question)
                    st.markdown('<h3 style="color: #4ecdc4;">🤖 Answers</h3>', unsafe_allow_html=True)
                    st.markdown(question_output, unsafe_allow_html=True)
    elif option == "Log Sleep":
        st.markdown('<h3 style="color: #4ecdc4;">😴 Log Your Sleep Vibes</h3>', unsafe_allow_html=True)
        with st.form("sleep_form"):
            col1, col2 = st.columns(2)
            with col1:
                sleep_time = st.text_input("Sleep Time (HH:MM)", placeholder="e.g., 22:00")
                wake_time = st.text_input("Wake Time (HH:MM)", placeholder="e.g., 06:00")
                screen_minutes = st.number_input("Screen Time Before Bed (min)", min_value=0, step=1)
            with col2:
                woke_fresh = st.toggle("Woke Up Fresh", value=True)
                mood = st.selectbox("Mood", ["happy", "tired", "relaxed", "stressed", "energetic", "calm", "neutral"])
            submit = st.form_submit_button("Log Sleep")
            if submit:
                result = log_sleep(sleep_time, wake_time, screen_minutes, woke_fresh, mood)
                st.success(result)
                st.markdown('<script>triggerConfetti();</script>', unsafe_allow_html=True)
    elif option == "Log Exercise":
        st.markdown('<h3 style="color: #4ecdc4;">🏋️‍♂️ Log Your Workout Win</h3>', unsafe_allow_html=True)
        with st.form("exercise_form"):
            col1, col2 = st.columns(2)
            with col1:
                activity = st.text_input("Activity Type", placeholder="e.g., running, yoga")
                duration = st.slider("Duration (min)", 1, 180, 30, step=1)
                intensity = st.selectbox("Intensity", ["Low", "Moderate", "High"])
            with col2:
                heart_rate = st.number_input("Avg Heart Rate (bpm)", min_value=0, step=1, value=0)
                steps = st.number_input("Steps", min_value=0, step=100, value=0)
                notes = st.text_area("Workout Notes", placeholder="How did it go?")
            submit = st.form_submit_button("Log Workout")
            if submit:
                result = log_exercise(activity, duration, intensity, heart_rate, steps, notes)
                st.success(result["message"])
                st.progress(min(1.0, result["progress"] / result["goal"]))
                st.markdown('<script>triggerConfetti();</script>', unsafe_allow_html=True)
    elif option == "Sync Google Fit":
        st.markdown('<h3 style="color: #4ecdc4;">📱 Sync Google Fit</h3>', unsafe_allow_html=True)
        result = log_fit_exercise()
        if result["data"] is not None:
            st.markdown('<h3 style="color: #4ecdc4;">📱 Google Fit Data</h3>', unsafe_allow_html=True)
            st.dataframe(result["data"], use_container_width=True)
            if st.button("Log to Exercise Log"):
                if result["success"]:
                    st.success(result["message"])
                    st.markdown('<script>triggerConfetti();</script>', unsafe_allow_html=True)
                else:
                    st.warning(result["message"])
        else:
            st.warning(result["message"])
    elif option == "Show Wellness Summary":
        st.markdown('<h3 style="color: #4ecdc4;">🌟 Wellness Dashboard</h3>', unsafe_allow_html=True)
        summary = show_wellness_summary()
        if "error" in summary:
            st.error(summary["error"])
        else:
            st.markdown('<h4 style="color: #4ecdc4;">😴 Sleep Insights</h4>', unsafe_allow_html=True)
            if summary["sleep"]:
                st.markdown(f'<p class="metric"><span class="metric-label">Avg Sleep:</span> {summary["sleep"]["avg_hours"]:.1f} hrs ({summary["sleep"]["sleep_rating"]})</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="metric"><span class="metric-label">Sleep Debt:</span> {summary["sleep"]["sleep_debt"]:.1f} hrs to catch up!</p>', unsafe_allow_html=True)
                st.markdown('<h5 style="color: #4ecdc4;">Mood Trends:</h5>', unsafe_allow_html=True)
                st.bar_chart(summary["sleep"]["mood_counts"])
                if summary["sleep"]["screen_warning"]:
                    st.warning(summary["sleep"]["screen_warning"])
            
            st.markdown('<h4 style="color: #4ecdc4;">🏋️‍♂️ Exercise Power-Up</h4>', unsafe_allow_html=True)
            if summary["exercise"]:
                st.markdown(f'<p class="metric"><span class="metric-label">Total this week:</span> {summary["exercise"]["total_mins"]} min, {summary["exercise"]["total_cals"]} kcal burned ({summary["exercise"]["ex_rating"]})</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="metric"><span class="metric-label">High-Intensity Days:</span> {summary["exercise"]["high_days"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="metric"><span class="metric-label">Avg Heart Rate:</span> {summary["exercise"]["avg_hr"]:.0f} bpm</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="metric"><span class="metric-label">Total Steps:</span> {summary["exercise"]["step_total"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="metric"><span class="metric-label">Streak:</span> {summary["exercise"]["streak"]} days! Keep the fire burning! 🔥</p>', unsafe_allow_html=True)
                st.plotly_chart(summary["exercise"]["scatter_fig"])
                st.markdown(summary["exercise"]["exercise_warning"], unsafe_allow_html=True)
            
            st.markdown('<h4 style="color: #4ecdc4;">🌟 Your Wellness Boost</h4>', unsafe_allow_html=True)
            st.markdown(summary["motivation"], unsafe_allow_html=True)
    elif option == "Get Recovery Advice":
        st.markdown('<h3 style="color: #4ecdc4;">🧘 Recovery Coach</h3>', unsafe_allow_html=True)
        advice = recovery_ai_agent()
        st.markdown(advice, unsafe_allow_html=True)
    elif option == "Weekly Goal Recommender":
        st.markdown('<h3 style="color: #4ecdc4;">🎯 Weekly Goals</h3>', unsafe_allow_html=True)
        goals = weekly_goal_recommender()
        st.markdown(goals, unsafe_allow_html=True)
    elif option == "Recovery Schedule":
        st.markdown('<h3 style="color: #4ecdc4;">📅 Recovery Plan</h3>', unsafe_allow_html=True)
        schedule = recovery_schedule()
        st.markdown(schedule, unsafe_allow_html=True)
    elif option == "Budget vs. Food Analysis":
        st.markdown('<h3 style="color: #4ecdc4;">🍴 Budget vs. Nutrition</h3>', unsafe_allow_html=True)
        analysis = budget_food_analysis()
        st.markdown(analysis, unsafe_allow_html=True)
    elif option == "Holistic Wellness Report":
        st.markdown('<h3 style="color: #4ecdc4;">🌍 Holistic Report</h3>', unsafe_allow_html=True)
        report = holistic_wellness_report()
        st.markdown(report, unsafe_allow_html=True)
    elif option == "Visualize Data":
        st.markdown('<h3 style="color: #4ecdc4;">📊 Visualize Your Journey</h3>', unsafe_allow_html=True)
        viz_type = st.selectbox("Choose Visualization", ["Finance", "Food", "Sleep", "Exercise"])
        if viz_type == "Finance":
            viz = visualize_finance()
            if "error" in viz:
                st.error(viz["error"])
            else:
                st.plotly_chart(viz["bar_fig"])
                if viz["pie_fig"]:
                    st.plotly_chart(viz["pie_fig"])
        elif viz_type == "Food":
            viz = visualize_food()
            if "error" in viz:
                st.error(viz["error"])
            else:
                st.plotly_chart(viz["fig"])
        elif viz_type == "Sleep":
            viz = visualize_sleep()
            if "error" in viz:
                st.error(viz["error"])
            else:
                st.plotly_chart(viz["fig"])
        elif viz_type == "Exercise":
            viz = visualize_exercise()
            if "error" in viz:
                st.error(viz["error"])
            else:
                st.plotly_chart(viz["fig"])
    elif option == "Reset All Data":
        st.markdown('<h3 style="color: #4ecdc4;">🗑️ Start Fresh</h3>', unsafe_allow_html=True)
        st.warning("This will wipe all data. Sure you want to proceed?")
        if st.button("Confirm Reset"):
            result = reset_all_data()
            st.success(result)
            st.markdown('<script>triggerConfetti();</script>', unsafe_allow_html=True)
    elif option == "Daily Breakdown":
        display_daily_breakdown()