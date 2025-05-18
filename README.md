# =============================== KUBERNETES COMMANDS ===============================

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
```
./ktest_marketplace.sh
```
# To Access Monitoring:
```
minikube service monitoring-prometheus -n marketplace
minikube service monitoring-grafana -n marketplace
```
# To Access Adminer
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
```
kubectl create namespace portainer
```
Go to: http://marketplace.local:30777/

user: admin
password: portainer123

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
# CHECK EVERYTHING IS OK, CHECK PODS
Check all services:
```
kubectl get svc -n marketplace
```
Get pods:
```
kubectl get pods -n marketplace
```
# WIPE USERS/ITEMS/TRANSACTIONS FOR A CLEAR TEST
```
kubectl delete pvc --all -n marketplace
kubectl delete pod -l app=postgres-userdb -n marketplace
kubectl delete pod -l app=postgres-shopdb -n marketplace
kubectl delete pod -l app=postgres-transactiondb -n marketplace
```
# =============================== DOCKER COMPOSE COMMANDS ===============================
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

