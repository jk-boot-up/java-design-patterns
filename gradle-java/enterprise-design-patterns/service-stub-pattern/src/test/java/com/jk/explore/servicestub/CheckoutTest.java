package com.jk.explore.servicestub;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.junit.jupiter.api.Test;

class CheckoutTest {

    @Test
    void knownPostcodeFillsTheAddress() {
        assertEquals("deliver to 4 Mill Lane, Leeds", Checkout.address(new PostcodeStub(), "LS1 4AP"));
    }

    @Test
    void unknownPostcodeAsksTheCustomer() {
        assertEquals("postcode not found: please type your address", Checkout.address(new PostcodeStub(), "ZZ9 9ZZ"));
    }

    @Test
    void outageAsksTheCustomer() {
        assertEquals("lookup unavailable: please type your address",
                Checkout.address(new PostcodeStub().goDown(), "LS1 4AP"));
    }

    @Test
    void realServiceCostsMoney() {
        PostcodeService real = new PostcodeService();
        real.lookup("LS1 4AP");
        assertEquals(5, real.spentPence());
    }

    @Test
    void contractCheckFindsTheCaseDifference() {
        assertEquals(1, ContractCheck.differences(new PostcodeStub(), new PostcodeService(),
                List.of("LS1 4AP", "ZZ9 9ZZ", "ls1 4ap")).size());
    }
}
