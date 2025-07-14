import pandas as pd
from openai import OpenAI
from datetime import datetime, timedelta
import os
import plotly.express as px
import plotly.graph_objects as go
import google_fit

# 🔐 Groq API Setup
GROQ_API_KEY = ""
GROQ_MODEL = "llama3-70b-8192"
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def call_groq_api(prompt, max_tokens=800):
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful wellness and finance assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ API error: {e}"

# 📊 Finance Tracker
finance_file = "finance_log.csv"
if os.path.exists(finance_file):
    df_finance = pd.read_csv(finance_file)
    df_finance["date"] = pd.to_datetime(df_finance["date"], format="mixed", errors="coerce")
else:
    df_finance = pd.DataFrame(columns=["date", "type", "amount", "category", "note"])

def add_transaction(t_type, amount, category, note=""):
    global df_finance
    try:
        amount = float(amount)
        if t_type.lower() not in ["income", "expense"]:
            return "⚠️ Type must be 'income' or 'expense'."
        new_entry = pd.DataFrame([{
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "type": t_type.lower(),
            "amount": amount,
            "category": category.lower(),
            "note": note
        }])
        df_finance = pd.concat([df_finance, new_entry], ignore_index=True)
        df_finance.to_csv(finance_file, index=False)
        return f"✅ Added: {t_type.upper()} ₹{amount} for '{category}' - {note}"
    except ValueError:
        return "⚠️ Invalid amount. Please enter a number."

def show_finance_summary():
    income = df_finance[df_finance["type"] == "income"]["amount"].sum()
    expense = df_finance[df_finance["type"] == "expense"]["amount"].sum()
    balance = income - expense
    expense_breakdown = df_finance[df_finance["type"] == "expense"].groupby("category")["amount"].sum()
    # Format expense breakdown as a markdown list for clean UI display
    breakdown_formatted = "\n".join([f"- **{cat.capitalize()}**: ₹{amt:.2f}" for cat, amt in expense_breakdown.items()]) if not expense_breakdown.empty else "No expenses recorded."
    return {
        "income": income,
        "expense": expense,
        "balance": balance,
        "expense_breakdown": breakdown_formatted
    }

def generate_finance_advice():
    income = df_finance[df_finance["type"] == "income"]["amount"].sum()
    expenses_df = df_finance[df_finance["type"] == "expense"]
    expenses = expenses_df.groupby("category")["amount"].sum().to_dict()
    total_expense = sum(expenses.values())
    balance = income - total_expense
    if income == 0 or not expenses:
        return "⚠️ Add some finance data before getting advice."
    breakdown = "\n".join([f"- {cat}: ₹{amt:.0f}" for cat, amt in expenses.items()])
    prompt = f"""You are a smart, helpful personal finance advisor.

Income: ₹{income}
Expenses:
{breakdown}
Total expenses: ₹{total_expense}
Available balance: ₹{balance}

Based on this, give practical savings advice for next month. Focus on reducing food, entertainment, subscriptions, etc. Recommend a monthly savings goal. Be natural, helpful, and realistic."""
    return call_groq_api(prompt)

# 🍽️ Food Tracker
food_db = {
    "roti": {"cal": 120, "cat": "carb"}, "rice": {"cal": 130, "cat": "carb"},
    "dal": {"cal": 100, "cat": "protein"}, "chicken curry": {"cal": 180, "cat": "protein"},
    "egg": {"cal": 78, "cat": "protein"}, "banana": {"cal": 90, "cat": "carb"},
    "apple": {"cal": 52, "cat": "fiber"}, "milk": {"cal": 103, "cat": "protein"},
    "bread": {"cal": 66, "cat": "carb"}, "butter": {"cal": 102, "cat": "fat"},
    "maggi": {"cal": 205, "cat": "junk"}, "pizza slice": {"cal": 285, "cat": "junk"},
    "burger": {"cal": 295, "cat": "junk"}, "chips": {"cal": 150, "cat": "junk"},
    "coffee": {"cal": 40, "cat": "fat"}, "tea": {"cal": 30, "cat": "fat"},
    "salad": {"cal": 60, "cat": "fiber"}, "paneer": {"cal": 265, "cat": "protein"},
    "oats": {"cal": 68, "cat": "carb"}, "spinach": {"cal": 30, "cat": "fiber"},
    "green beans": {"cal": 40, "cat": "fiber"}, "curd": {"cal": 60, "cat": "protein"}
}

