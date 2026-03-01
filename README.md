---
title: Fake Job Detector
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# PIH2026_Gamma
app link - https://pih2026gamma-kpdrgs7zjelrlvsqxnwjpq.streamlit.app/
prototype - https://drive.google.com/file/d/19nkc2RIjgaoVnAvYRSLnBvPLcwMC5akV/view?usp=sharing
1.Problem → Input/Output
What goes in? (job posting text)
What comes out? (Real/Fake + confidence + explanation)

2.Data
Get dataset, understand label, clean minimal.

3.Model baseline
Choose fast strong baseline (TF-IDF + Logistic Regression).
Train → evaluate → save.

4.Product layer (UI)
Streamlit app: paste text → call model → show result.

5.Packaging
README, screenshots, instructions, consistent commits