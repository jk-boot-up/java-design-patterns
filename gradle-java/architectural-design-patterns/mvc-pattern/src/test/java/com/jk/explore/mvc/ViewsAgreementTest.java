package com.jk.explore.mvc;

import com.jk.explore.mvc.application.PlaceOrderRequest;
import com.jk.explore.mvc.application.PlaceOrderRequest.RequestedLine;
import com.jk.explore.mvc.application.PlaceOrderService;
import com.jk.explore.mvc.controller.OrderSummaryController;
import com.jk.explore.mvc.controller.OrderSummaryController.CheckoutOutcome;
import com.jk.explore.mvc.infrastructure.CardNetwork;
import com.jk.explore.mvc.infrastructure.EmailServer;
import com.jk.explore.mvc.infrastructure.InMemoryOrderTable;
import com.jk.explore.mvc.infrastructure.OrderTable;
import com.jk.explore.mvc.infrastructure.ProductTable;
import com.jk.explore.mvc.naive.view.RoundedEmailView;
import com.jk.explore.mvc.view.EmailConfirmationView;
import com.jk.explore.mvc.view.ScreenSummaryView;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;

/**
 * The point of this whole project, pinned down as two assertions.
 *
 * <p>{@code twoRealViewsAlwaysAgree} is the pattern working: nothing here is
 * a coincidence of the numbers chosen, because neither view is capable of
 * producing a total that differs from the model's.
 *
 * <p>{@code theNaiveShortcutReallyDoesDisagree} is not a failure waiting to
 * be fixed. It is a demonstration that the bug this project is about is
 * real, reproducible, and not a rhetorical example — the eighty-nine pounds
 * fifty burr grinder genuinely rounds to ninety before {@code RoundedEmailView}
 * multiplies it, and this test proves that arithmetic rather than asserting
 * it in prose.
 */
class ViewsAgreementTest {

    private PlaceOrderRequest adasOrder() {
        return PlaceOrderRequest.of("cust-8801",
                new RequestedLine("ESP-001", 1),
                new RequestedLine("GRD-014", 1),
                new RequestedLine("BNS-220", 2));
    }

    @Test
    void twoRealViewsAlwaysAgree() {
        ProductTable products = ProductTable.seeded();
        OrderTable orders = new InMemoryOrderTable();
        EmailServer email = new EmailServer();
        PlaceOrderService placeOrder =
                new PlaceOrderService(products, orders, CardNetwork.working());
        OrderSummaryController controller =
                new OrderSummaryController(placeOrder, orders, email);

        CheckoutOutcome outcome = controller.checkout(
                adasOrder(), "ada@example.com",
                new ScreenSummaryView(), new EmailConfirmationView());

        assertEquals(outcome.model().total().toString(), "£382.50");
        assertEquals(1, email.sent().size());
        // The email's body carries the same total the screen printed.
        assertEquals(true, email.sent().get(0).body().contains("£382.50"));
        assertEquals(true, outcome.screenText().contains("£382.50"));
    }

    @Test
    void theNaiveShortcutReallyDoesDisagree() {
        ProductTable products = ProductTable.seeded();
        OrderTable orders = new InMemoryOrderTable();
        PlaceOrderService placeOrder =
                new PlaceOrderService(products, orders, CardNetwork.working());
        OrderSummaryController controller =
                new OrderSummaryController(placeOrder, orders, new EmailServer());
        RoundedEmailView roundedEmail = new RoundedEmailView(products);

        CheckoutOutcome outcome = controller.checkout(
                adasOrder(), "ada@example.com", new ScreenSummaryView(), roundedEmail);

        String screenTotal = outcome.model().total().toString();
        String emailText = roundedEmail.render(outcome.model());

        assertEquals("£382.50", screenTotal);
        assertEquals(true, emailText.contains("£383.00"));
        assertNotEquals(screenTotal, "£383.00");
    }
}
