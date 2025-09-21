# Smart Farm AI 🌱🤖

Smart Farm AI is an AI-powered farm management and decision-support system built with Streamlit and Python.  
Designed for smallholder farmers and agritech builders, it helps manage crops, track productivity, predict disease and yields, monitor sensors, and provide a multilingual smart tutor (text + voice).

---

## Table of contents
- [Project overview](#project-overview)
- [Features](#features)
- [Demo / Screenshots](#demo--screenshots)
- [Installation](#installation)
- [Running the app](#running-the-app)
- [Project structure](#project-structure)
- [Key components explained](#key-components-explained)
- [Configuration](#configuration)
- [Raspberry Pi & Sensors (optional)](#raspberry-pi--sensors-optional)
- [Models & Data](#models--data)
- [Testing & Troubleshooting](#testing--troubleshooting)
- [Deployment suggestions](#deployment-suggestions)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Credits & Author](#credits--author)
- [License](#license)
- [Contact](#contact)

---

## Project overview
Smart Farm AI bundles 50+ features into a single Streamlit app to support farm management and decision-making. The app runs on desktop or mobile (Streamlit) and can be extended later with Raspberry Pi-based sensors and edge inference.

Core goals:
- Make farm data actionable for smallholder farmers.
- Combine simple ML (classification/regression) with practical farm tools (inventory, loans, scheduling).
- Provide multilingual help via a Smart Tutor (text + optional voice).
- Be deployable on low-cost hardware (Raspberry Pi) or Streamlit Cloud.

---

## Features

### 1. Farm Management
- Add / Edit / View Crop Records (Maize, Cassava, Rice, Tomato, Yam).
- Inventory Management (Add items, view stock, alerts).
- Lot Manager & Farm Indicators (track plots and indicators).
- Calendar & Season Planner.

### 2. Productivity & Records
- Sales Records & Expense Tracker.
- Farm Productivity Stats (yield, area, production history).
- Budget Planner & Profit Estimates.

### 3. AI Predictions (🧠)
- Crop Disease Detection (model saved as crop_disease_detector.pkl — logistic regression prototype).
- Yield Prediction (simple regression/ML model).
- Soil Health Check & Recommendations.
- Decision-Making Models (rule-based + ML suggestions).

### 4. Irrigation & Soil
- Irrigation Schedule Manager.
- Soil moisture logging (manual & sensor-based).
- Irrigation voice assistant (optional voice control for scheduling).

### 5. Market & Finance
- Market price tracker (scraped or manually updated).
- Farm Loan Tracker with reminders.
- Financial summaries & reports.

### 6. Sensors & Monitoring
- Live Sensor Dashboard (temperature, humidity, soil moisture).
- Sensor history & alerts.
- Sensor simulation mode (for testing without hardware).

### 7. Support & Help
- Smart Tutor: multilingual help system (text + voice output).
- FAQ & Troubleshooting assistant.
- Quick tips and treatment recommendations for detected crop diseases.

---

## Demo / Screenshots
Place screenshots in /assets/screenshots/ and reference them here. Example:

![Dashboard](assets/screenshots/dashboard.jpg)

---

## Installation

1. Create project folder and copy files (or clone if repo availablejonathanpaul_s creating a GitHub repo and pushing files
git clone https://github.com/<your-github-username>/smart-farm-ai.git
cd smart-farm-ain`
