up: 
	docker compose up --build -docker

etl: 
	docker exec etl python pipeline/to_landing.py
	docker exec etl python pipeline/etl.py

warehouse: 
	docker exec -ti warehouse psql postgres://dorian:1412@localhost:5432/retail_sales

down: 
	docker compose down 