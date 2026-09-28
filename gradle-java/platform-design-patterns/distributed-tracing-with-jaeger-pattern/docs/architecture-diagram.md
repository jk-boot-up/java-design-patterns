# Distributed Tracing with Jaeger Pattern — Architecture Diagram

Two service programs, one HTTP hop between them, and one collector. The only arrow between the services carries an ordinary request with one extra header. Each service sends its own spans to Jaeger, separately; nothing forwards anybody else's.

![Distributed Tracing with Jaeger Pattern — Architecture Diagram](images/architecture-diagram.png)