food_file = "food_log.csv"
if os.path.exists(food_file):
    food_log = pd.read_csv(food_file)
    food_log["datetime"] = pd.to_datetime(food_log["datetime"], format="mixed", errors="coerce")
else:
    food_log = pd.DataFrame(columns=["datetime", "meal", "item", "quantity", "calories", "category"])

def log_meal(meal_type, item, qty):
    global food_log
    try:
        qty = int(qty)
        item = item.lower()
        if item not in food_db:
            return f"⚠️ '{item}' not in food database."
        cal = food_db[item]["cal"] * qty
        cat = food_db[item]["cat"]
        new_row = pd.DataFrame([{
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "meal": meal_type.lower(),
            "item": item,
            "quantity": qty,
            "calories": cal,
            "category": cat
        }])
        food_log = pd.concat([food_log, new_row], ignore_index=True)
        food_log.to_csv(food_file, index=False)
        return f"✅ {qty}x {item} logged for {meal_type} ({cal} kcal, {cat})"
    except ValueError:
        return "⚠️ Invalid quantity. Please enter a number."

def show_food_summary(limit=2200, data=None):
    if data is None:
        data = food_log
    if data.empty:
        return {"error": "⚠️ No food data to display."}
    total = data["calories"].sum()
    per_meal = data.groupby("meal")["calories"].sum()
    cat_counts = data["category"].value_counts()
    junk_warning = "🚨 Too much junk food logged today." if cat_counts.get("junk", 0) > 2 else ""
    # Format calories by meal and category counts as markdown lists for clean UI display
    meal_formatted = "\n".join([f"- **{meal.capitalize()}**: {cal:.0f} kcal" for meal, cal in per_meal.items()]) if not per_meal.empty else "No meals recorded."
    category_formatted = "\n".join([f"- **{cat.capitalize()}**: {count} items" for cat, count in cat_counts.items()]) if not cat_counts.empty else "No categories recorded."
    return {
        "data": data[["datetime", "meal", "item", "quantity", "calories", "category"]],
        "total_calories": total,
        "calorie_status": f"{'⚠️ Over Limit' if total > limit else '✅ OK'}",
        "calories_by_meal": meal_formatted,
        "category_counts": category_formatted,
        "junk_warning": junk_warning
    }

def diet_advice_agent():
    if food_log.empty:
        return "⚠️ No meals logged."
    total = food_log["calories"].sum()
    meals = food_log.groupby("meal")["calories"].sum().to_dict()
    categories = food_log["category"].value_counts().to_dict()
    meal_txt = "\n".join([f"- {k}: {v:.0f} kcal" for k, v in meals.items()])
    cat_txt = ", ".join([f"{k}={v}" for k, v in categories.items()])
    meal_list = "\n".join([f"- {row['datetime']}: {row['meal']} - {row['quantity']}x {row['item']} ({row['calories']} kcal, {row['category']})" for _, row in food_log.iterrows()])
    prompt = f"""You are a health-conscious AI nutrition coach.

Today's intake:
Total calories: {total}
Meal calories:
{meal_txt}
Nutrition distribution: {cat_txt}
Meals consumed:
{meal_list}

Based on the specific meals consumed, total calories, and nutrition distribution, assess if the user is eating too little, too much, or has an imbalance in macros (fiber, protein, etc.). Warn about junk food and suggest specific improvements for tomorrow's diet, referencing the consumed meals where relevant. Be practical and friendly."""
    return call_groq_api(prompt)

def smart_meal_suggester(ingredients, calorie_target=500, reuse_mode=True):
    ingredient_line = ", ".join(ingredients)
    reuse_clause = "Prefer reusing these ingredients to reduce waste, but you can add others as needed." if reuse_mode else "Feel free to use any ingredients."
    exercise_cals = exercise_log["est_calories"].tail(7).sum() if not exercise_log.empty else 0
    calorie_target = max(300, calorie_target + (exercise_cals / 7))
    prompt = f"""You are a nutrition coach. I have these ingredients: {ingredient_line}.
Suggest eight diverse meals from various global cuisines (e.g., Italian, Mexican, Japanese, Mediterranean, etc.) around {calorie_target} kcal each. {reuse_clause}
Mention missing macros (fiber, protein, etc) if any, and suggest what to add. Give 2–3 line steps per meal. Output should be natural, easy to follow, and include the cuisine type for each meal."""
    return call_groq_api(prompt, max_tokens=2000)

