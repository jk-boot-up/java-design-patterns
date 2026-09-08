package com.jk.explore.proxy;

/**
 * A protection proxy. Wraps any other {@link ProductImage} -- a real one, or
 * another proxy -- and refuses to delegate {@link #render()} unless the
 * caller holds {@link Role#CATALOG_ADMIN}. Used for assets that must not
 * reach shoppers yet: unreleased products, embargoed launches, artwork a
 * supplier has not cleared.
 *
 * <p>Composable with {@link LazyProductImage}: wrapping one around the other
 * gets lazy loading and access control at once, neither aware the other
 * exists.
 */
public final class RestrictedProductImage implements ProductImage {

    private final ProductImage image;
    private final Role role;

    public RestrictedProductImage(ProductImage image, Role role) {
        this.image = image;
        this.role = role;
    }

    @Override
    public String render() {
        if (role != Role.CATALOG_ADMIN) {
            throw new SecurityException("Only catalog admins may view " + image.sku());
        }
        return image.render();
    }

    @Override
    public String sku() {
        return image.sku();
    }
}
