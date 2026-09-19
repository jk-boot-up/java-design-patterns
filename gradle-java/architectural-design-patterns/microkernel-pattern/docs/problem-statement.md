# Problem Statement

## The scenario

The checkout has a member discount and a shipping fee. Now the marketing team wants gift wrap, then loyalty points, then more.

## The naive version

Put every feature inside the checkout, with a switch that grows by one case each time.

```
  gift wrap asked for. supported: false. total: 10000, unchanged.
  to add it, edit the checkout, test all of it again, and release all of it.
```

## What this project must deliver

A checkout with features built in, unable to add gift wrap without an edit; a kernel with a Plugin interface; plugins added and removed at run time, and started and stopped; a plugin that throws, recorded and skipped; two orders of the same plugins giving two prices; and a narrow interface.
