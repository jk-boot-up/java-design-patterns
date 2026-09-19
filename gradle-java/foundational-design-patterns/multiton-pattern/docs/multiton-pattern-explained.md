# Multiton, Explained

## The pattern in one sentence

A multiton is a singleton with a key: it keeps exactly one instance for each key, and hands back that same instance every time the key is asked for.

## The six acts

### A New One Each Time

Two callers each made a UK warehouse. They are not the same object. One has stock ninety, the other a hundred. The shop now believes two different things about one warehouse.

```
  two callers each made a UK warehouse. same object: false. A has stock 90, B has 100.
  the shop now believes two different things about one warehouse.
```

### One Per Region

Asked for the UK twice, it is the same object. Asked for the EU, it is a different one. Created so far: two.

```
  asked for UK twice: same object: true. asked for EU: same as UK: false. created so far: 2.
```

### Shared, So They Agree

One part of the shop reserved ten in the UK. Another part, asking for the UK, sees stock ninety. The EU warehouse has a hundred.

```
  one part of the shop reserved 10 in the UK. another part, asking for UK, sees stock 90. the EU warehouse has 100.
```

### A Fixed Set Of Keys

Asked for Mars, it is refused: no warehouse in Mars. Instances held: three.

```
  asked for MARS: refused, "no warehouse in MARS". instances held: 3.
```

### Two Threads, One Region

Look first, create second, with no lock: both threads looked before either created. Not the same object, and two were created. With an atomic create if absent, eight threads at once get the same object, and one is created.

```
  look first, create second, no lock: both threads looked before either created. same object: false. created: 2.
  with an atomic create-if-absent: 8 threads at once, same object: true. created: 1.
```

### The Bill

One test reserved thirty. The next test starts, and asks for the UK: stock seventy, not a hundred. State leaks from one test to the next. The instances live as long as the program does, and nothing ever lets one go. And any code can reach any warehouse from anywhere, so who changed the stock is hard to say.

```
  one test reserved 30. the next test starts, and asks for UK: stock 70, not 100. state leaks from one test to the next.
  the instances live as long as the program does: held 1, and nothing ever lets one go.
  and any code can reach any warehouse from anywhere, so who changed the stock is hard to say.
```

## The verdict

Use a multiton when there must be exactly one object for each of a small fixed set of keys. Create with an atomic create-if-absent. Give tests a way to reset. And prefer passing the object in, when you can, so that the sharing is visible.

## How to recognise this in code you did not write

- A static `Map` of instances and a `getInstance(key)` method.
- `ConcurrentHashMap.computeIfAbsent` used to create on demand.
- `Currency.getInstance(code)`, `Locale` constants and `Charset.forName`.
- Enums, which are a multiton the language provides.

## Where you have already met this

`java.util.Currency`, logger factories that return one logger per name, and enum constants.

## When this is too much

If an enum can name the fixed set, use an enum. If the object can be passed in, pass it in. A multiton is global state with a key.
