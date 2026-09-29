# Context Map and Shared Kernel, Explained

## The pattern in one sentence

A context map records how the parts of a system relate; a shared kernel is a
tiny model two parts share and change only together.

## The 5 acts

### 1. Two copies of an address

In the `before` package, sales has `SalesAddress` with a flat, and shipping
has `ShippingAddress` without one. A converter copies between them. Priya
types "Flat 2, 4 Mill Lane, Leeds"; the shipping label reads "4 Mill Lane,
Leeds". The flat was lost between the two contexts.

### 2. A shared kernel

A small `kernel` package holds `Address` and `Money`, owned by both teams.
Sales places `ORD-1` for £38.00 with a kernel address; shipping prints the
label from the same address: "Flat 2, 4 Mill Lane, Leeds, insured for
£38.00". The converter is gone.

### 3. The context map

`ContextMap.RELATIONSHIPS` writes down how the contexts relate: the catalogue
is sales' supplier (sales asks it for prices); sales and shipping share the
kernel. Shipping does not know that sales exists.

### 4. The map, checked

The map also lists what each context may import. `ContextMap.surprises` reads
every source file: zero imports the map does not allow. When someone adds an
import of `sales.Sales` to shipping, the check reports it, so the drawing and
the code cannot drift apart.

### 5. The bill

A shared kernel changes slowly: adding a postcode to `Address` needs both
teams to agree, test and release together. The answer is to keep it tiny,
here two classes, and leave everything else inside its own context.

## The verdict

Draw a context map as soon as a system has more than one team or model, and
keep it as code that is checked. Share a kernel only for the few concepts that
must match exactly, keep it tiny, and change it by agreement.

## How to recognise this in code you did not write

- A small shared `kernel`, `common` or `shared` package used by two areas.
- Architecture tests listing which packages may import which.
- Diagrams with arrows labelled upstream, downstream, conformist or ACL.

## Where you have already met this

- A shared `common` or `core` library used by two services.
- Context map diagrams in architecture documents, with arrows marked upstream and downstream.
- ArchUnit or module rules that say which packages may depend on which.
