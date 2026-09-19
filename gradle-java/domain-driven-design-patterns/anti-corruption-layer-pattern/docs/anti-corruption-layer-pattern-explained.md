# Anti-Corruption Layer, Explained

## The pattern in one sentence

An anti-corruption layer is a translator between your model and another system's model, so the other system's ideas never leak into yours.

## The six acts

### Their Model, Everywhere

Four features each read the old record directly, so four places have learnt that Y means in stock and D means discontinued.

```
  what the old system sends: LegacyStockRecord[ITM_CD=MUG-BLUE, QTY_ON_HND=0012, IN_STK_FLG=Y, ITM_STAT=A, LST_CNT_DT=20260114, WHSE_CD=W01, UOM=EA].
  product page: in stock. basket: true. reorder: 38. report: MUG-BLUE 12 A.
  places in the shop that have learnt the codes Y, N, A, D and S: 4.
```

### Their Model, Translated Once

The adapter turns each old record into a stock level with a real number and a meaning. No code crosses it.

```
  StockLevel[sku=MUG-BLUE, available=12, availability=IN_STOCK], can be bought: true.
  StockLevel[sku=MUG-OLD, available=0, availability=DISCONTINUED], can be bought: false.
  StockLevel[sku=TEA-050, available=240, availability=IN_STOCK], can be bought: true.
  no code, and no string pretending to be a number, has crossed the layer.
```

### Bad Data Stops At The Door

A quantity of twelve X fails deep in a report with no sku in the message. The layer refuses it at the door, naming the sku and the problem.

```
  the shortcut, deep in a report: NumberFormatException, and no sku in the message.
  the layer: legacy data for MUG-BLUE: quantity '12X' is not a number.
```

### The Other Side Changes

The old system starts sending H for on hold. The four features each guess. The page says in stock and the basket allows it. The layer decides once: on hold, and it cannot be bought.

```
  the old system starts sending status H for a product on hold.
  the shortcut: page says in stock, basket allows it: true, reorder: 0. four places, four private guesses.
  the layer: ON_HOLD, can be bought: false. one decision, in one place.
```

### What The Layer Costs

The old row has seven fields. The shop uses four. The layer drops three, and any feature that later needs one has to extend the layer and the shop's model.

```
  the old row has 7 fields. the shop uses 4 of them. the layer drops: [LST_CNT_DT, WHSE_CD, UOM].
  the day a feature needs the last count date, the layer must be extended, and the shop's model with it.
```

### What The Layer Protects

The shop speaks four availability words of its own. Replace the old system and only the adapter changes.

```
  the shop's own words: [IN_STOCK, OUT_OF_STOCK, DISCONTINUED, ON_HOLD].
  the old system's words stay behind the layer. replace the old system, write one new adapter, and nothing else changes.
```

## The verdict

Use an anti-corruption layer when your model must stay clean against a system you do not control: legacy, third-party, or a very different one. Put every translation in one adapter, refuse what cannot be translated, and list what you drop. Do not build one for a system whose model already matches yours.

## How to recognise this in code you did not write

- An interface in your domain and an adapter class that implements it against another system.
- Mapping code between two sets of types with different names for the same idea.
- A package for the other system's types that nothing but one class imports.
- Names like `LegacyXAdapter`, `Translator` or `Facade` around an old service.

## Where you have already met this

Any integration with a legacy system or a third-party API, when the team decides not to let its types into the domain.

## When this is too much

When the other system's model already matches yours, or when it is small and stable, a direct call is simpler. The layer earns its place against a model that is foreign, large or changing.