def answer_food_question(question):
    ingredient_line = ", ".join(["rice", "chicken", "spinach", "beans"])
    food_context = ""
    if not food_log.empty:
        total = food_log["calories"].sum()
        meal_list = "\n".join([f"- {row['datetime']}: {row['meal']} - {row['quantity']}x {row['item']} ({row['calories']} kcal, {row['category']})" for _, row in food_log.iterrows()])
        food_context = f"User's recent food log:\nTotal calories: {total} kcal\nMeals consumed:\n{meal_list}\n"
    question_prompt = f"""You are a nutrition coach specializing in meals, food, diet, and health. {food_context}User's available ingredients: {ingredient_line}.
Answer the following question only if it is related to meals, food, diet, or health: '{question}'.
If the question is unrelated to these topics, respond with: 'This model is built only for answering food, diet, and health-related questions, nothing else.'
Provide a detailed, practical, and friendly response."""
    return call_groq_api(question_prompt, max_tokens=1000)

# 😴 Sleep & 🏋️ Exercise Tracker
sleep_file = "sleep_log.csv"
if os.path.exists(sleep_file):
    sleep_log = pd.read_csv(sleep_file)
else:
    sleep_log = pd.DataFrame(columns=["date", "sleep_time", "wake_time", "screen_before_bed", "wake_fresh", "hours", "mood"])
    sample_sleep = pd.DataFrame([
        {"date": "2025-07-06", "sleep_time": "22:00", "wake_time": "06:00", "screen_before_bed": 30, "wake_fresh": "yes", "hours": 8.0, "mood": "happy"},
        {"date": "2025-07-07", "sleep_time": "23:00", "wake_time": "05:30", "screen_before_bed": 60, "wake_fresh": "no", "hours": 6.5, "mood": "tired"},
        {"date": "2025-07-08", "sleep_time": "22:30", "wake_time": "06:30", "screen_before_bed": 45, "wake_fresh": "yes", "hours": 8.0, "mood": "relaxed"},
        {"date": "2025-07-09", "sleep_time": "23:30", "wake_time": "06:00", "screen_before_bed": 90, "wake_fresh": "no", "hours": 6.5, "mood": "stressed"},
        {"date": "2025-07-10", "sleep_time": "22:00", "wake_time": "07:00", "screen_before_bed": 20, "wake_fresh": "yes", "hours": 9.0, "mood": "energetic"},
        {"date": "2025-07-11", "sleep_time": "22:45", "wake_time": "06:15", "screen_before_bed": 30, "wake_fresh": "yes", "hours": 7.5, "mood": "calm"},
        {"date": "2025-07-12", "sleep_time": "23:00", "wake_time": "06:30", "screen_before_bed": 40, "wake_fresh": "no", "hours": 7.5, "mood": "neutral"}
    ])
    sleep_log = pd.concat([sleep_log, sample_sleep], ignore_index=True)
    sleep_log.to_csv(sleep_file, index=False)

exercise_file = "exercise_log.csv"
if os.path.exists(exercise_file):
    exercise_log = pd.read_csv(exercise_file)
else:
    exercise_log = pd.DataFrame(columns=["date", "type", "duration", "intensity", "est_calories", "heart_rate", "steps", "notes"])
    sample_exercise = pd.DataFrame([
        {"date": "2025-07-06", "type": "running", "duration": 30, "intensity": "moderate", "est_calories": 180, "heart_rate": 140, "steps": 5000, "notes": "Felt great!"},
        {"date": "2025-07-07", "type": "yoga", "duration": 45, "intensity": "low", "est_calories": 180, "heart_rate": 90, "steps": 2000, "notes": "Stretching day"},
        {"date": "2025-07-09", "type": "cycling", "duration": 60, "intensity": "high", "est_calories": 540, "heart_rate": 160, "steps": 3000, "notes": "Tough ride"},
        {"date": "2025-07-10", "type": "weightlifting", "duration": 40, "intensity": "high", "est_calories": 360, "heart_rate": 150, "steps": 1500, "notes": "Leg day"},
        {"date": "2025-07-11", "type": "walking", "duration": 20, "intensity": "low", "est_calories": 80, "heart_rate": 100, "steps": 3000, "notes": "Evening stroll"}
    ])
    exercise_log = pd.concat([exercise_log, sample_exercise], ignore_index=True)
    exercise_log.to_csv(exercise_file, index=False)

