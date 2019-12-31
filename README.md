# kanu-vmware

Steps to take -

1. Git clone the repo in a directory. 
git clone https://github.com/kkalra24/kanu-vmware.git

2. Build the docker container
docker build -t vmwareapp:latest .

3. Apply the manifest file vmwarejob.yaml using kubectl to create a job in kuberenetes cluster
kubectl apply -f vmwarejob.yaml

4. Check job/pod are up 
kubectl get jobs
kubectl get pods

5. Check the logs
kubectl get logs
