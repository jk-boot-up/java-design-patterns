# Sidecar on Kubernetes Pattern — UML Sequence Diagrams

Four sequences.

## 1. Compose Needs The Line

![Compose Needs The Line](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant F as compose file
    participant C as checkout
    participant P as proxy
    F->>P: network_mode service:checkout
    C->>P: localhost:8081, reached
    Note over F,P: forget the line, and the call is refused
```

</details>

## 2. Deleting A Pod

![Deleting A Pod](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant U as user
    participant K as control plane
    participant Pod as Pod
    U->>K: delete the Pod
    K->>Pod: stop every container
    K->>K: schedule a new Pod, new address
```

</details>

## 3. A Container Restarts Alone

![A Container Restarts Alone](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant P as proxy
    participant K as kubelet
    P->>P: process dies
    K->>P: restart, restart count 1
    Note over C: checkout restart count stays 0
```

</details>

## 4. Injection

![Injection](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant T as refunds team
    participant A as admission step
    participant K as control plane
    T->>K: create a Pod with one container
    K->>A: about to create it
    A-->>K: add the sidecar proxy
    K->>K: the Pod has two containers
```

</details>

