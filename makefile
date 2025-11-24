run:
	export PYTHONPATH=. && uv run app/main.py --project .

get-all:
	curl -X GET "http://127.0.0.1:8000/recipes"

 add-r1:
	curl -X POST "http://127.0.0.1:8000/recipes" -d @tmp/recipe1.json -H "Content-Type: application/json"

 add-r2:
	curl -X POST "http://127.0.0.1:8000/recipes" -d @tmp/recipe2.json -H "Content-Type: application/json"