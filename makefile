all:
	@echo "Starting dockers..."
	@cd dockers && docker-compose up -d
	@echo "Done"

setup:
	@echo "Running first time setup..."
	@cd dockers && docker-compose up --build -d
	@echo "Done"

stop:
	@echo "Stopping dockers..."
	@cd dockers && docker-compose down
	@echo "Done"

del:
	@echo "Stopping dockers..."
	@cd dockers && docker-compose down
	@echo "Done"

	@echo "Deleting volumes..."
	@cd dockers && docker volume rm dockers_data
	@echo "Done"

	@echo "Everything has been deleted, you must use the command 'make setup' to rebuild the dockers and their volumes."

start:
	@echo "Starting dockers..."
	@cd dockers && docker-compose up --build