package com.jk.explore.staticfactory;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.params.provider.Arguments.arguments;

import java.util.stream.Stream;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

@DisplayName("Discount — named creation, shared instances, hidden classes")
class DiscountTest {

    private static final Order ORDER =
            new Order("ORD-4001", "CUST-001", Money.pounds(120.00), Money.pounds(4.99));

    static Stream<Arguments> coupons() {
        return Stream.of(
                arguments("SAVE10", "10% off", Money.pounds(12.00)),
                arguments("SAVE25", "25% off", Money.pounds(30.00)),
                arguments("FIVEROFF", "£5.00 off", Money.pounds(5.00)),
                arguments("FREESHIP", "Free shipping", Money.pounds(4.99)),
                arguments("", "No discount", Money.zero()));
    }

    @ParameterizedTest(name = "{0} -> {1} saves {2}")
    @MethodSource("coupons")
    @DisplayName("one call site, one line of code, five different classes")
    void couponCodeChoosesTheImplementation(String code, String description, Money saving) {
        Discount discount = Discount.forCoupon(code);

        assertAll(
                () -> assertEquals(description, discount.describe()),
                () -> assertEquals(saving, discount.appliedTo(ORDER)));
    }

    @Test
    @DisplayName("the factory method's name says what the number means")
    void namesRemoveTheAmbiguity() {
        // Both take a single number. As constructors they could not coexist.
        assertAll(
                () -> assertEquals(Money.pounds(12.00),
                        Discount.percentage(10).appliedTo(ORDER)),
                () -> assertEquals(Money.pounds(10.00),
                        Discount.amountOff(Money.pounds(10)).appliedTo(ORDER)));
    }

    @Test
    @DisplayName("none() hands back the same instance every time")
    void noneIsShared() {
        assertSame(Discount.none(), Discount.none());
    }

    @Test
    @DisplayName("freeShipping() hands back the same instance every time")
    void freeShippingIsShared() {
        assertSame(Discount.freeShipping(), Discount.freeShipping());
    }

    @Test
    @DisplayName("asking for 0% quietly gives back the do-nothing discount")
    void zeroPercentIsSubstituted() {
        assertSame(Discount.none(), Discount.percentage(0));
    }

    @Test
    @DisplayName("asking for £0.00 off quietly gives back the do-nothing discount")
    void zeroAmountIsSubstituted() {
        assertSame(Discount.none(), Discount.amountOff(Money.zero()));
    }

    @Test
    @DisplayName("bestOf picks per order, so the winner can change")
    void bestOfDependsOnTheOrder() {
        Discount best = Discount.bestOf(Discount.percentage(10), Discount.amountOff(Money.pounds(5)));

        Order small = new Order("ORD-S", "CUST-S", Money.pounds(20.00), Money.pounds(4.99));
        Order large = new Order("ORD-L", "CUST-L", Money.pounds(200.00), Money.pounds(4.99));

        assertAll(
                // 10% of £20 is £2, so the flat £5 wins.
                () -> assertEquals(Money.pounds(5.00), best.appliedTo(small)),
                // 10% of £200 is £20, so the percentage wins.
                () -> assertEquals(Money.pounds(20.00), best.appliedTo(large)));
    }

    @Test
    @DisplayName("a flat discount never exceeds the subtotal")
    void flatDiscountIsCapped() {
        Order cheap = new Order("ORD-C", "CUST-C", Money.pounds(3.00), Money.pounds(4.99));

        assertEquals(Money.pounds(3.00), Discount.amountOff(Money.pounds(5)).appliedTo(cheap));
    }

    @Test
    @DisplayName("an impossible percentage is refused at the door")
    void percentageIsValidated() {
        assertAll(
                () -> assertThrows(IllegalArgumentException.class, () -> Discount.percentage(-1)),
                () -> assertThrows(IllegalArgumentException.class, () -> Discount.percentage(101)));
    }

    @Test
    @DisplayName("an unknown coupon code is refused, and says so")
    void unknownCouponIsRejected() {
        IllegalArgumentException e = assertThrows(IllegalArgumentException.class,
                () -> Discount.forCoupon("SAVE99"));

        assertTrue(e.getMessage().contains("SAVE99"), e.getMessage());
    }

    @Test
    @DisplayName("every implementation class is invisible from outside the package")
    void implementationsAreNotPublic() {
        assertAll(
                () -> assertTrue(isHidden(Discount.none())),
                () -> assertTrue(isHidden(Discount.percentage(10))),
                () -> assertTrue(isHidden(Discount.amountOff(Money.pounds(5)))),
                () -> assertTrue(isHidden(Discount.freeShipping())),
                () -> assertTrue(isHidden(Discount.bestOf(Discount.none(), Discount.none()))));
    }

    private static boolean isHidden(Discount discount) {
        return !java.lang.reflect.Modifier.isPublic(discount.getClass().getModifiers());
    }
}
