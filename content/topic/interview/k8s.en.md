---
categories:
- Interview
date: 2025-12-06 10:15:30
draft: false
tags:
- K8s
title: SRE Interview Questions Summary | K8s
---

## 1. How Different Modules Communicate with API Server
Various functional modules within the cluster store information in etcd through the API Server. When they need to retrieve and operate on these data, they achieve inter-module information interaction by using the REST interfaces provided by the API Server (using GET, LIST, or WATCH methods).

In Kubernetes, different modules interact with the API Server through standard HTTP/HTTPS requests, ensuring security through authentication and authorization mechanisms, and utilizing the Watch mechanism to implement real-time resource status monitoring and synchronization.

## 2. How kubelet Monitors Worker Nodes
```
Linux Kernel
    ↓
cAdvisor Collects Container and Node Metrics
    ↓
kubelet Processes, Aggregates, and Judges Node Status
    ↓
apiserver + metrics server Aggregate
    ↓
kubectl top / HPA / Scheduler Make Decisions
```

## 3. Considerations for Clusters with Over a Thousand Nodes
Official documentation: https://kubernetes.io/zh-cn/docs/setup/best-practices/cluster-large/

## 4. Content Stored in kubeconfig
Information about clusters, users, namespaces, and authentication mechanisms.

## 5. The Role of kube-proxy
Core Responsibility: Maintain Service Forwarding Rules
kube-proxy listens for changes to Service, Endpoints/EndpointSlice in the API Server, maintains iptables or IPVS rules on the node to achieve traffic forwarding from Service to backend Pods.

### Types
- iptables: Default mode, uses iptables rules to implement Service forwarding.
- IPVS: Based on Linux kernel IPVS for four-layer load balancing, high performance, and fast rule updates.

## 6. Scheduler Scheduling Process
1. Listening and Getting (Listen & Get)
- Scheduler listens to the K8s API Server for unbound Pods
- Through the Informer mechanism, it gets real-time information of Pods and Nodes from the local cache to improve efficiency
2. Preselection Phase (Predicates/Filter)
- Quickly filter out nodes that do not meet the conditions to reduce subsequent calculation volume
- Node resources (CPU, Memory), Node Selector/Affinity/Anti-Affinity, Taints/Tolerations, Pod reservation, etc. Get a list of "candidate nodes" that pass all filters.
3. Priority Selection Phase (Priority)
- Scoring: Score the nodes that pass the preselection to evaluate their "goodness".
- Node resource utilization, load balancing, topology location (such as prioritizing the same rack/region).
Result: Get a node list sorted by score in descending order.
4. Binding Phase (Bind)
- Select the node with the highest score
- Write the selection result to the local cache (Scheduler Cache), record resource usage, and try to reserve resources.
- Asynchronously call the API Server to update the spec.nodeName of the Pod, binding the Pod to the selected node.
- After the Kubelet detects the Pod binding event, it starts creating containers

## 7. POD Startup Process
- Users submit the pod's yaml configuration to the API Server through kubectl or other tools
- After receiving the request, the API Server stores the configuration in etcd
- Scheduler binds the Pod to an appropriate node according to the scheduling strategy
- After the Kubelet detects the Pod binding event, it starts creating containers
  - Pull images
  - Create sandbox, where all containers share network and storage namespaces
  - Call the container runtime to create containers in the pod
  - If there are init containers, the kubelet starts them before the application containers
  - aws-node creates pod network interface, assigns IP address
- After the container starts, the Kubelet sends a status update to the API Server
- After receiving the update, the API Server stores the status in etcd
- When users query the Pod status through kubectl or other tools, the API Server retrieves the latest status from etcd and returns it

## 8. Troubleshooting Failed DNS Resolution for Pods
1. Check Pod Internal and Configuration
- kubectl exec -it <pod> -- nslookup kubernetes.default Cluster internal DNS failure
- kubectl exec -it <pod> -- curl https://www.google.com Upstream DNS or CoreDNS configuration issue
- Check DNS Policy: View the Pod YAML to ensure that the dnsPolicy (such as ClusterFirst) configuration is correct.
Default: Pod inherits the domain name resolution configuration from the node it runs on.
ClusterFirst: Pod first resolves from the cluster internal DNS, and then uses the node DNS configuration if it fails.

2. Check coredns
- Check coredns load
- Check coredns configmap forward

3. Investigate kube-proxy
DNS traffic is Pod → kube-proxy → CoreDNS Pod

4. Check CNI Network Plugin

5. Whether Istio / Linkerd / Envoy sidecar is used

## 9. Common Pod Scheduling Methods
1. Default Scheduler
2. Node Selector
3. Affinity and Anti-Affinity
4. Taints and Tolerations
5. Resource Requests and Limits
6. Pod Topology Spread Scheduling: Uniform distribution across different nodes/racks
7. Preemption Scheduling

## 10. The Purpose of the Pause Container
The only role of the Pause container is to ensure that the Pod will not be deleted even if there are no containers running in it, because there is still a Pause container running at this time.
- Network namespace isolation
- Process isolation
- Resource isolation
- Lifecycle management

## 11. Possible Causes and Troubleshooting for Failed Pod Health Checks
- Probe configuration issues
- Application not started/responding slowly: Exceeds initialDelaySeconds, process exits (CrashLoopBackOff)
- Resource constraints: CPU/Memory insufficient, causing Kubelet to fail to run health checks
- Network issues: Container cannot access external services, such as DNS resolution failure
- Unavailable dependencies: Database, cache, etc. dependent services are not ready
- Database, cache, etc. dependent services are not ready

Troubleshooting Approach
- kubectl describe pod
- kubectl logs
- Check health check configuration
- Enter the container internally to troubleshoot
  - Use curl, wget to test the HTTP probe path.
  - netstat -tulnp or ss -tulnp to confirm that the port is listening
- Check resources and nodes

## 12. How to Troubleshoot Inability to Access Pods

## 13. Common States of Pods
Pod Phase

- Running
- Succeeded (Job completed, CronJob completed)
- Failed (Program crash, container startup failed)
- Pending (Resource insufficient, NodeSelector no match, image pull slow)
- Unknown (Kubelet cannot report status, node offline, network interruption)

Creation/Scheduling Related
- ContainerCreating (Container is being created, pulling images)
- PodInitializing (Container is initializing, executing init container)
- ImagePullBackOff (Image pull failed, such as authentication issue, image does not exist)
- ErrImagePull (Same as above, earlier than BackOff)
- CreateContainerConfigError (Container creation configuration error, such as mount volume does not exist)
- Error (Container exits with a non-zero exit code, but may not trigger failure due to restart policy)

Running Abnormally
- CrashLoopBackOff (Container crashes, kubelet restarts the container according to the backoff strategy, default 10s)
- OOMKilled (Container exceeds memory limit, forcibly killed by kubelet)
- BackOff (After multiple failures, enter the avoidance state, such as init container failure)
- CrashLoopBackOff (Main container keeps crashing and restarting)
- CreateContainerConfigError (Container creation configuration error, such as mount volume does not exist)
- Error (Container exits with a non-zero exit code, but may not trigger failure due to restart policy)

Termination/Completion
- Terminating (Container is terminating, such as deleting pod)
- Completed (Container exits normally, such as the main container exits)
- Failed (Container exits with a non-zero exit code, and the restart policy is Never)