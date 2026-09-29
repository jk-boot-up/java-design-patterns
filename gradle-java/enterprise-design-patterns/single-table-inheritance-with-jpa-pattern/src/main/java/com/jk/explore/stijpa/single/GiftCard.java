package com.jk.explore.stijpa.single;

import jakarta.persistence.DiscriminatorValue;
import jakarta.persistence.Entity;

/**
 * A product row whose type column says GIFT_CARD.
 */
@Entity
@DiscriminatorValue("GIFT_CARD")
public class GiftCard extends Product {

    private int valuePence;

    protected GiftCard() {
    }

    public GiftCard(String sku, String name, int pence, int valuePence) {
        super(sku, name, pence);
        this.valuePence = valuePence;
    }

    @Override
    public String detail() {
        return "activate £" + valuePence / 100 + " on dispatch";
    }
}
