# Prototype with Spring Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. A singleton storefront is built. Its constructor asks the container for a listing, and gets one. The constructor never runs again. Caller one asks for a draft and gets that listing, and sets its title. Caller two asks for a draft and gets the very same listing, with caller one's title already on it.

![Prototype with Spring pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as Storefront
    participant C as container
    participant A as caller one
    participant B as caller two
    C->>S: constructor, with one listing
    A->>S: draftInjectedOnce
    S-->>A: the listing
    A->>A: setTitle Blue Mug
    B->>S: draftInjectedOnce
    S-->>B: the same listing, titled Blue Mug
```

</details>

The load-bearing sentence: **a prototype injected into a singleton stops being a prototype.**