def log_sleep(sleep_time_str, wake_time_str, screen_minutes, woke_fresh=True, mood="neutral"):
    global sleep_log
    try:
        date = datetime.now().strftime("%Y-%m-%d")
        fmt = "%H:%M"
        sleep_time = datetime.strptime(sleep_time_str, fmt)
        wake_time = datetime.strptime(wake_time_str, fmt)
        screen_minutes = int(screen_minutes)
        if wake_time <= sleep_time:
            wake_time += timedelta(days=1)
        hours = round((wake_time - sleep_time).total_seconds() / 3600, 2)
        entry = pd.DataFrame([{
            "date": date,
            "sleep_time": sleep_time_str,
            "wake_time": wake_time_str,
            "screen_before_bed": screen_minutes,
            "wake_fresh": "yes" if woke_fresh else "no",
            "hours": hours,
            "mood": mood.lower()
        }])
        if not entry.dropna(axis=1, how="all").empty:
            sleep_log = pd.concat([sleep_log, entry], ignore_index=True)
            sleep_log.to_csv(sleep_file, index=False)
        return f"🎉 Sleep logged: {hours} hrs, Mood: {mood}!"
    except ValueError:
        return "⚠️ Invalid input. Ensure time format is HH:MM and screen minutes is a number."

def log_exercise(activity_type, duration_minutes, intensity_level, heart_rate=0, steps=0, notes=""):
    global exercise_log
    try:
        duration_minutes = float(duration_minutes)
        heart_rate = int(heart_rate) if heart_rate else 0
        steps = int(steps) if steps else 0
        intensity_level = intensity_level.lower()
        if intensity_level not in ["low", "moderate", "high"]:
            return "⚠️ Intensity must be 'low', 'moderate', or 'high'."
        date = datetime.now().strftime("%Y-%m-%d")
        cal_map = {"low": 4, "moderate": 6, "high": 9}
        est_cals = duration_minutes * cal_map.get(intensity_level, 5)
        entry = pd.DataFrame([{
            "date": date,
            "type": activity_type.lower(),
            "duration": duration_minutes,
            "intensity": intensity_level,
            "est_calories": est_cals,
            "heart_rate": heart_rate,
            "steps": steps,
            "notes": notes
        }])
        if not entry.dropna(axis=1, how="all").empty:
            exercise_log = pd.concat([exercise_log, entry], ignore_index=True)
            exercise_log.to_csv(exercise_file, index=False)
        progress = exercise_log["duration"].tail(7).sum()
        goal = 150
        return {
            "message": f"💪 Exercise logged: {duration_minutes} min {activity_type}, {est_cals} kcal, HR: {heart_rate} bpm!",
            "progress": progress,
            "goal": goal
        }
    except ValueError:
        return "⚠️ Invalid input. Ensure numbers are valid."

def log_fit_exercise():
    service = google_fit.init_fit_service()
    fit_data = google_fit.get_fit_sessions(service)
    if fit_data.empty:
        return {"success": False, "message": "⚠️ No Google Fit data found.", "data": None}
    fit_data.loc[fit_data["type"].str.lower().isin(["rem sleep", "light sleep", "deep sleep", "sleeping"]), "steps"] = 0
    fit_data.loc[fit_data["type"].str.lower().isin(["rem sleep", "light sleep", "deep sleep", "sleeping"]), "distance_m"] = 0
    fit_data.loc[fit_data["type"].str.lower().isin(["rem sleep", "light sleep", "deep sleep", "sleeping"]), "calories"] = fit_data["duration_minutes"] * 1
    fit_data["date"] = pd.to_datetime(fit_data["date"], format="mixed", errors="coerce").dt.date
    fit_data["duration_minutes"] = pd.to_numeric(fit_data["duration_minutes"], errors="coerce").fillna(0).astype(float)
    success = google_fit.log_fit_to_exercise(exercise_file, fit_data)
    return {
        "success": success,
        "message": "✅ Google Fit data synced to exercise log!" if success else "⚠️ No new data to sync.",
        "data": fit_data[["date", "type", "name", "duration_minutes", "steps", "distance_m", "calories"]]
    }

