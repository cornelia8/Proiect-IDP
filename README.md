# /// BASIC MARKETPLACE APP ///

# + KUBERNETES COMMANDS +

# GENERAL

# To Deploy:

```
eval $(minikube docker-env)
docker build -t idp_user_service ./user_service
docker build -t idp_shop_service ./shop_service
docker build -t idp_transaction_service ./transaction_service
docker build -t idp_api_gateway ./api_gateway
```

# To Apply:
```
kubectl create namespace marketplace
kubectl apply -f k8s/ -n marketplace
```
# To Test:
![test](https://github.com/user-attachments/assets/c29b26bc-af7d-4d03-929c-ef91dfd56a67)
```
./ktest_marketplace.sh
```
# To Access Monitoring:
![prometheus](https://github.com/user-attachments/assets/3094d2bb-439c-4666-a579-18184c859218)
```
minikube service monitoring-prometheus -n marketplace
```
![grafana](https://github.com/user-attachments/assets/4ff185da-91e6-4d3c-a738-af7824f8fcc8)
```
minikube service monitoring-grafana -n marketplace
```
# To Access Adminer
![adminer](https://github.com/user-attachments/assets/d2c22149-3080-4874-848f-98ae8961d3a3)
```
minikube service adminer -n marketplace
```
If your Kubernetes service names and credentials are correct, you’ll land on the database dashboard.

Server: postgres-userdb

Username: postgres

Password: password

Database: user_db

Do the same for:

postgres-shopdb / shop_db

postgres-transactiondb / transaction_db

# To Acess Portainer
![portainer](https://github.com/user-attachments/assets/366c8060-b985-43b7-8b4a-166a54092a80)
```
kubectl create namespace portainer
```
Go to: http://marketplace.local:30777/

user: admin
password: portainer123

# To Check Services and Pods
Check all services:
```
kubectl get svc -n marketplace
```
Get pods:
```
kubectl get pods -n marketplace
```

# CHECKLIST PROIECT
```
• existența și integrarea celor minim 3 servicii proprii (0.9p) --> DONE
• existența și integrarea unui serviciu de baze de date (0.3p) --> DONE (fiecare serviciu are baza lui de date)
• existența și integrarea unui serviciu de utilitar DB (0.3p) --> DONE (Adminer)
• existența și integrarea Portainer sau a unui serviciu similar (0.5p) --> DONE (Portainer)
• utilizarea Docker și rularea într-un cluster Docker Swarm (0.6p) --> DONE (Utilizam Docker dar Kubernetes - vezi bonus)
• existența și integrarea Kong sau a unui serviciu similar (0.6p)--> DONE (avem propriul container api gateway)
• existența și integrarea unui sistem de logging sau monitorizare, cu dashboard pentru observabilitate (0.5p)--> DONE (Grafana Prometheus)
• utilizarea de Gitlab CI/CD (sau o unealtă similară) (0.3p) --> DONE (Am facut cu GitHub Actions)
• utilizarea de Kubernetes în loc de Docker Swarm (0.3p bonus). --> DONE (Am folosit Kubernetes)
```
# START ALL
```
kubectl apply -f k8s/ -n marketplace
```
# STOP EVERYTHING NORMALLY
```
kubectl delete -f k8s/ -n marketplace
```
# DELETE THE NAMESPACE (NUKE EVERYTHING, VOLUMES, All Deployments, Services, Pods, PVCs and their backing volumes, ConfigMaps, Secrets, Ingresses, etc.) 
```
kubectl delete namespace marketplace
```
# TO CLEAN AND RESTART EVERYTHING
```
kubectl delete namespace marketplace
kubectl create namespace marketplace
kubectl apply -f k8s/ -n marketplace
```
# TO RUN MINIKUBE DOCKER DAEMON
```
eval $(minikube docker-env)
```
# REBUILD SERVICES WITH DOCKER
```
docker build -t idp_api_gateway ./api_gateway
docker build -t idp_user_service ./user_service
docker build -t idp_shop_service ./shop_service
docker build -t idp_transaction_service ./transaction_service
```
# RESTART KUBERNETES DEPLOYMENTS
```
kubectl rollout restart deployment api-gateway -n marketplace
kubectl rollout restart deployment user-service -n marketplace
kubectl rollout restart deployment shop-service -n marketplace
kubectl rollout restart deployment transaction-service -n marketplace
```
# WIPE USERS/ITEMS/TRANSACTIONS FOR A CLEAR TEST
```
kubectl delete pvc --all -n marketplace
kubectl delete pod -l app=postgres-userdb -n marketplace
kubectl delete pod -l app=postgres-shopdb -n marketplace
kubectl delete pod -l app=postgres-transactiondb -n marketplace
```
# + DOCKER COMPOSE COMMANDS +
```
docker-compose build
docker-compose up -d
docker-compose down
docker-compose down -v
```
# RUN/BUILD ALL SERVICES WITH ONE COMMAND
```
docker-compose up --build -d
```
# TO SEE ALL DOCKER PROCESSES
```
docker ps
```
# TO STOP ALL SERVICES
```
docker-compose down
```
# TO DELETE ALL POSTGRESQL VOLUMES
```
docker-compose down -v 
```
