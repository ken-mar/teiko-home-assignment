.PHONY: setup pipeline dashboard

setup:
	pip install -r requirements.txt

pipeline:
	python load_data.py
	python pipeline.py

dashboard:
	python3.11 -m streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0
