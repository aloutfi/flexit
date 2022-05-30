build:
	docker-compose up -d
	echo "Sleeping for 10 seconds so database can start up..."
	sleep 10
	python -c 'from config import init_db; init_db(True)'

purge:
	docker-compose down --rmi all

rebuild:
	make purge
	make build