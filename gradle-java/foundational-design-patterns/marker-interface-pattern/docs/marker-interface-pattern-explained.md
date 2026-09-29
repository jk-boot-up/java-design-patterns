# Marker Interface, Explained

## The pattern in one sentence

A marker interface is an empty interface whose name tells code and the
compiler something about a type, replacing free-text tags that can be
misspelt.

## The 5 acts

### 1. Free-text tags

`TaggedProduct` keeps care instructions as a list of strings. The packer looks
for exactly "perishable". The first milk gets ice packs. The second, tagged
with a capital P, and the cream, tagged with a spelling mistake, go out in a
plain box. Nothing complained.

### 2. A marker interface

`Perishable` and `Fragile` are empty interfaces. `Milk` implements
`Perishable`, `Mug` implements `Fragile`, `Kettle` implements neither. The
packer asks `instanceof`: milk gets ice packs, the mug bubble wrap, the kettle
a plain box. A misspelt interface name simply would not compile.

### 3. The compiler checks

`Packer.sendChilled` takes a `Perishable` parameter. Milk is accepted by the
chilled van. Writing `sendChilled(kettle)` does not compile, because a kettle
is not `Perishable`. The rule is enforced before the program runs.

### 4. The mark is passed on

Another team writes `YoghurtMultipack extends Yoghurt`. They never mention
`Perishable`, but `Yoghurt` implements it, so the multipack is perishable too
and gets ice packs.

### 5. The bill

A marker answers yes or no. It cannot say how cold: that needs a method, which
makes it no longer a marker, or an annotation like `@Chilled(maxC = 5)`. And a
subclass cannot take the mark off: a dried yoghurt snack extending `Yoghurt`
would still get ice packs.

## The verdict

Use markers for simple yes-or-no facts about a type that the compiler should
check, especially as method parameter types. Use an annotation when the fact
needs values or is read by frameworks.

## How to recognise this in code you did not write

- `implements Serializable`, `Cloneable`, `RandomAccess`.
- Interfaces with no methods whose name is an adjective.
- Methods whose parameter type is such an interface.

## Where you have already met this

- `java.io.Serializable`, `java.lang.Cloneable` and `java.util.RandomAccess`.
- `java.rmi.Remote`, marking objects that can be called over the network.
- Annotations such as `@FunctionalInterface` and `@Entity`, the other way to mark a type.
