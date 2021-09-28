## Kubernetes Declarative Manifests 

Place the Kubernetes declarative manifests in this directory.

## Commands used
```
--To start vagrant virtual box vm:
vagrant up

--To ssh to the VM:
vagrant ssh

--To install k3s kubernetes distribution as described on https://k3s.io/
curl -sfL https://get.k3s.io | sh -

--To elevate user permissions (you need to become root user in order to use kubectl):
sudo su -

--Install apparmor (This was required in order for containers to start properly)
zypper install -t pattern apparmor

--Install nano in order to edit manifest files:
zypper install nano

--To check if kubernetes cluster is operational
kubectl get no

--To create namespace.yaml:
kubectl create ns sandbox --dry-run=client -o yaml > namespace.yaml

--To create namespace using manifest:
kubectl apply -f namespace.yaml

--To create deploy.yaml:
kubectl create deploy techtrends -n sandbox --image=andremagalhaes/techtrends:latest -r 1 --port 3111 --dry-run=client -o yaml > deploy.yaml

--Manually append the sections below to yaml to configure resource limits and probes:
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
          requests: 
            memory: "64Mi"
            cpu: "250m"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 3111
        readinessProbe:
          httpGet:
            path: /healthz
            port: 3111

--To create deployment
kubectl apply -f deploy.yaml

--To create service.yaml
kubectl expose deploy techtrends -n sandbox --port 4111 --target-port 3111 --type ClusterIP --protocol TCP --dry-run=client -o yaml > service.yaml

--To create service:
kubectl apply -f service.yaml

--To get all resources in the namespace:
kubectl get all -n sandbox
```

