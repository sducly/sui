init:
	docker-compose up --build -d
	docker-compose exec app ollama pull phi4
	docker-compose exec app ollama create sui -f ./Models/Sui
	docker-compose exec app ollama create functions -f ./Models/Functions
	
py:
	docker-compose exec -it app /bin/bash

start:
	docker-compose up -d
	make -j 2 start-app start-server 

start-app:
	docker-compose exec app python3 /app/app/main.py

start-server:
	python3 -m http.server

