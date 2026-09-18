package com.jk.explore.mvc;

import com.jk.explore.mvc.domain.Order;
import com.jk.explore.mvc.domain.OrderLine;
import com.jk.explore.mvc.domain.Product;
import com.jk.explore.mvc.model.OrderSummaryModel;
import com.jk.explore.mvc.view.CompositeOrderView;
import com.jk.explore.mvc.view.EmailConfirmationView;
import com.jk.explore.mvc.view.ScreenSummaryView;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The composite lets several views be treated as one, so a caller wanting
 * "print the screen and the email together" needs nothing more than a
 * longer list — no new interface, no change to anything that already calls
 * a plain {@code OrderSummaryView}.
 */
class CompositeOrderViewTest {

    @Test
    void rendersEveryViewInOrder() {
        Product grinder = new Product("GRD-014", "Burr Grinder",
                com.jk.explore.mvc.domain.Money.pounds(89, 50));
        Order order = Order.placed("ord-9001", "cust-1",
                List.of(OrderLine.of(grinder, 1)));
        OrderSummaryModel model = OrderSummaryModel.of(order);

        CompositeOrderView composite = new CompositeOrderView(
                List.of(new ScreenSummaryView(), new EmailConfirmationView()));

        String rendered = composite.render(model);

        assertTrue(rendered.contains("Order ord-9001 placed."));
        assertTrue(rendered.contains("is confirmed."));
        assertTrue(rendered.indexOf("Order ord-9001 placed.")
                < rendered.indexOf("is confirmed."),
                "views must render in the order they were given");
    }
}
