package com.jk.explore.adapter;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class AcmeShippingSdkTest {

    private final AcmeShippingSdk sdk = new AcmeShippingSdk();

    @Test
    void quotesInWholeCentsGivenPounds() {
        assertEquals(1348L, sdk.fetchCostInCents("94107", 7.71617));
    }

    @Test
    void baseRateAloneIsFourDollarsNinetyNineCents() {
        assertEquals(499L, sdk.fetchCostInCents("94107", 0.0));
    }
}
