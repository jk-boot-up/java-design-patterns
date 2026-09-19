package com.jk.explore.contract;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.junit.jupiter.api.Test;

class ContractTest {

    @Test
    void aRenamedFieldBreaksCheckoutAtRunTime() {
        assertEquals(-1, new Checkout().total(PriceProvider.renamed(), "MUG", 2));
        assertEquals(3200, new Checkout().total(PriceProvider.v1(), "MUG", 2));
    }

    @Test
    void theCurrentReleaseSatisfiesBothContracts() {
        assertEquals(List.of(), Verifier.verify(PriceProvider.v1(), "MUG", Checkout.CONTRACT, Reports.CONTRACT));
    }

    @Test
    void theRenameIsNamedForTheConsumerThatNeedsIt() {
        assertEquals(List.of("checkout expects priceCents (integer): missing"),
                Verifier.verify(PriceProvider.renamed(), "MUG", Checkout.CONTRACT, Reports.CONTRACT));
    }

    @Test
    void addingAFieldIsSafe() {
        assertEquals(List.of(), Verifier.verify(PriceProvider.extraField(), "MUG", Checkout.CONTRACT, Reports.CONTRACT));
    }

    @Test
    void aWrongTypeIsCaught() {
        PriceProvider text = sku -> java.util.Map.of("sku", sku, "priceCents", "1600");
        assertEquals(List.of("checkout expects priceCents (integer): got String"), Verifier.verify(text, "MUG", Checkout.CONTRACT));
    }

    @Test
    void aChangeOfMeaningPassesTheContract() {
        assertEquals(List.of(), Verifier.verify(PriceProvider.pounds(), "MUG", Checkout.CONTRACT));
        assertEquals(32, new Checkout().total(PriceProvider.pounds(), "MUG", 2));
    }
}
