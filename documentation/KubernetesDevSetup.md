# Purpose

To set up `kubectl` to access the development AKS instance in Azure, follow the following steps.


# Pre-requisites

1. Ensure you have the Azure CLI (`az` command) installed and configured in your operating system. Note that you may need to set your default subscription to `6684ee99-767f-433f-a086-89cf2dafbaea` prior to running the following commands.

1. Ensure that you have the Kubernetes CLI installed. (No need to configure it, just install it.)

# Configure `kubectl` for AKS

## Use `az` to set up the `kubectl` configuration:

```
az aks get-credentials --resource-group dev-eastus --name savvly-dev-aks-eastus
```

`kubectl` should now be configured. You can test it using:

```
kubectl get namespaces
```

You should see a `dev` namespace, among a few others.


## Set the default namespace

This step isn't necessary, but it's annoying to add `-n dev` to every `kubectl` command. You can set it as the default by:

```
kubectl config set-context --current --namespace dev
```

# Using `kubectl`

## Get a List of Deployments

Deployments in Kubernetes are definitions of how to run a given "pod". A "pod" is the actual running container set (think of it as an instance of a deployment.) If you want to see the deployments:

```
kubectl get deployments
```

## Get a List of Cron Jobs

Kubernetes allows scheduling jobs similar to Cron. In fact, the job type is `CronJob`. You can get a list of them using: 

```
kubectl get cronjobs
```

Logs can be found by getting the podlist and following the procedures below. Logs are kept for the past 3 runs of the job.


## Get a List of Running Pods

If you want to see actual running containers, you can get a list of the running pods:

```
kubectl get pods
```

## Get Container Logs

In order to see the logs, you have to know which container you're asking for. You'll use `kubectl get pods` to find the one you are looking for, and then `kubectl logs` to actually fetch them.


```
kubectl get pods
kubectl logs <full pod name>
```

Note that you can add a `-f` switch to follow ("tail") the logs.



