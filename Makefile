# Development commands
build:
	docker compose up --build -d

up:
	docker compose up -d

down:
	docker compose down

down_v:
	docker compose down -v

topic_all: # all tables
	curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" http://localhost:8083/connectors/ -d @debezium.json

