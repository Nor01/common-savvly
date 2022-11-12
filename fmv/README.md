# fmv - Fair Market Value

# Purpose

# Documentation


# Build the Container

```
./build-container.sh
```


# Deploy to Kubernetes

Assuming you have kubectl configured to point to a cluster:

```
kubectl apply -f deployment.yml -n <target namespace>
```



#----------- only once -----------------------
az account list --output table
az account set --subscription "6684ee99-767f-433f-a086-89cf2dafbaea"
az aks get-credentials --resource-group dev-eastus --name savvly-dev-aks-eastus
kubectl config set-context --current --namespace dev

kubectl get pods
kubectl logs 'xxxx'

sudo chmod 666 /var/run/docker.sock

az login --scope https://management.core.windows.net//.default
az acr login -n savvlydeveastus
docker run -it savvlydeveastus.azurecr.io/fmv:7f29269163165b05aec2ef632f812f2df2f1ba93 sh


