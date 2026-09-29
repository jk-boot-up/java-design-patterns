package com.jk.explore.remotefacademvc;

import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * The pattern: a coarse-grained facade for remote callers. One call returns the whole order screen as
 * JSON; one call changes the whole delivery. Inside, it only packs and unpacks; the rules stay on Order.
 */
@RestController
public class OrderFacade {

    /** What the order screen needs, in one piece. Jackson turns it into JSON. */
    public record OrderSummary(String id, String customer, List<String> items, String total, String address, String slot) {
    }

    /** A whole delivery change, in one piece. */
    public record DeliveryChange(String address, String slot) {
    }

    private final OrderStore store;

    public OrderFacade(OrderStore store) {
        this.store = store;
    }

    @GetMapping("/order-summary")
    public OrderSummary summary() {
        Order o = store.order();
        return new OrderSummary(o.id(), o.customer(), o.items(), String.format("£%.2f", o.pence() / 100.0), o.address(), o.slot());
    }

    @PutMapping("/order-delivery")
    public String changeDelivery(@RequestBody DeliveryChange change) {
        store.order().changeDelivery(change.address(), change.slot());
        return "delivery changed";
    }

    /** A refused change becomes a standard problem report: HTTP 422 with the reason. */
    @ExceptionHandler(IllegalArgumentException.class)
    public ProblemDetail refused(IllegalArgumentException e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.UNPROCESSABLE_CONTENT, e.getMessage());
    }
}