def show_wellness_summary():
    if sleep_log.empty and exercise_log.empty:
        return {"error": "⚠️ No sleep or exercise data yet."}
    
    result = {"sleep": {}, "exercise": {}, "motivation": ""}
    
    if not sleep_log.empty:
        recent = sleep_log.tail(7)
        avg_hours = recent["hours"].mean()
        sleep_debt = max(0, 7 * 8 - recent["hours"].sum())
        mood_counts = recent["mood"].value_counts()
        sleep_rating = "🌟 Awesome" if avg_hours >= 7.5 else "⚠️ Boost Needed" if avg_hours < 6 else "✅ Good"
        screen_warning = f"💤 High screen time ({recent['screen_before_bed'].mean():.0f} min avg) might affect sleep." if recent["screen_before_bed"].mean() > 60 else ""
        result["sleep"] = {
            "avg_hours": avg_hours,
            "sleep_debt": sleep_debt,
            "mood_counts": mood_counts,
            "sleep_rating": sleep_rating,
            "screen_warning": screen_warning
        }
    
    if not exercise_log.empty:
        recent_ex = exercise_log.tail(7)
        recent_ex["date"] = pd.to_datetime(recent_ex["date"])
        total_mins = recent_ex["duration"].sum()
        total_cals = recent_ex["est_calories"].sum()
        high_days = recent_ex[recent_ex["intensity"] == "high"].shape[0]
        avg_hr = recent_ex["heart_rate"].mean() if recent_ex["heart_rate"].notna().any() else 0
        step_total = recent_ex["steps"].sum()
        streak = (recent_ex["date"].diff().dt.days <= 2).sum() + 1 if not recent_ex.empty else 1
        ex_rating = "🔥 Epic" if total_mins >= 200 else "💪 Solid" if total_mins >= 150 else "⚠️ Move More"
        exercise_warning = "⚠️ Aim for 150 min/week!" if total_mins < 150 else "🎉 Smashing your fitness goals!"
        fig = px.scatter(recent_ex, x="date", y="est_calories", size=recent_ex["duration"].astype(float), color="intensity",
                         title="Calorie Burn vs. Intensity (Last 7 Days)", labels={"est_calories": "Calories", "duration": "Duration (min)"},
                         color_discrete_map={"low": "green", "moderate": "orange", "high": "red"})
        result["exercise"] = {
            "total_mins": total_mins,
            "total_cals": total_cals,
            "high_days": high_days,
            "avg_hr": avg_hr,
            "step_total": step_total,
            "streak": streak,
            "ex_rating": ex_rating,
            "exercise_warning": exercise_warning,
            "scatter_fig": fig
        }
    
    avg_hours = result["sleep"].get("avg_hours", 0)
    total_mins = result["exercise"].get("total_mins", 0)
    msg = call_groq_api(f"""You're a motivational wellness coach. Based on:
- Avg sleep: {avg_hours:.1f} hrs
- Total exercise mins: {total_mins} min
Give a short, upbeat message to inspire the user for tomorrow!""")
    result["motivation"] = msg.strip()
    
    return result

def recovery_ai_agent():
    if sleep_log.empty and exercise_log.empty:
        return "⚠️ No sleep or exercise data yet."
    s = sleep_log.tail(3)
    e = exercise_log.tail(5)
    avg_sleep = s["hours"].mean() if not s.empty else 0
    wake_fresh = s["wake_fresh"].tolist() if not s.empty else []
    screen_avg = s["screen_before_bed"].mean() if not s.empty else 0
    total_exercise_mins = e["duration"].sum() if not e.empty else 0
    intense_workouts = e[e["intensity"] == "high"].shape[0] if not e.empty else 0
    prompt = f"""You're a personal recovery + wellness AI coach.

Recent data:
- Avg sleep: {avg_sleep:.1f} hrs
- Wake freshness (yes/no): {wake_fresh}
- Screen before bed avg: {screen_avg:.1f} mins
- Total exercise mins: {total_exercise_mins} mins
- Intense workouts: {intense_workouts}

Give advice for:
1. Energy levels
2. Sleep hygiene
3. If they need more rest or more workouts
4. Link screen time to poor wake-up
5. Suggest one small improvement they can do from tomorrow.

Be smart but friendly."""
    return call_groq_api(prompt)

