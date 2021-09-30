## ArgoCD Manifests 

Place the ArgoCD manifests in this directory.

## Commands used
```
--Install argocd in the vagrant box as described on https://argoproj.github.io/argo-cd/getting_started/#1-install-argo-cd:
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

--Expose argocd outside of the vm by creating a node port service.
--This will allow you to access argocd on the browser using the vm ip address assigned in vagrant file.
--The urls are: http://192.168.50.4:30007 and https://192.168.50.4:30008
kubectl apply -f argocd-nodeport.yaml

--Get the argocd automatically generated password. 
--This is the password for admin user which you will use to logon to argocd on the browser:
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

--Create the argocd applications for techtrends project:
kubectl apply -f helm-techtrends-staging.yaml
kubectl apply -f helm-techtrends-prod.yaml

--Argocd defines a new Application resource type. You can list the applications deployed using kubectl:
--All applications are deployed under argocd namespace
kubectl get application -n argocd
NAME                 SYNC STATUS   HEALTH STATUS
techtrends-prod      Synced        Healthy
techtrends-staging   Synced        Healthy

--Once applications are created, logon to argocd and sync each application so that all kubernetes resources can be provisioned.
--With everything working properly, argocd will pull Chart.yaml, templates and values files from the github repo and provision all required resources as defined in the templates folder.

--Each application deploys its resources in a namespace defined in values files for the helm templates:
kubectl get all -n prod
kubectl get all -n staging
```