#!/bin/bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
python -m streamlit run app/Streamlit.py --server.port 8501 --server.address 0.0.0.0