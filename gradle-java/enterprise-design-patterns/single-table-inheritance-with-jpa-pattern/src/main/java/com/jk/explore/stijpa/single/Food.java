package com.jk.explore.stijpa.single;

import jakarta.persistence.DiscriminatorValue;
import jakarta.persistence.Entity;

/**
 * A product row whose type column says FOOD.
 */
@Entity
@DiscriminatorValue("FOOD")
public class Food extends Product {

    private String bestBefore;

    protected Food() {
    }

    public Food(String sku, String name, int pence, String bestBefore) {
        super(sku, name, pence);
        this.bestBefore = bestBefore;
    }

    @Override
    public String detail() {
        return "best before " + bestBefore;
    }
}
