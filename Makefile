install:
	pip install -e .

lint:
	ruff check src tests

test:
	pytest -v

run-api:
	uvicorn churn_model.api:app --reload