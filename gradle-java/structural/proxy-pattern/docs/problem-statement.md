# The Problem

A product listing needs to show high-resolution images. Decoding one from
disk (or fetching it over a network) is genuinely expensive — imagine it
takes real time and real memory, even though this project models that cost
with a simple counter instead of an actual delay so the tests stay fast.
On top of that, some images are only meant to be seen by admins, not by
every shopper who opens the listing.

Two separate problems, two separate naive traps.

## Trap 1: loading everything, whether you need it or not

```java
public final class NaiveProductListing {

    private final List<HighResolutionProductImage> images = new ArrayList<>();

    public NaiveProductListing(List<String> skus) {
        for (String sku : skus) {
            images.add(new HighResolutionProductImage(sku)); // eager, always
        }
    }

    public String renderFirst() {
        return images.get(0).render();
    }
}
```

Construct a `NaiveProductListing` with ten SKUs, call `renderFirst()`,
and you have paid the full loading cost of all ten images to look at one.
The class has no way to defer the expense — the moment you have a
`HighResolutionProductImage` reference, it has already been built. A listing
screen that shows thumbnails first and loads full resolution only on click
cannot be built this way without gutting the class.

## Trap 2: scattering the same access check everywhere

```java
public final class NaiveAdminImageViewer {

    private final ProductImage image;

    public NaiveAdminImageViewer(ProductImage image) {
        this.image = image;
    }

    public String view(Role role) {
        if (role != Role.CATALOG_ADMIN) {
            throw new SecurityException("Only catalog admins may view " + image.sku());
        }
        return image.render();
    }
}
```

This works, but only for callers that go through `NaiveAdminImageViewer`.
Add a second screen — a thumbnail grid, a slideshow, a search results page — and
each one either duplicates the `if (role != Role.CATALOG_ADMIN)` check or forgets
it entirely. The permission rule lives in every call site instead of in
one place, and nothing stops a new caller from talking to a `ProductImage`
directly and skipping the check altogether.

## What both traps have in common

In both cases, the client is forced to deal with a concern that has
nothing to do with *rendering an image* — either lifecycle management
(when does the expensive object get built?) or access control (who is
allowed to see it?). The client just wants to call `render()`. Everything
else should happen behind that same interface, invisibly. That is exactly
what the Proxy pattern is for: a stand-in that implements the same
interface as the real thing, and only it knows about the loading strategy
or the access rule.
