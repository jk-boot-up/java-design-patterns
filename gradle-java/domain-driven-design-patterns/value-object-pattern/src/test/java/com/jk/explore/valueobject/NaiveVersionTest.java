package com.jk.explore.valueobject;

import com.jk.explore.valueobject.domain.EmailAddress;
import com.jk.explore.valueobject.naive.BareEmailSignup;
import com.jk.explore.valueobject.naive.IdentityMoney;
import com.jk.explore.valueobject.naive.MutableMoney;
import com.jk.explore.valueobject.naive.NaivePricing;
import org.junit.jupiter.api.Test;

import java.util.HashSet;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/** These document the bugs the pattern removes, so that a change which quietly fixes them is noticed. */
class NaiveVersionTest {

    @Test
    void doubleArithmeticIsNotExact() {
        assertNotEquals(3.3, NaivePricing.total(1.10, 3));
        assertNotEquals(0.3, 0.1 + 0.2);
    }

    @Test
    void poundsAndDollarsAreAddedWithoutComplaint() {
        assertEquals(20.0, NaivePricing.add(10, "GBP", 10, "USD"));
    }

    @Test
    void aMutablePriceSharedByTwoOrdersChangesBoth() {
        MutableMoney shared = new MutableMoney(2000);
        MutableMoney other = shared;
        other.subtract(500);
        assertEquals(1500, shared.pence());
    }

    @Test
    void identityEqualityMakesThreeOfTheSameAmount() {
        assertEquals(3, new HashSet<>(List.of(new IdentityMoney(500), new IdentityMoney(500), new IdentityMoney(500))).size());
    }

    @Test
    void roundedSplitLosesAPenny() {
        double[] s = NaivePricing.splitThreeWays(10.00);
        assertEquals(999, Math.round((s[0] + s[1] + s[2]) * 100));
    }

    @Test
    void theStringVersionStoresABadEmailButTheTypeRefusesIt() {
        BareEmailSignup signup = new BareEmailSignup();
        signup.importFromPartner("not an email");
        assertEquals(List.of("not an email"), signup.stored());
        assertThrows(IllegalArgumentException.class, () -> EmailAddress.of("not an email"));
    }
}
