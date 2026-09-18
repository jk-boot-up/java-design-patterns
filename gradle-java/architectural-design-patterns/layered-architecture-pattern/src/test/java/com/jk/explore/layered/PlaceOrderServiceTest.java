package com.jk.explore.layered;

import com.jk.explore.layered.application.PlaceOrderRequest;
import com.jk.explore.layered.application.PlaceOrderRequest.RequestedLine;
import com.jk.explore.layered.application.PlaceOrderResult;
import com.jk.explore.layered.application.PlaceOrderService;
import com.jk.explore.layered.domain.Money;
import com.jk.explore.layered.infrastructure.CardNetwork;
import com.jk.explore.layered.infrastructure.EmailServer;
import com.jk.explore.layered.infrastructure.InMemoryOrderTable;
import com.jk.explore.layered.infrastructure.ProductTable;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The application layer's one use case, tested without a screen, a real
 * network or a real store — which is the whole point of putting the rule
 * about layers where a build can check it. If this class could not be built
 * without constructing {@code CheckoutScreen}, the layer boundary would be
 * decorative.
 */
class PlaceOrderServiceTest {

    private PlaceOrderService serviceWith(CardNetwork cards) {
        return new PlaceOrderService(ProductTable.seeded(), new InMemoryOrderTable(),
                cards, new EmailServer());
    }

    @Test
    void threeLinesPriceToTheExpectedTotal() {
        PlaceOrderService service = serviceWith(CardNetwork.working());
        PlaceOrderResult result = service.place(
                PlaceOrderRequest.of("cust-8801",
                        new RequestedLine("ESP-001", 1),
                        new RequestedLine("GRD-014", 1),
                        new RequestedLine("BNS-220", 2)),
                "ada@example.com");

        assertTrue(result.placed());
        assertEquals(Money.pounds(382, 50), result.total());
    }

    @Test
    void notEnoughStockIsRefusedBeforeAnyChargeOrWrite() {
        CardNetwork cards = CardNetwork.working();
        PlaceOrderService service = serviceWith(cards);

        PlaceOrderResult result = service.place(
                PlaceOrderRequest.of("cust-8801", new RequestedLine("GRD-014", 3)),
                "ada@example.com");

        assertFalse(result.placed());
        assertEquals("only 2 of GRD-014 left", result.reason());
        assertTrue(cards.charges().isEmpty(), "a refused order must never reach the card network");
    }

    @Test
    void unknownProductIsRefused() {
        PlaceOrderService service = serviceWith(CardNetwork.working());

        PlaceOrderResult result = service.place(
                PlaceOrderRequest.of("cust-8801", new RequestedLine("XXX-999", 1)),
                "ada@example.com");

        assertFalse(result.placed());
        assertEquals("no such product: XXX-999", result.reason());
    }

    @Test
    void aDeclinedCardLeavesStockAndOrdersUntouched() {
        ProductTable products = ProductTable.seeded();
        InMemoryOrderTable orders = new InMemoryOrderTable();
        PlaceOrderService service = new PlaceOrderService(
                products, orders, CardNetwork.declining(), new EmailServer());

        PlaceOrderResult result = service.place(
                PlaceOrderRequest.of("cust-8801", new RequestedLine("BNS-220", 2)),
                "ada@example.com");

        assertFalse(result.placed());
        assertEquals(40, products.stockOf("BNS-220"),
                "charging happens before stock is reduced, so a decline must leave stock untouched");
        assertEquals(0, orders.count(),
                "charging happens before the order is saved, so a decline must leave no order behind");
    }

    @Test
    void exactlyOneChargeAndOneConfirmationPerPlacedOrder() {
        EmailServer email = new EmailServer();
        PlaceOrderService service = new PlaceOrderService(
                ProductTable.seeded(), new InMemoryOrderTable(),
                CardNetwork.working(), email);

        service.place(PlaceOrderRequest.of("cust-8801", new RequestedLine("BNS-220", 1)),
                "ada@example.com");

        assertEquals(1, email.sent().size());
        assertEquals("ada@example.com", email.sent().get(0).to());
    }

    @Test
    void orderIdsAreAssignedInSequence() {
        PlaceOrderService service = serviceWith(CardNetwork.working());
        PlaceOrderRequest oneBag = PlaceOrderRequest.of("cust-8801", new RequestedLine("BNS-220", 1));

        PlaceOrderResult first = service.place(oneBag, "ada@example.com");
        PlaceOrderResult second = service.place(oneBag, "ada@example.com");

        assertEquals("ord-1001", first.orderId());
        assertEquals("ord-1002", second.orderId());
    }
}
