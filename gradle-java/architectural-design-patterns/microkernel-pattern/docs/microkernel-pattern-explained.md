# Microkernel, Explained

## The pattern in one sentence

A microkernel keeps a small core that only knows how to keep plugins and run them, and puts every feature in a plugin.

## The six acts

### Every Feature Inside

Gift wrap is asked for, and the checkout does not support it. The total is unchanged. To add it, edit the checkout, test all of it again, and release all of it.

```
  gift wrap asked for. supported: false. total: 10000, unchanged.
  to add it, edit the checkout, test all of it again, and release all of it.
```

### A Core And Plugins

The core has two plugins, member discount and shipping fee. A total of ten thousand becomes ninety five hundred. The core knows one interface, and nothing about discounts or fees.

```
  plugins: [member-discount, shipping-fee]. total of 10000: 9500.
  the core knows one interface, Plugin, and nothing about discounts or fees.
```

### A New Feature, No Change

Gift wrap is registered while the system is running. It is started, and the total is ninety eight hundred. Then it is taken away again, stopped, and the total goes back to ninety five hundred. The core was not changed.

```
  gift wrap registered while running. plugins: [member-discount, shipping-fee, gift-wrap]. total: 9800. started: true.
  and taken away again. stopped: true. total: 9500.
```

### A Plugin That Breaks

The loyalty points plugin throws an error. The core records it, and carries on. The other plugins still ran, and the total is ninety five hundred.

```
  total: 9500, so the other plugins still ran.
  recorded: [loyalty-points: loyalty-points lost its connection].
```

### Order Matters

Discount then fee gives ninety five hundred. Fee then discount gives ninety four fifty. The same two plugins, a different price. The core cannot know which is right.

```
  discount then fee: 9500. fee then discount: 9450.
  the same two plugins, a different price. the core cannot know which is right.
```

### The Bill

The interface offers one thing: adjust a total. Plugins want more: the customer's country, and a line on the receipt. If the interface grows, every plugin feels it. If it does not, plugins reach around the core. And a customer's total is now decided by whichever plugins are installed, in some order.

```
  the interface offers one thing: adjust a total. wanted by plugins: [adjust a total, read the customer's country, add a line to the receipt].
  a plugin that needs the country cannot get it. either the interface grows, and every plugin feels it, or plugins reach round the core.
  and a customer's total is now decided by whichever plugins happen to be installed, in some order.
```

## The verdict

Use a microkernel when features come and go, and different customers or teams need different sets. Keep the core tiny and the interface stable. Decide the order of plugins on purpose. Isolate a failing plugin. Do not use it for a system whose features never change.

## How to recognise this in code you did not write

- A `Plugin` or `Extension` interface loaded by name or from a folder.
- `ServiceLoader` in Java.
- IDEs, browsers with extensions, and build tools with plugins.
- OSGi bundles and the Eclipse platform.

## Where you have already met this

Eclipse and IntelliJ, VS Code extensions, Maven and Gradle plugins, and the Linux kernel's loadable modules.

## When this is too much

If the features are few and fixed, plain classes are simpler. A plugin system costs an interface, a lifecycle and a way to order things, and pays off only when the set of features truly varies.
