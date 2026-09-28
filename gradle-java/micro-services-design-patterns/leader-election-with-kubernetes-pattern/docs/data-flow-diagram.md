# Leader Election with Kubernetes Pattern — Data Flow Diagram

How one copy decides, every second or so, whether it leads. Note where the clock is read: in the copy, never in the API server.

![Leader Election with Kubernetes Pattern — Data Flow Diagram](images/data-flow-diagram.png)

