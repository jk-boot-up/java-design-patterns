package com.jk.explore.pageobjectselenium;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import org.junit.jupiter.api.Test;

/** The whole demo in a real Chromium container; skipped, not failed, without a container runtime. */
class DemoRunsTest {

    @Test
    void acts() throws Exception {
        assumeTrue(Browser.containerRuntimeAvailable(), "needs a container runtime");
        String all = String.join("\n", SeleniumPageObjectDemo.run());
        assertTrue(all.contains("click #apply-btn, read #total: 50.00"), all);
        assertTrue(all.contains("name the selector themselves: 0 of 5 pass"), all);
        assertTrue(all.contains("after one selector is changed in it: 5 of 5 pass"), all);
        assertTrue(all.contains("checkout.applyCoupon(\"SAVE10\").total(): 45.00"), all);
        assertTrue(all.contains("ConfirmationPage: ORD-1042, \"Thank you for your order\""), all);
    }

    @Test
    void adviceIsASentenceNotAStackTrace() {
        assertTrue(Browser.NO_RUNTIME_ADVICE.contains("Start Docker Desktop"));
    }
}
