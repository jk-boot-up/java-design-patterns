# Singleton Pattern — UML Sequence Diagram

Shows two runtime flows side by side: the enum singleton rejecting both
attacks, and the classic private-constructor shape falling to both.

![Singleton pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    actor Client as OrderSequenceGeneratorDemo
    participant Good as OrderSequenceGenerator (enum)
    participant Legacy as LegacyOrderSequenceGenerator

    Note over Client,Good: JVM created INSTANCE once, during class loading

    Client->>Good: INSTANCE.nextOrderNumber()
    Good-->>Client: "ORD-000001"

    Client->>Good: reflection: getDeclaredConstructor(String, int)
    Client->>Good: constructor.newInstance("FORGED", 99)
    Good-->>Client: throws IllegalArgumentException

    Client->>Good: serialize INSTANCE, then deserialize
    Good-->>Client: same INSTANCE reference back

    Note over Client,Legacy: getInstance() looks identical to callers — until attacked

    Client->>Legacy: getInstance()
    Legacy-->>Client: the shared instance

    Client->>Legacy: reflection: getDeclaredConstructor()
    Client->>Legacy: constructor.newInstance()
    Legacy-->>Client: a second, independent instance

    Client->>Legacy: serialize the shared instance, then deserialize
    Legacy-->>Client: a third, independent instance
```

</details>

## Notes

- The two flows are drawn together deliberately: the calls a well-behaved
  client makes (top three arrows on each participant) are identical in
  shape. The difference only appears once something adversarial —
  reflection, serialization — is thrown at each one.
- `OrderSequenceGenerator.INSTANCE` never appears on the right-hand side of
  an assignment inside this project's own code. It cannot; there is no
  constructor call to make one.
- Compare with
  [`../../prototype-pattern/docs/uml-diagram.md`](../../prototype-pattern/docs/uml-diagram.md).
  There, the interesting sequence is one object producing a second,
  independent one on purpose. Here, the interesting sequence is an attempt
  to produce a second instance *despite* the type actively working to
  prevent it.