def weekly_goal_recommender():
    avg_sleep = sleep_log["hours"].tail(7).mean() if not sleep_log.empty else 0
    total_ex = exercise_log["duration"].tail(7).sum() if not exercise_log.empty else 0
    prompt = f"""You're a smart AI health planner. Based on the data:

- Avg Sleep: {avg_sleep:.1f} hrs
- Weekly Exercise Minutes: {total_ex:.0f}

Recommend:
1. One smart sleep goal for next week.
2. One fitness activity goal.
3. What to maintain and what to improve.

Keep it short and specific."""
    return call_groq_api(prompt)

def recovery_schedule():
    prompt = """I'm feeling a bit low on energy and overtrained.

Design a simple 3-day wellness recovery plan. Include:
- Sleep timing advice
- Low-stress exercise or rest
- One helpful tip per day
Make it short and personalized."""
    return call_groq_api(prompt)

def budget_food_analysis():
    food_expenses = df_finance[(df_finance["type"] == "expense") & (df_finance["category"] == "food")]["amount"].sum()
    total_expense = df_finance[df_finance["type"] == "expense"]["amount"].sum()
    income = df_finance[df_finance["type"] == "income"]["amount"].sum()
    food_calories = food_log["calories"].sum() if not food_log.empty else 0
    prompt = f"""You're a frugal nutrition coach.

- Food expenses: ₹{food_expenses:.2f}
- Total expenses: ₹{total_expense:.2f}
- Income: ₹{income:.2f}
- Total calories consumed: {food_calories:.0f} kcal

Analyze if food spending is proportional to income and calorie needs. Suggest 2-3 cost-effective, healthy meal ideas using ingredients from the food database. Keep it practical."""
    return call_groq_api(prompt)

def holistic_wellness_report():
    avg_sleep = sleep_log["hours"].tail(7).mean() if not sleep_log.empty else 0
    total_ex_cals = exercise_log["est_calories"].tail(7).sum() if not exercise_log.empty else 0
    food_calories = food_log["calories"].tail(7).sum() if not food_log.empty else 0
    junk_count = food_log[food_log["category"] == "junk"].shape[0] if not food_log.empty else 0
    balance = df_finance[df_finance["type"] == "income"]["amount"].sum() - df_finance[df_finance["type"] == "expense"]["amount"].sum()
    prompt = f"""You're a holistic wellness coach.

- Avg sleep (last 7 days): {avg_sleep:.1f} hrs
- Exercise calories burned: {total_ex_cals:.0f} kcal
- Food calories consumed: {food_calories:.0f} kcal
- Junk food entries: {junk_count}
- Financial balance: ₹{balance:.2f}

Provide a concise report on overall wellness, linking sleep, exercise, diet, and finance. Suggest one key action to improve balance across all areas."""
    return call_groq_api(prompt)

def visualize_finance():
    if df_finance.empty:
        return {"error": "⚠️ No finance data to visualize."}
    df_finance["date"] = pd.to_datetime(df_finance["date"])
    income = df_finance[df_finance["type"] == "income"]["amount"].sum()
    expense = df_finance[df_finance["type"] == "expense"]["amount"].sum()
    bar_fig = go.Figure(data=[
        go.Bar(name="Income", x=["Income"], y=[income], marker_color="green"),
        go.Bar(name="Expense", x=["Expense"], y=[expense], marker_color="red")
    ])
    bar_fig.update_layout(title="Money Spent vs. Earned", yaxis_title="Amount (₹)", barmode="group")
    expenses = df_finance[df_finance["type"] == "expense"].groupby("category")["amount"].sum()
    pie_fig = px.pie(values=expenses.values, names=expenses.index, title="Expense Category Split") if not expenses.empty else None
    return {"bar_fig": bar_fig, "pie_fig": pie_fig}

