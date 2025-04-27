docker-compose build
docker-compose up -d
docker-compose down
docker-compose down -v

#RUN/BUILD ALL SERVICES WITH ONE COMMAND

docker-compose up --build -d

#TO SEE ALL DOCKER PROCESSES

docker ps

#TO STOP ALL SERVICES

docker-compose down

#TO DELETE ALL POSTGRESQL VOLUMES

docker-compose down -v 