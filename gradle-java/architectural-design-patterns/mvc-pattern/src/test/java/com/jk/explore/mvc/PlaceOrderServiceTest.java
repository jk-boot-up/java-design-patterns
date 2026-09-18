package com.jk.explore.mvc;

import com.jk.explore.mvc.application.PlaceOrderRequest;
import com.jk.explore.mvc.application.PlaceOrderRequest.RequestedLine;
import com.jk.explore.mvc.application.PlaceOrderResult;
import com.jk.explore.mvc.application.PlaceOrderService;
import com.jk.explore.mvc.domain.Money;
import com.jk.explore.mvc.infrastructure.CardNetwork;
import com.jk.explore.mvc.infrastructure.InMemoryOrderTable;
import com.jk.explore.mvc.infrastructure.ProductTable;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class PlaceOrderServiceTest {

    private PlaceOrderService serviceWith(CardNetwork cards) {
        return new PlaceOrderService(ProductTable.seeded(), new InMemoryOrderTable(), cards);
    }

    @Test
    void threeLinesPriceToTheExpectedTotal() {
        PlaceOrderResult result = serviceWith(CardNetwork.working()).place(
                PlaceOrderRequest.of("cust-8801",
                        new RequestedLine("ESP-001", 1),
                        new RequestedLine("GRD-014", 1),
                        new RequestedLine("BNS-220", 2)));

        assertTrue(result.placed());
        assertEquals(Money.pounds(382, 50), result.total());
    }

    @Test
    void notEnoughStockIsRefusedBeforeAnyCharge() {
        CardNetwork cards = CardNetwork.working();
        PlaceOrderResult result = serviceWith(cards).place(
                PlaceOrderRequest.of("cust-8801", new RequestedLine("GRD-014", 3)));

        assertFalse(result.placed());
        assertEquals("only 2 of GRD-014 left", result.reason());
        assertTrue(cards.charges().isEmpty());
    }

    @Test
    void unknownProductIsRefused() {
        PlaceOrderResult result = serviceWith(CardNetwork.working()).place(
                PlaceOrderRequest.of("cust-8801", new RequestedLine("XXX-999", 1)));

        assertFalse(result.placed());
        assertEquals("no such product: XXX-999", result.reason());
    }

    @Test
    void aDeclinedCardLeavesStockUntouched() {
        ProductTable products = ProductTable.seeded();
        PlaceOrderService service =
                new PlaceOrderService(products, new InMemoryOrderTable(), CardNetwork.declining());

        PlaceOrderResult result = service.place(
                PlaceOrderRequest.of("cust-8801", new RequestedLine("BNS-220", 2)));

        assertFalse(result.placed());
        assertEquals(40, products.stockOf("BNS-220"));
    }

    @Test
    void orderIdsAreAssignedInSequence() {
        PlaceOrderService service = serviceWith(CardNetwork.working());
        PlaceOrderRequest oneBag = PlaceOrderRequest.of("cust-8801", new RequestedLine("BNS-220", 1));

        assertEquals("ord-1001", service.place(oneBag).orderId());
        assertEquals("ord-1002", service.place(oneBag).orderId());
    }
}
