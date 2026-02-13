# 🌻 Seed Growth Visualization (Streamlit)

This is a Streamlit conversion of a Matplotlib-widgets interactive visualization (sliders + buttons).
It renders a phyllotaxis / seed-growth style pattern and supports stepping day-by-day or autoplay.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud (free)

1. Create a new GitHub repo and upload these files:
   - `app.py`
   - `requirements.txt`
   - `README.md`
2. Go to Streamlit Community Cloud and click **New app**
3. Select your repo + branch
4. Set **Main file path** = `app.py`
5. Deploy — Streamlit will give you a shareable link.

## Notes

- The original script wrote `radius_log.txt` on every frame and printed every seed.
  In Streamlit, the radius log is kept in memory and you can download it as `radius_log.csv`.
- Autoplay is implemented via periodic reruns (50ms), similar to the original timer.
