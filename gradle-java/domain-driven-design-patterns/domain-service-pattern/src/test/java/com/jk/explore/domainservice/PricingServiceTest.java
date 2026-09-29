package com.jk.explore.domainservice;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.jk.explore.domainservice.Model.Basket;
import com.jk.explore.domainservice.Model.Coupon;
import com.jk.explore.domainservice.Model.Customer;
import com.jk.explore.domainservice.Model.Line;
import com.jk.explore.domainservice.Model.Tier;
import java.util.List;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class PricingServiceTest {

    private final PricingService pricing = new PricingService();

    @ParameterizedTest
    @CsvSource({
        "STANDARD, 6000, false, 6000",
        "STANDARD, 6000, true, 5500",
        "GOLD, 6000, false, 5400",
        "GOLD, 6000, true, 5400",
        "GOLD, 4500, true, 4000",
        "STANDARD, 3000, true, 3000"})
    void biggerDiscountWins(Tier tier, long subtotal, boolean coupon, long expected) {
        Basket b = new Basket(List.of(new Line("x", subtotal)));
        assertEquals(expected, pricing.price(new Customer("C", tier), b, coupon ? Coupon.SAVE5 : null).totalPence());
    }

    @ParameterizedTest
    @CsvSource({"STANDARD, 6000", "GOLD, 6000", "GOLD, 4500"})
    void webCopyAgreesWithTheService(Tier tier, long subtotal) {
        Basket b = new Basket(List.of(new Line("x", subtotal)));
        Customer c = new Customer("C", tier);
        assertEquals(pricing.price(c, b, Coupon.SAVE5).totalPence(), Copies.webCheckout(c, b, Coupon.SAVE5));
    }
}
