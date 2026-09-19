# Strategy with Spring Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. At startup the container creates the four rule beans and puts them in a map. It then builds the selected shipping component, passing the map and the configured name. The component looks the name up. If it finds a rule it keeps it. If it finds nothing, it throws, and the application does not start.

![Strategy with Spring pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as container
    participant R as four rules
    participant S as SelectedShipping
    C->>R: create the beans
    C->>S: constructor(map, name)
    S->>S: rules.get(name)
    alt found
        S-->>C: ready
    else not found
        S-->>C: IllegalArgumentException
    end
```

</details>

The load-bearing sentence: **a wrong name is found at startup, not at checkout.**
