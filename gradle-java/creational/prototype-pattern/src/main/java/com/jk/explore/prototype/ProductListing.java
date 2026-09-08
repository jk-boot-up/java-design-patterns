package com.jk.explore.prototype;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

/**
 * A marketplace listing: title, description, category, images, shipping —
 * everything a seller fills in once and then reuses across many near-
 * identical variants of the same product.
 *
 * <p>Assembling one from nothing is real work: choosing a category from a
 * taxonomy, writing compliant boilerplate into the description, picking a
 * shipping profile, setting a return window that matches the category's
 * policy. Most of that is identical across a "wireless earbuds" listing in
 * black, white and blue — only the sku, the title and one attribute differ.
 * {@link #copy()} lets a seller pay that cost once, then clone and tweak.
 *
 * <p>Mutable on purpose. A prototype is a working draft: you copy it, then
 * change the handful of fields that make the new listing different, then
 * publish it. That is a different job from {@code PurchaseOrder} in the
 * builder pattern project, which is assembled once and never changes again.
 */
public final class ProductListing implements Prototype<ProductListing> {

    private String sku;
    private String title;
    private String description;
    private final String category;
    private final String brand;
    private Money price;
    private final List<String> images;
    private final Map<String, String> attributes;
    private final ShippingProfile shippingProfile;
    private final int returnWindowDays;
    private final int warrantyMonths;

    public ProductListing(String sku, String title, String description, String category,
            String brand, Money price, List<String> images, Map<String, String> attributes,
            ShippingProfile shippingProfile, int returnWindowDays, int warrantyMonths) {
        this.sku = Objects.requireNonNull(sku, "sku");
        this.title = Objects.requireNonNull(title, "title");
        this.description = Objects.requireNonNull(description, "description");
        this.category = Objects.requireNonNull(category, "category");
        this.brand = Objects.requireNonNull(brand, "brand");
        this.price = Objects.requireNonNull(price, "price");
        // Deep copies, not the caller's own list and map. This one line is
        // what makes copy() safe below: it reuses this very constructor, so
        // a copy can never end up sharing a mutable collection with the
        // prototype it was copied from.
        this.images = new ArrayList<>(Objects.requireNonNull(images, "images"));
        this.attributes = new LinkedHashMap<>(Objects.requireNonNull(attributes, "attributes"));
        this.shippingProfile = Objects.requireNonNull(shippingProfile, "shippingProfile");
        this.returnWindowDays = returnWindowDays;
        this.warrantyMonths = warrantyMonths;
    }

    @Override
    public ProductListing copy() {
        return new ProductListing(sku, title, description, category, brand, price,
                images, attributes, shippingProfile, returnWindowDays, warrantyMonths);
    }

    public String sku() {
        return sku;
    }

    public void setSku(String sku) {
        this.sku = Objects.requireNonNull(sku, "sku");
    }

    public String title() {
        return title;
    }

    public void setTitle(String title) {
        this.title = Objects.requireNonNull(title, "title");
    }

    public String description() {
        return description;
    }

    public void setDescription(String description) {
        this.description = Objects.requireNonNull(description, "description");
    }

    public String category() {
        return category;
    }

    public String brand() {
        return brand;
    }

    public Money price() {
        return price;
    }

    public void setPrice(Money price) {
        this.price = Objects.requireNonNull(price, "price");
    }

    /**
     * The live, mutable image list. Deliberately not a copy — callers are
     * meant to add to and remove from it directly, the way a seller edits a
     * draft listing. Because {@link #copy()} routes through the
     * constructor, this list is never the same instance as another
     * listing's list, so editing it here can never leak into a sibling.
     */
    public List<String> images() {
        return images;
    }

    /** The live, mutable attribute map — same reasoning as {@link #images()}. */
    public Map<String, String> attributes() {
        return attributes;
    }

    public ShippingProfile shippingProfile() {
        return shippingProfile;
    }

    public int returnWindowDays() {
        return returnWindowDays;
    }

    public int warrantyMonths() {
        return warrantyMonths;
    }

    @Override
    public boolean equals(Object other) {
        if (!(other instanceof ProductListing that)) {
            return false;
        }
        return returnWindowDays == that.returnWindowDays
                && warrantyMonths == that.warrantyMonths
                && sku.equals(that.sku)
                && title.equals(that.title)
                && description.equals(that.description)
                && category.equals(that.category)
                && brand.equals(that.brand)
                && price.equals(that.price)
                && images.equals(that.images)
                && attributes.equals(that.attributes)
                && shippingProfile.equals(that.shippingProfile);
    }

    @Override
    public int hashCode() {
        return Objects.hash(sku, title, description, category, brand, price, images,
                attributes, shippingProfile, returnWindowDays, warrantyMonths);
    }

    @Override
    public String toString() {
        return "ProductListing{sku=%s, title=%s, price=%s, images=%d, attributes=%s}"
                .formatted(sku, title, price, images.size(), attributes);
    }
}
