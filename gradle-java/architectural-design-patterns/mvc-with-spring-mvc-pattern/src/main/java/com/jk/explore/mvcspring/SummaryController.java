package com.jk.explore.mvcspring;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

/**
 * The controller: it finds the order, asks the model for a summary, and names a view. It works out
 * nothing itself, and it does not know what the view will look like.
 */
@Controller
public class SummaryController {

    private final OrderStore orders;

    public SummaryController(OrderStore orders) {
        this.orders = orders;
    }

    @GetMapping(value = "/orders/{id}", produces = "text/html")
    public String page(@PathVariable String id, Model model) {
        model.addAttribute("summary", OrderSummary.of(orders.find(id).orElseThrow()));
        return "summary";
    }

    @GetMapping(value = "/orders/{id}", produces = "application/json")
    @ResponseBody
    public OrderSummary json(@PathVariable String id) {
        return OrderSummary.of(orders.find(id).orElseThrow());
    }

    /** The shortcut: hands the raw order to a view that does its own sums. */
    @GetMapping(value = "/orders/{id}/naive", produces = "text/html")
    public String naive(@PathVariable String id, Model model) {
        model.addAttribute("order", orders.find(id).orElseThrow());
        return "naive-summary";
    }

    @PostMapping("/orders")
    public String place(@RequestParam String customer, @RequestParam String sku, @RequestParam int quantity) {
        return "redirect:/orders/" + orders.place(customer, sku, quantity).id();
    }
}
