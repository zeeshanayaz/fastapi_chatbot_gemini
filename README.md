# from project root
uvicorn backend.main:app --reload --port 8000



# from project root, example:
python3 -m http.server 5500 -d frontend
# then open http://localhost:5500 in the browser