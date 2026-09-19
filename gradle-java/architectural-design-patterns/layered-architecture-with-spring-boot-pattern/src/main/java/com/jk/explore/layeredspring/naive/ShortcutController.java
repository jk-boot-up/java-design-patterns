package com.jk.explore.layeredspring.naive;

import com.jk.explore.layeredspring.domain.Order;
import com.jk.explore.layeredspring.infrastructure.OrderRepository;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

/**
 * The shortcut, kept for contrast and never scanned: a screen that reads the repository directly
 * and returns the domain object as it is. Ten minutes to write, and nothing in Spring objects.
 */
@RestController
public class ShortcutController {

    private final OrderRepository orders;

    public ShortcutController(OrderRepository orders) {
        this.orders = orders;
    }

    @GetMapping("/raw-orders/{id}")
    public Order raw(@PathVariable String id) {
        return orders.find(id).orElseThrow();
    }
}
