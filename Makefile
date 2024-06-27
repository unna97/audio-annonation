install:
	poetry install --with dev

test:
	#poetry run pytest .

format:	
	poetry run black .

lint:
	poetry run ruff .

refactor: format lint

deploy:
	#deploy goes here
		
all: install lint test format deploy