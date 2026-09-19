package com.jk.explore.stranglerfig.domain;

/** What a checkout produced. */
public record Result(Pricing pricing, boolean stockReserved, String chargeId, boolean emailSent) {

    public boolean succeeded() {
        return stockReserved && chargeId != null && emailSent;
    }
}
