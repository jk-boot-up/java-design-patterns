package com.jk.explore.cleanspring.usecases;

import com.jk.explore.cleanspring.entities.CheckoutRefusedException;
import com.jk.explore.cleanspring.entities.Order;
import com.jk.explore.cleanspring.entities.OrderLine;
import com.jk.explore.cleanspring.entities.Product;

import java.util.ArrayList;
import java.util.List;

/**
 * <strong>This class is the use case, and its imports are the whole
 * argument of this project.</strong> Two packages only: {@code entities}
 * and this one, {@code usecases}. Not one class from {@code adapters}
 * appears here, in either direction — not a controller calling in, and not
 * a gateway being named directly.
 *
 * <p>Read the four fields. Every one of them is an interface this same
 * package declares: {@link OrderRepository}, {@link ProductRepository},
 * {@link PaymentGateway}, {@link NotificationGateway}. The classes that
 * really save an order, really take a payment, live two circles further
 * out, in {@code adapters.gateway} — and they reach <em>up</em> to
 * implement these interfaces. The call to {@code orders.save(order)} sends
 * control outward, to whichever gateway was wired in; the dependency —
 * which type must exist for this file to compile — points inward, at an
 * interface this file owns. Control flows out. The dependency points in.
 * Those are two different directions, and Clean Architecture's whole trick
 * is that they are allowed to disagree.
 */
public class PlaceOrderInteractor implements PlaceOrderInputBoundary {

    private final ProductRepository products;
    private final OrderRepository orders;
    private final PaymentGateway payments;
    private final NotificationGateway notifications;
    private int nextOrderNumber = 1001;

    public PlaceOrderInteractor(ProductRepository products, OrderRepository orders,
                                PaymentGateway payments, NotificationGateway notifications) {
        this.products = products;
        this.orders = orders;
        this.payments = payments;
        this.notifications = notifications;
    }

    @Override
    public PlaceOrderOutput execute(PlaceOrderInput input) {
        try {
            List<OrderLine> lines = priceEveryLine(input);
            Order order = Order.placed(nextId(), input.customerId(), lines);

            payments.charge(order.customerId(), order.total());

            for (OrderLine line : order.lines()) {
                products.reduceStock(line.sku(), line.quantity());
            }
            orders.save(order);
            notifications.send(input.contact(), confirmationFor(order));

            return PlaceOrderOutput.placed(order.id(), order.total());
        } catch (CheckoutRefusedException refused) {
            return PlaceOrderOutput.refused(refused.getMessage());
        } catch (PaymentDeclinedException declined) {
            return PlaceOrderOutput.refused(declined.getMessage());
        }
    }

    private List<OrderLine> priceEveryLine(PlaceOrderInput input) {
        List<OrderLine> lines = new ArrayList<>();
        for (PlaceOrderInput.RequestedLine requested : input.lines()) {
            Product product = products.find(requested.sku())
                    .orElseThrow(() -> new CheckoutRefusedException(
                            "no such product: " + requested.sku()));
            int available = products.stockOf(requested.sku());
            if (available < requested.quantity()) {
                throw new CheckoutRefusedException(
                        "only " + available + " of " + requested.sku() + " left");
            }
            lines.add(OrderLine.of(product, requested.quantity()));
        }
        return lines;
    }

    private String confirmationFor(Order order) {
        return "Thank you. Your order " + order.id() + " for " + order.total()
                + " is confirmed.";
    }

    private String nextId() {
        return "ord-" + nextOrderNumber++;
    }
}
