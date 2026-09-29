package com.jk.explore.remotefacademvc;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Before: the order's small methods published one by one, so the phone app needs a call per fact.
 */
@RestController
public class FineGrainedController {

    private final OrderStore store;

    public FineGrainedController(OrderStore store) {
        this.store = store;
    }

    @GetMapping("/order/customer")
    public String customer() {
        return store.order().customer();
    }

    @GetMapping("/order/items")
    public String items() {
        return String.join(", ", store.order().items());
    }

    @GetMapping("/order/total")
    public String total() {
        return String.format("£%.2f", store.order().pence() / 100.0);
    }

    @GetMapping("/order/address")
    public String address() {
        return store.order().address();
    }

    @GetMapping("/order/slot")
    public String slot() {
        return store.order().slot();
    }

    @PutMapping("/order/address")
    public String changeAddress(@RequestBody String address) {
        store.order().changeAddress(address);
        return "address changed";
    }

    @PutMapping("/order/slot")
    public String changeSlot(@RequestBody String slot) {
        store.order().changeSlot(slot);
        return "slot changed";
    }
}
