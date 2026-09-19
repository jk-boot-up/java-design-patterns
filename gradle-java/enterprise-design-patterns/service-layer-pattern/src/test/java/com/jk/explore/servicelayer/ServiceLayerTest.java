package com.jk.explore.servicelayer;

import com.jk.explore.servicelayer.domain.CartLine;
import com.jk.explore.servicelayer.domain.EmailService;
import com.jk.explore.servicelayer.domain.Order;
import com.jk.explore.servicelayer.domain.OrderRejectedException;
import com.jk.explore.servicelayer.domain.OrderRequest;
import com.jk.explore.servicelayer.domain.PaymentGateway;
import com.jk.explore.servicelayer.domain.Product;
import com.jk.explore.servicelayer.domain.Shop;
import com.jk.explore.servicelayer.naive.ControllerLogic;
import com.jk.explore.servicelayer.naive.CopiedInTheCli;
import com.jk.explore.servicelayer.naive.SelfPlacingOrder;
import com.jk.explore.servicelayer.pattern.AnemicOrder;
import com.jk.explore.servicelayer.pattern.OrderService;
import com.jk.explore.servicelayer.pattern.SupportCli;
import com.jk.explore.servicelayer.pattern.WebController;
import com.jk.explore.servicelayer.toydb.Database;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ServiceLayerTest {

    @Test
    void withOneDoorTheControllerLogicWorks() {
        PaymentGateway payments = new PaymentGateway();
        EmailService email = new EmailService();
        ControllerLogic web = new ControllerLogic(Shop.seeded(), Shop.products(), payments, email);
        assertEquals("placed", web.placeOrder(PlaceOrderDemo.fineOrder()));
        assertEquals(20_000, payments.totalChargedPence());
        assertEquals(1, email.sentCount());
    }

    @Test
    void theCopiedDoorChargesACustomerWhoseOrderIsRefused() {
        PaymentGateway webPayments = new PaymentGateway();
        PaymentGateway cliPayments = new PaymentGateway();
        new ControllerLogic(Shop.seeded(), Shop.products(), webPayments, new EmailService()).placeOrder(PlaceOrderDemo.tooManyMice());
        new CopiedInTheCli(Shop.seeded(), Shop.products(), cliPayments, new EmailService()).placeOrder(PlaceOrderDemo.tooManyMice());
        assertEquals(0, webPayments.totalChargedPence());
        assertEquals(6_000, cliPayments.totalChargedPence());
    }

    @Test
    void anOrderThatDoesEverythingNeedsSixCollaborators() {
        assertEquals(6, SelfPlacingOrder.class.getConstructors()[0].getParameterCount());
    }

    @Test
    void bothDoorsGiveTheSameAnswerBecauseThereIsOnePlaceOrder() {
        PaymentGateway payments = new PaymentGateway();
        OrderService service = new OrderService(Shop.seeded(), Shop.products(), payments, new EmailService());
        String web = new WebController(service).placeOrder(PlaceOrderDemo.tooManyMice());
        String cli = new SupportCli(service).placeOrder(PlaceOrderDemo.tooManyMice());
        assertEquals(web, cli);
        assertEquals(0, payments.totalChargedPence());
    }

    @Test
    void aSuccessfulOrderIsWrittenChargedAndEmailedOnce() {
        Database db = Shop.seeded();
        PaymentGateway payments = new PaymentGateway();
        EmailService email = new EmailService();
        Order order = new OrderService(db, Shop.products(), payments, email).placeOrder(PlaceOrderDemo.fineOrder());
        assertEquals(20_000, order.totalPence());
        assertEquals(1, db.table(Shop.ORDERS).size());
        assertEquals(20_000, payments.totalChargedPence());
        assertEquals(1, email.sentCount());
    }

    @Test
    void aRefusedOrderIsRolledBackAndNothingIsEmailed() {
        Database db = Shop.seeded();
        EmailService email = new EmailService();
        OrderService service = new OrderService(db, Shop.products(), new PaymentGateway(), email);
        assertThrows(OrderRejectedException.class, () -> service.placeOrder(PlaceOrderDemo.tooManyMice()));
        assertEquals(0, db.table(Shop.ORDERS).size());
        assertEquals(0, email.sentCount());
    }

    @Test
    void theRulesLiveInTheDomainNotTheService() {
        List<Product> products = Shop.products();
        assertThrows(OrderRejectedException.class,
                () -> Order.from(1, new OrderRequest(7, List.of()), products));
        assertThrows(OrderRejectedException.class,
                () -> Order.from(1, new OrderRequest(7, List.of(new CartLine(1, 0))), products));
        assertThrows(OrderRejectedException.class, () -> products.get(1).reserve(4));
        assertTrue(Order.from(1, new OrderRequest(7, List.of(new CartLine(3, 1))), products).deliveryIsFree());
    }

    @Test
    void anAnemicOrderHasOnlyGettersAndSetters() {
        assertTrue(Arrays.stream(AnemicOrder.class.getDeclaredMethods()).map(Method::getName)
                .allMatch(m -> m.startsWith("get") || m.startsWith("set")));
    }
}
