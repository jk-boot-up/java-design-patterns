# Strategy with Spring, Explained

## The pattern in one sentence

In Spring, the strategies are beans of one interface, and the container collects them into a map.

## What is new here

The pattern is [Strategy](../strategy-pattern). This page is only what Spring Boot adds.

### Spring Finds The Strategies

The container injects a map of every rule, keyed by bean name.

```
  rules found: [distance, flat, freeOverThreshold, weightBanded].
  the keys are bean names, chosen in the @Component annotations.
```

### The Same Shipments, Every Rule

The same three shipments priced under all four rules, and an unknown name at run time is refused with the list of known names.

```
  distance           light 2.99  middle 3.49  heavy 4.99
  flat               light 4.99  middle 4.99  heavy 4.99
  freeOverThreshold  light 4.99  middle 4.99  heavy 0.00
  weightBanded       light 2.99  middle 4.99  heavy 8.99
  a name at run time that is unknown: unknown shipping rule 'teleport'; known: [distance, flat, freeOverThreshold, weightBanded]
```

### Configuration Chooses

A property picks the rule. An unknown name stops the application from starting.

```
  shipping.rule=distance: the heavy shipment costs 4.99.
  shipping.rule=teleport: the application does not start. shipping.rule is 'teleport' but the rules are [distance, flat, freeOverThreshold, weightBanded]
```

### Four Beans, One Interface

A class that asks for the interface alone, not the map, stops the application, because the container will not choose among four.

```
  a class that asks for a single ShippingCostRule: expected a single bean but found 4.
```

### A Fifth Rule

A new rule appears in the map, and the checkout is unchanged. The demo registers it by hand so the default run stays at four; a component-scanned class is found the same way.

```
  rules found: [distance, express, flat, freeOverThreshold, weightBanded].
  express quotes the heavy shipment at 9.99. CheckoutService did not change.
```

### A Default When Nobody Chooses

Mark one bean primary and a class that asks for the interface alone gets it. The map still holds all four.

```
  with the flat rule marked primary, the same class starts, and prices the heavy shipment at 4.99.
  the map still holds all four: [distance, flat, freeOverThreshold, weightBanded].
```

## The verdict

Inject the map, name the beans explicitly, check the configured name at startup, and mark a primary where one default is needed.

## How to recognise this in code you did not write

- `Map<String, SomeInterface>` in a constructor.
- `List<SomeInterface>` in a constructor, used to find the first that applies.
- `@Qualifier` or `@Primary` next to an interface.

## Where you have already met this

Payment providers, message handlers, and export formats chosen by a name.

## When this is too much

Two rules that never change need no container. A plain conditional is easier to read.
