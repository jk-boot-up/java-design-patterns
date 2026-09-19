# Lazy Load, Explained

## The pattern in one sentence

Load the object you asked for now, and load the rest when it is asked for.

## Four variants

A reader will meet all four in real code.

**Lazy initialisation.** A field is empty until a getter is called.
**Virtual proxy.** A stand-in with the same interface loads the real object on first use.
**Value holder.** The caller knows it holds a promise and asks for the value.
**Ghost.** An object created with only its id, which loads everything the first time anything is asked of it.

```
TWO. Four ways to load later.
  lazy initialisation: before 0, after first use 1 (Customer 1), after second use 1
  virtual proxy:       before 0, after first use 1 (Customer 2), after second use 1
  value holder:        before 0, after first use 1 (Customer 3), after second use 1
  ghost:               before 0, after first use 1 (Customer 4), after second use 1
```

## The bill

This bill is heavy, and it is not softened.

**N+1.** You have replaced one large query with many small ones. A page of
twenty orders, each showing its customer, costs twenty-one queries.

```
THREE. The bill: N+1.
  lazy:    21 queries (one for the orders, one for each customer)
  batched: 2 queries
```

In a real system every query is a round trip, so the lazy page is slower than
the eager version it replaced.

**A field access is now I/O.** It can be slow, and it can fail.

```
FOUR. A field access is now I/O, so it can fail.
  asking for a customer's name threw: the database failed to read: SELECT customers id=1
```

**The session can be gone.** The object is passed somewhere its session no
longer exists, and the load fails at the point of use, not at the point of
loading.

```
FIVE. The session closes first — it fails at the point of use.
  the page asks for the name: cannot load customers id=1: the session is closed
```

## Where you have already met this

That last failure has a name in Hibernate: `LazyInitializationException`. It
is one of the most-searched Java errors there is, and it is exactly act five:
a lazy object whose session has closed. The Hibernate project in this
category produces it on purpose.

## When this is too much

If you almost always need the related data, lazy loading only adds queries.
It earns its place when the related data is large and rarely needed.
