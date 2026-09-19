package com.jk.explore.typeobject;

/** What kind of thing a product is, as data. Any field left empty is taken from the parent type. */
public class ProductType {

    private final String name;
    private final ProductType parent;
    private Integer taxPercent;
    private Integer returnDays;
    private Integer shippingCents;
    private boolean requiresSerial;

    public ProductType(String name, ProductType parent, Integer taxPercent, Integer returnDays, Integer shippingCents) {
        this.name = name;
        this.parent = parent;
        this.taxPercent = taxPercent;
        this.returnDays = returnDays;
        this.shippingCents = shippingCents;
    }

    public String name() {
        return name;
    }

    public int taxPercent() {
        return taxPercent != null ? taxPercent : parent.taxPercent();
    }

    public int returnDays() {
        return returnDays != null ? returnDays : parent.returnDays();
    }

    public int shippingCents() {
        return shippingCents != null ? shippingCents : parent.shippingCents();
    }

    public boolean requiresSerial() {
        return requiresSerial;
    }

    public ProductType requireSerial() {
        this.requiresSerial = true;
        return this;
    }

    public void setTaxPercent(int percent) {
        this.taxPercent = percent;
    }
}
