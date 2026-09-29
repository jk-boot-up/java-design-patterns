package com.jk.explore.stijpa.single;

import jakarta.persistence.DiscriminatorValue;
import jakarta.persistence.Entity;

/**
 * A product row whose type column says ELECTRONICS.
 */
@Entity
@DiscriminatorValue("ELECTRONICS")
public class Electronics extends Product {

    private int warrantyYears;

    protected Electronics() {
    }

    public Electronics(String sku, String name, int pence, int warrantyYears) {
        super(sku, name, pence);
        this.warrantyYears = warrantyYears;
    }

    @Override
    public String detail() {
        return warrantyYears + "-year warranty card";
    }
}
