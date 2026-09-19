# Pipes and Filters, Explained

## The pattern in one sentence

Pipes and filters breaks a job into small independent steps, filters, joined end to end by pipes, so each step does one thing and steps can be added, swapped or reused.

## The six acts

### One Method Does It All

One loop does five jobs. Six lines go in and three come out, and the three dropped left no trace of why.

```
  6 lines in, 3 out: [ada: 2 x MUG-BLUE = £19.20, ben: 1 x ESP-001 = £360.00, fay: 3 x TEA-050 = £28.80].
  5 separate jobs in one loop. the six lines came in, and the three that were dropped left no trace of why.
```

### Small Steps, Joined

The same job is five steps: parse, validate, price, tax, format. The price step on its own turns one parsed line into a priced one, with no need for the others.

```
  the pipeline: parse | validate | price | uk-tax | format.
  the price step on its own, for one parsed line: Priced[customer=ada, sku=MUG-BLUE, quantity=2, netPence=1600].
  each step can be run, and tested, without the others.
```

### Swap A Step, Add A Step

Swapping the UK tax step for an EU one changes the total from nineteen twenty to nineteen thirty six. A new step is added in the middle, and no other step changed.

```
  uk: [ada: 2 x MUG-BLUE = £19.20].
  eu: [ada: 2 x MUG-BLUE = £19.36].
  a new step added in the middle: parse | validate | not-ben | price | uk-tax | format. no other step changed.
```

### Bad Lines Are Rejected, And The Rest Go On

Three lines pass. Three are rejected, each with the step that dropped it and the reason, and the good lines carry on.

```
  3 orders out:
    ada: 2 x MUG-BLUE = £19.20
    ben: 1 x ESP-001 = £360.00
    fay: 3 x TEA-050 = £28.80
  3 rejected, each with the step and the reason:
    parse: quantity 'twelve' is not a number
    validate: di asked for 50 of MUG-BLUE
    parse: 'ed, TEA-050' does not have three fields
```

### Streaming, Or One Stage At A Time

With ten thousand lines, streaming holds one item at once and running one stage at a time holds twenty thousand. The results are the same.

```
  10000 lines. items held at once: streaming 1, one stage at a time 20000.
  the results are the same: true. only the memory differs.
```

### The Bill: The Steps Must Agree On The Shape

Steps that pass loose maps fail at run time when one calls a field qty and the next asks for quantity. Typed items catch that when compiling, but every step now depends on the type before it. And an error appears in the step that noticed, not the one that caused it.

```
  steps passing loose maps: one step calls the field qty and the next asks for quantity. it fails at run time, in the later step: NumberFormatException.
  with typed items, that mistake does not compile. but every step now depends on the type before it, and changing one means changing its neighbours.
  and when a line is wrong, the error appears in the step that noticed, which may be far from the step that caused it.
```

## The verdict

Use pipes and filters when a job is a sequence of independent transformations, when steps will change or be reused, and when items can be handled one at a time. Type the items between steps, report rejects with the step and the reason, and stream where the data is large. Keep a pipeline short enough to read. Do not use it where steps need the whole batch.

## How to recognise this in code you did not write

- A chain of `.map(...).filter(...)` on a stream.
- A Unix pipeline with `|`.
- Spring Batch's reader, processor and writer, and Camel routes.
- A list of processors, each with one `process` method.

## Where you have already met this

`java.util.stream`, shell pipelines, servlet filters, ETL tools, and image and audio processing chains.

## When this is too much

For a job with two simple steps, a pipeline is more structure than the job. Where every step needs the whole batch, a pipeline gains nothing.
