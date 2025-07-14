

# 🌟 smart-lifestyle-suite

**smart-lifestyle-suite** is an advanced, AI-powered personal optimization system that intelligently tracks your **finance, nutrition, sleep, and fitness** — and empowers you to live better through data-driven insights and LLM-generated coaching.

Designed as a complete personal command center, it combines **Streamlit UI**, **Groq-hosted LLaMA-3 70B**, and **Google Fit integration** to give you a holistic, visually rich, and deeply interactive life management experience.

---

## 🧠 Overview

Managing life’s many moving parts can be overwhelming. This suite changes that by bringing them all into one intelligent system.

**smart-lifestyle-suite** doesn’t just log your behavior — it understands it.

It helps you:
- Track and categorize income/expenses
- Log meals, calories, and nutrition macros
- Monitor sleep duration, quality, and mood
- Analyze workouts by time, steps, calories, and intensity
- Pull real-time fitness & sleep data from Google Fit
- Get natural-language suggestions, warnings, and recovery plans powered by an LLM

From budgeting smarter to eating better and training harder — this suite guides you, daily.

---

## 🔧 Architecture & Components

The project is structured into **three primary modules**:

### 1. 💻 Streamlit Dashboard (UI Layer)

- Fully modular and responsive UI built in Streamlit
- Sidebar navigation between Finance, Food, Sleep, Exercise, Reports, and Visualizations
- Custom dark theme, gradient styling, hover effects, and confetti animations
- 3D Lifestyle Radar Chart to visualize life balance across domains
- Daily breakdown table of everything you logged
- One-click buttons to trigger AI agents or sync Google Fit

### 2. 🧠 Core Logic + AI Intelligence (Backend Layer)

The brain of the system, handling:
- CSV-based log storage for finance, food, sleep, and workouts
- Aggregation and summary functions for each module
- Rule-based alerts (junk food warnings, overspending, low sleep)
- LLM integration via **Groq API** using **LLaMA-3 70B**

#### AI Use Cases Include:
- Finance coaching based on income/expense breakdown
- Diet improvement based on calorie + macro balance
- Smart meal generation based on pantry ingredients
- Daily motivation and goal reminders
- Holistic lifestyle analysis linking food, fitness, sleep, and money

### 3. 📲 Google Fit Integration

- OAuth2 authentication via client secrets
- Pulls last 24h of sessions (activity & sleep)
- Auto-extracts steps, distance, calories, and session names
- Sleep types supported: REM, Light, Deep
- Deduplicates against your logs and safely appends new entries

---

## 📚 Key Features

### 💰 Finance Tracking & Advice
- Log income or categorized expenses
- Get budget summaries and visual breakdowns
- AI-powered savings tips tailored to your patterns
- View pie and bar charts of spending and remaining balance

### 🍽️ Nutrition Logger & Diet Coach
- Choose food from built-in calorie + macro database
- Tracks total calories, per-meal breakdown, and macro distribution
- Highlights junk food frequency
- Get LLM-based diet feedback and next-day food improvements
- Generate meals using available ingredients and a target calorie count

### 😴 Sleep Analysis
- Log sleep/wake time, screen usage before bed, and mood
- Tracks weekly average sleep hours and “sleep debt”
- Detects poor habits (e.g., too much screen time)
- Offers smart tips to improve bedtime hygiene and energy recovery

### 🏋️‍♂️ Exercise Log & Fitness Tracker
- Record activity, duration, intensity, steps, heart rate, and notes
- Weekly streaks, high intensity days, and progress toward 150 min/week goal
- Chart calorie burn by day and activity type
- Auto-sync from Google Fit with just one click

### 📊 Visualization
- **Finance:** Income vs Expense bar chart + category pie chart
- **Food:** Calories by meal type
- **Sleep:** Hours slept over time
- **Exercise:** Duration by activity and intensity scatter plots
- **3D Lifestyle Radar:** Overall balance across all life domains

### 📆 Daily Pulse
- Choose any date to see a unified summary of:
  - Meals logged
  - Exercises done
  - Money spent
- Flags risky behavior (e.g., too much junk, no exercise, high spend)

---

## 🤖 AI Integration via Groq (LLaMA-3 70B)

This suite uses the **Groq API** to call the **LLaMA-3 70B model**, generating fluent, deeply personalized feedback.

Prompts are crafted to match real user context:
- Expense history becomes financial coaching
- Logged meals become diet critiques
- Sleep patterns turn into energy and rest advice
- Exercise logs translate into recovery planning and encouragement

This isn’t just data — it’s insight.

---

## 🔁 Google Fit Sync

Use your mobile devices or wearables — this module lets you:
- Pull real-time sleep and workout sessions
- Automatically map sessions to calories, steps, and durations
- Convert Google Fit sessions into entries in your exercise log
- Track light/REM/deep sleep with timestamp accuracy

---

## ⚙️ Tech Stack

- **Python**
- **Streamlit** – UI and dashboard interface
- **Pandas** – Data handling and CSV storage
- **Plotly** – Visualizations (bar, pie, line, scatter, 3D radar)
- **Groq API** – LLaMA-3 70B model for all AI-generated feedback
- **Google Fit API (OAuth2)** – Access to health data from your devices

---

## 🧑‍💼 Who Is It For?

- Individuals seeking total control over personal health and finances
- Professionals tracking burnout, sleep, productivity, and spending
- Students managing food, exercise, screen time, and mood
- Developers building the future of **AI-powered personal wellness tools**

Whether you’re wearing a fitness tracker, logging manually, or just want to *optimize your daily flow* — this suite helps you **see, understand, and improve**.
