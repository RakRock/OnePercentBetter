# 1% Better Every Day

A daily improvement tracker app for kids and adults. Built with Python and Streamlit.

## Features

- **4 User Profiles**: Arjun, Krish, Sangeetha, Rakesh — each with their own dashboard
- **Daily Login Tracking**: Streaks and total days logged
- **Krish's Reading App**: "I Can Read Level 1" picture books with AI-generated cartoon illustrations and comprehension quizzes
- **Score Tracking**: Progress charts and daily score summaries
- **Beautiful UI**: Modern, colorful, and kid-friendly design

## Running Locally

```bash
# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Regenerating Story Images

The `images/` folder contains 48 pre-generated AI cartoon illustrations (one per story page). To regenerate them:

```bash
# Install the generation dependency
pip install huggingface_hub

# Set your Hugging Face token
export HF_TOKEN="hf_..."

# Run the generator (skips existing images)
python generate_images.py
```

## Deploy to Render

1. Push this repo to GitHub
2. Go to [Render](https://render.com) and create a new **Web Service**
3. Connect your GitHub repo
4. Render will auto-detect the `render.yaml` configuration
5. Click **Deploy**

## Project Structure

```
OnePercent/
├── app.py                 # Main Streamlit application
├── database.py            # SQLite database module
├── reading_content.py     # Story library with comprehension questions
├── generate_images.py     # AI image generation script (run once)
├── images/                # Pre-generated story illustrations (48 PNGs)
├── requirements.txt       # Python runtime dependencies
├── render.yaml            # Render deployment config
└── .streamlit/
    └── config.toml        # Streamlit theme and config
```

## Tech Stack

- **Frontend**: Streamlit
- **Database**: SQLite
- **Charts**: Plotly
- **Images**: FLUX.1-schnell via Hugging Face (pre-generated)
- **Deployment**: Render
