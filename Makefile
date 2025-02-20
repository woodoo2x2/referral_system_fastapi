# Остановка и удаление контейнеров, сетей и volumes
app-down:
	docker-compose down --volumes --remove-orphans

# Построение и запуск контейнеров
app-start:
	docker-compose up --build

# Остановка контейнеров без удаления данных
app-stop:
	docker-compose stop

# Получение логов контейнера web (с возможностью выбора количества строк)
app-logs:
	docker logs -f web

# Очищение всех неиспользуемых контейнеров, образов, томов
app-prune:
	docker system prune -af

# Проверка статуса контейнеров
app-status:
	docker-compose ps

# Синхронизация миграций
app-migrate:
	docker-compose exec web alembic upgrade head

# Включение утилиты для работы с базой данных в контейнере (для psql, например)
app-db-shell:
	docker-compose exec db psql -U postgres