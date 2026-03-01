---
title: Fake Job Detector
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# PIH2026_Gamma
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