def visualize_food():
    if food_log.empty:
        return {"error": "⚠️ No food data to visualize."}
    food_log["datetime"] = pd.to_datetime(food_log["datetime"])
    calories_by_meal = food_log.groupby("meal")["calories"].sum()
    if not calories_by_meal.empty:
        fig = px.bar(x=calories_by_meal.index, y=calories_by_meal.values, title="Calorie Intake by Meal Type",
                     labels={"x": "Meal Type", "y": "Calories (kcal)"}, color_discrete_sequence=["skyblue"])
        return {"fig": fig}
    return {"error": "⚠️ No meal data to visualize."}

def visualize_sleep():
    if sleep_log.empty:
        return {"error": "⚠️ No sleep data to visualize."}
    sleep_log["date"] = pd.to_datetime(sleep_log["date"])
    sleep_by_date = sleep_log.groupby("date")["hours"].mean()
    if not sleep_by_date.empty:
        fig = px.line(x=sleep_by_date.index, y=sleep_by_date.values, title="Sleep Duration Over Time",
                      labels={"x": "Date", "y": "Hours"}, markers=True, line_shape="linear")
        return {"fig": fig}
    return {"error": "⚠️ No sleep data to visualize."}

def visualize_exercise():
    if exercise_log.empty:
        return {"error": "⚠️ No exercise data to visualize."}
    exercise_log["date"] = pd.to_datetime(exercise_log["date"], format="mixed", errors="coerce").dt.date
    duration_by_type = exercise_log.groupby("type")["duration"].sum()
    if not duration_by_type.empty:
        fig = px.bar(x=duration_by_type.index, y=duration_by_type.values, title="Exercise Duration by Type",
                     labels={"x": "Exercise Type", "y": "Minutes"}, color_discrete_sequence=["purple"])
        return {"fig": fig}
    return {"error": "⚠️ No exercise data to visualize."}

def reset_all_data():
    global df_finance, food_log, sleep_log, exercise_log
    df_finance = pd.DataFrame(columns=["date", "type", "amount", "category", "note"])
    food_log = pd.DataFrame(columns=["datetime", "meal", "item", "quantity", "calories", "category"])
    sleep_log = pd.DataFrame(columns=["date", "sleep_time", "wake_time", "screen_before_bed", "wake_fresh", "hours", "mood"])
    exercise_log = pd.DataFrame(columns=["date", "type", "duration", "intensity", "est_calories", "heart_rate", "steps", "notes"])
    for file in [finance_file, food_file, sleep_file, exercise_file]:
        if os.path.exists(file):
            os.remove(file)
    return "✅ All data reset successfully."

def show_daily_breakdown(selected_date):
    date_str = selected_date.strftime("%Y-%m-%d")
    food_day = food_log[pd.to_datetime(food_log["datetime"]).dt.date == selected_date] if not food_log.empty else pd.DataFrame()
    ex_day = exercise_log[exercise_log["date"] == date_str] if not exercise_log.empty else pd.DataFrame()
    finance_day = df_finance[pd.to_datetime(df_finance["date"]).dt.date == selected_date] if not df_finance.empty else pd.DataFrame()
    summary = {
        "food_calories": food_day["calories"].sum() if not food_day.empty else 0,
        "exercise_minutes": ex_day["duration"].sum() if not ex_day.empty else 0,
        "finance_expense": finance_day[finance_day["type"] == "expense"]["amount"].sum() if not finance_day.empty else 0
    }
    all_data = []
    if not food_day.empty:
        for _, row in food_day.iterrows():
            all_data.append(["Food", row["datetime"], row["meal"], f"{row['quantity']}x {row['item']}", f"{row['calories']} kcal", row["category"]])
    if not ex_day.empty:
        for _, row in ex_day.iterrows():
            all_data.append(["Exercise", row["date"], row["type"], f"{row['duration']} min", f"{row['est_calories']} kcal", row["intensity"]])
    if not finance_day.empty:
        for _, row in finance_day.iterrows():
            all_data.append(["Finance", row["date"], row["type"], f"₹{row['amount']}", row["category"], row["note"]])
    df_daily = pd.DataFrame(all_data, columns=["Type", "Time", "Activity", "Details", "Value", "Category/Note"])
    return {"summary": summary, "table": df_daily}