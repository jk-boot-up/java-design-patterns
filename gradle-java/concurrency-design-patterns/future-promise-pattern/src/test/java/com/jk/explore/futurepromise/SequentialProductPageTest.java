package com.jk.explore.futurepromise;

import com.jk.explore.futurepromise.domain.ProductPageView;
import com.jk.explore.futurepromise.naive.SequentialProductPage;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;

class SequentialProductPageTest {

    @Test
    void rendersAllThreeValuesByCallingEachLookupInOrder() {
        StringBuilder callOrder = new StringBuilder();
        SequentialProductPage page = new SequentialProductPage(
                sku -> { callOrder.append("price,"); return new BigDecimal("9.99"); },
                sku -> { callOrder.append("stock,"); return 3; },
                sku -> { callOrder.append("rating"); return 4.0; });

        ProductPageView view = page.render("ESP-001");

        assertEquals(new BigDecimal("9.99"), view.price());
        assertEquals(3, view.stock());
        assertEquals(4.0, view.rating());
        assertEquals("price,stock,rating", callOrder.toString(),
                "each lookup must complete before the next one is even called");
    }
}
