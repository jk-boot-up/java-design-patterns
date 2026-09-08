package com.jk.explore.templatemethod;

import java.util.List;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The comparison. Each drift in {@link NaiveFulfilment} is pinned here as a
 * passing test that asserts the wrong behaviour, so the difference the
 * pattern makes is a diff between two test files rather than a claim.
 */
@DisplayName("NaiveFulfilment — three copies, already drifting")
class NaiveFulfilmentTest {

    private final StockLedger ledger = new StockLedger().stock("H-100", 10);
    private final SellerApi seller = new SellerApi("Acme Optics").willConfirm("L-900");
    private final NaiveFulfilment naive = new NaiveFulfilment(ledger, "Reading", seller);

    private Order digitalOrder() {
        return Order.addressless("D-1", "sam@example.com",
                List.of(new OrderLine("E-777", "Recipe e-book", Money.pounds(9.99), 1)));
    }

    private Order marketplaceOrder(String sku) {
        return Order.shipped("M-1", "priya@example.com", "12 Mill Lane, Bath",
                List.of(new OrderLine(sku, "Macro lens", Money.pounds(129.00), 1)));
    }

    @Test
    @DisplayName("the warehouse copy is still correct — the trap is not that it is broken")
    void warehouseCopyIsFine() {
        FulfilmentReport report = naive.fulfilFromWarehouse(
                Order.shipped("A-1", "grace@example.com", "London",
                        List.of(new OrderLine("H-100", "Headphones", Money.pounds(89.99), 1))));
        assertEquals(List.of("validate", "reserve", "charge", "pack", "dispatch", "notify"),
                report.stepNames());
    }

    @Test
    @DisplayName("the digital copy runs notify before dispatch")
    void digitalCopyHasTheLastTwoStepsSwapped() {
        assertEquals(List.of("validate", "reserve", "charge", "pack", "notify", "dispatch"),
                naive.fulfilDigital(digitalOrder()).stepNames());
    }

    @Test
    @DisplayName("so the customer's email contains no licence key")
    void digitalEmailHasNoKey() {
        FulfilmentReport report = naive.fulfilDigital(digitalOrder());
        assertEquals(List.of("sam@example.com: Order D-1 is ready to download. "
                + "Key: (not dispatched)"), report.notifications());
    }

    @Test
    @DisplayName("even though the key was minted a moment later")
    void theKeyExistsButNobodyWasTold() {
        assertEquals("KEY-D-1-E-777", naive.fulfilDigital(digitalOrder()).dispatchReference());
    }

    @Test
    @DisplayName("the pattern sends the same email with the key in it")
    void thePatternGetsItRight() {
        FulfilmentReport report = new DigitalFulfilment().fulfil(digitalOrder());
        assertTrue(report.notifications().get(0).contains("KEY-D-1-E-777"));
        assertNotEquals(naive.fulfilDigital(digitalOrder()).notifications(),
                report.notifications());
    }

    @Test
    @DisplayName("the marketplace copy charges before the seller has confirmed")
    void marketplaceCopyChargesFirst() {
        assertEquals(List.of("validate", "charge", "reserve", "pack", "dispatch", "notify"),
                naive.fulfilFromMarketplace(marketplaceOrder("L-900")).stepNames());
    }

    @Test
    @DisplayName("so a refused order still took the customer's money")
    void refusedOrderWasAlreadyCharged() {
        assertThrows(FulfilmentException.class,
                () -> naive.fulfilFromMarketplace(marketplaceOrder("T-410")));
        // The seller was asked only after the charge step had already run.
        assertEquals(1, seller.callCount());
    }

    @Test
    @DisplayName("the pattern asks first and charges second, so nothing is taken")
    void thePatternRefusesBeforeCharging() {
        FulfilmentProcess route = new MarketplaceFulfilment(seller);
        assertThrows(FulfilmentException.class, () -> route.fulfil(marketplaceOrder("T-410")));
    }

    @Test
    @DisplayName("no copy can be given a new step without editing all three")
    void aNewStepWouldHaveToBeAddedThreeTimes() {
        // There is no shared method to add it to. This test documents the
        // shape of the problem: three step lists, produced by three bodies.
        FulfilmentReport a = naive.fulfilFromWarehouse(
                Order.shipped("A-2", "grace@example.com", "London",
                        List.of(new OrderLine("H-100", "Headphones", Money.pounds(89.99), 1))));
        FulfilmentReport b = naive.fulfilDigital(digitalOrder());
        assertNotEquals(a.stepNames(), b.stepNames());
    }
}
