package com.jk.explore.nullobject;

import com.jk.explore.nullobject.domain.DiscountDirectory;
import com.jk.explore.nullobject.domain.DiscountServiceDown;
import com.jk.explore.nullobject.naive.NaiveCheckout;
import com.jk.explore.nullobject.pattern.ForgivingDirectory;
import com.jk.explore.nullobject.pattern.NoDiscount;
import com.jk.explore.nullobject.pattern.NullObjectCheckout;
import com.jk.explore.nullobject.pattern.NullObjectDirectory;
import com.jk.explore.nullobject.pattern.OptionalDirectory;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class NullObjectTest {

    private static final long PRICE = 10_000;

    @Test
    void theNaiveCheckoutWorksWherePeopleRememberedTheCheck() {
        NaiveCheckout c = new NaiveCheckout(new DiscountDirectory());
        assertEquals(9_000, c.total(1, PRICE));
        assertEquals(10_000, c.total(2, PRICE));
        assertEquals(7_500, c.staffExport(3, PRICE));
    }

    @Test
    void theEighthMethodThrowsARealNullPointerExceptionForACustomerWithNoDiscount() {
        NaiveCheckout c = new NaiveCheckout(new DiscountDirectory());
        assertThrows(NullPointerException.class, () -> c.taxBase(2, PRICE));
        assertEquals(9_000, c.taxBase(1, PRICE), "it only fails for customers without a discount");
    }

    @Test
    void sevenOfTheEightMethodsCheckForNull() throws IOException {
        String source = Files.readString(Path.of("src/main/java/com/jk/explore/nullobject/naive/NaiveCheckout.java"));
        int checks = source.split("discount != null", -1).length - 1;
        assertEquals(7, checks);
    }

    @Test
    void deletingEveryNullCheckLeavesTheBehaviourIdentical() {
        NaiveCheckout naive = new NaiveCheckout(new DiscountDirectory());
        NullObjectCheckout pattern = new NullObjectCheckout(new NullObjectDirectory(new DiscountDirectory()));
        for (int customer = 1; customer <= 4; customer++) {
            assertEquals(naive.total(customer, PRICE), pattern.total(customer, PRICE));
        }
    }

    @Test
    void theNullObjectFixesTheForgottenCheck() {
        NullObjectCheckout pattern = new NullObjectCheckout(new NullObjectDirectory(new DiscountDirectory()));
        assertEquals(10_000, pattern.taxBase(2, PRICE));
        assertEquals(PRICE, NoDiscount.INSTANCE.apply(PRICE));
    }

    @Test
    void aPlainNullObjectStillLetsAnOutageThrough() {
        DiscountDirectory directory = new DiscountDirectory();
        directory.goDown();
        assertThrows(DiscountServiceDown.class, () -> new NullObjectDirectory(directory).find(1));
    }

    @Test
    void aForgivingNullObjectTurnsAnOutageIntoASilentFullPriceOrder() {
        DiscountDirectory directory = new DiscountDirectory();
        directory.goDown();
        assertEquals(10_000, new ForgivingDirectory(directory).find(1).apply(PRICE));
        assertEquals(9_000, new NullObjectDirectory(new DiscountDirectory()).find(1).apply(PRICE),
                "what the customer was entitled to");
    }

    @Test
    void optionalKeepsNoDiscountAndAnOutageApart() {
        DiscountDirectory directory = new DiscountDirectory();
        OptionalDirectory optional = new OptionalDirectory(directory);
        assertTrue(optional.find(1).isPresent());
        assertFalse(optional.find(2).isPresent());
        directory.goDown();
        assertThrows(DiscountServiceDown.class, () -> optional.find(1));
    }
}
