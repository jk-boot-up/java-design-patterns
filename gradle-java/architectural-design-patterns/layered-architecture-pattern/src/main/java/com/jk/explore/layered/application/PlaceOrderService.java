package com.jk.explore.layered.application;

import com.jk.explore.layered.domain.CheckoutRefusedException;
import com.jk.explore.layered.domain.Money;
import com.jk.explore.layered.domain.Order;
import com.jk.explore.layered.domain.OrderLine;
import com.jk.explore.layered.domain.Product;
import com.jk.explore.layered.infrastructure.CardNetwork;
import com.jk.explore.layered.infrastructure.EmailServer;
import com.jk.explore.layered.infrastructure.OrderTable;
import com.jk.explore.layered.infrastructure.PaymentDeclinedException;
import com.jk.explore.layered.infrastructure.ProductTable;

import java.util.ArrayList;
import java.util.List;

/**
 * The application layer: one method, four steps, in order.
 *
 * <p>This class is the use case. It owns the <em>sequence</em> — check, charge,
 * reduce, store, notify — and nothing else. It does no arithmetic (the domain
 * does that), it holds no data (storage does that), and it renders nothing (the
 * presentation layer does that). A use case that is only a list of steps is a
 * use case you can read aloud, and reading this one aloud is how the video
 * explains the feature.
 *
 * <p><strong>The order of the steps is load-bearing, and it is not obvious.</strong>
 * The card is charged <em>before</em> anything is written down. Do it the other
 * way — store the order, reduce the stock, then charge — and a declined card
 * leaves an order in the database, stock missing from the shelf and no way to
 * know that neither should have happened. Charging first means a decline throws
 * before a single thing has changed, which is acceptance assertion A6 of the
 * shared feature.
 *
 * <p><strong>And here is this project's honest cost, stated in its own source.</strong>
 * Look at the imports. Five of them are the storage package. This class cannot
 * be compiled, let alone tested, without the classes that keep orders in a map
 * and send email — because the <em>names</em> {@code OrderTable},
 * {@code CardNetwork} and {@code EmailServer} are defined down there. The layer
 * boundary is a package, not a direction: the use case reaches down and takes
 * what it finds. Hexagonal architecture changes exactly that, by moving those
 * three names up here and leaving the implementations below. That is one move,
 * and it is the entire difference between this project and the next one.
 */
public class PlaceOrderService {

    private final ProductTable products;
    private final OrderTable orders;
    private final CardNetwork cards;
    private final EmailServer email;
    private int nextOrderNumber = 1001;

    public PlaceOrderService(ProductTable products,
                             OrderTable orders,
                             CardNetwork cards,
                             EmailServer email) {
        this.products = products;
        this.orders = orders;
        this.cards = cards;
        this.email = email;
    }

    public PlaceOrderResult place(PlaceOrderRequest request, String customerEmail) {
        try {
            List<OrderLine> lines = priceEveryLine(request);
            Order order = Order.placed(nextId(), request.customerId(), lines);

            // Money first. Nothing below this line can be undone for free, and
            // nothing above it has changed anything yet.
            cards.charge(order.customerId(), order.total());

            for (OrderLine line : order.lines()) {
                products.reduceStock(line.sku(), line.quantity());
            }
            orders.save(order);
            email.send(customerEmail, confirmationFor(order));

            return PlaceOrderResult.placed(order.id(), order.total());
        } catch (CheckoutRefusedException refused) {
            return PlaceOrderResult.refused(refused.getMessage());
        } catch (PaymentDeclinedException declined) {
            // The card network's exception stops here. The layer above is told
            // "refused, and here is why" in the same shape as any other refusal,
            // because a customer does not care which package the news came from.
            return PlaceOrderResult.refused(declined.getMessage());
        }
    }

    private List<OrderLine> priceEveryLine(PlaceOrderRequest request) {
        List<OrderLine> lines = new ArrayList<>();
        for (PlaceOrderRequest.RequestedLine requested : request.lines()) {
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
        Money total = order.total();
        return "Thank you. Your order " + order.id() + " for " + total + " is confirmed.";
    }

    private String nextId() {
        return "ord-" + nextOrderNumber++;
    }
}
