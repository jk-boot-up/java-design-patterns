package com.jk.explore.proxy;

/**
 * The other trap: without a protection proxy, every screen that shows
 * catalog imagery re-implements the same role check inline -- the category
 * page, the search results, the quick-view modal, the PDF export -- coupling
 * each one to {@link Role} and to the exact wording of the denial, and
 * leaving the rule one forgotten copy away from being wrong.
 */
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
