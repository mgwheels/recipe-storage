# recipe-storage

Python app designed to locally manage various recipes

Run with `make run`

Get all recipes with `curl -X GET "http://127.0.0.1:8000/recipes"`

Add recipe with:
```bash
curl -X GET "http://127.0.0.1:8000/recipes" \
-H "Content-Type: application/json" \
-d @tmp/recipe1.json
```

TODO:
- recipe1.json errors, but recipe2.json does not error
