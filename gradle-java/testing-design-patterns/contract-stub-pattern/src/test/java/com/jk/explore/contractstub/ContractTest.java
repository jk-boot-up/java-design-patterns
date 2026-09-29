package com.jk.explore.contractstub;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Map;
import org.junit.jupiter.api.Test;

/**
 * Both halves of the pattern: the consumer's tests against the stub, and the provider's check.
 */
class ContractTest {

    private final Contract contract = Contract.payments();

    @Test
    void consumerSideUsesTheStub() {
        Checkout checkout = new Checkout(new ContractStub(contract));
        assertEquals("order confirmed", checkout.pay("20.00", "4000000000000001", "GBP"));
    }

    @Test
    void providerSideHonoursTheContract() {
        assertTrue(ProviderVerifier.mismatches(contract, new RealPaymentService(1)).isEmpty());
    }

    @Test
    void renameIsCaught() {
        assertEquals(3, ProviderVerifier.mismatches(contract, new RealPaymentService(2)).size());
    }

    @Test
    void unlistedRequestIsRefused() {
        assertThrows(IllegalStateException.class,
                () -> new ContractStub(contract).charge(Map.of("amount", "5.00", "card", "x", "currency", "GBP")));
    }
}
