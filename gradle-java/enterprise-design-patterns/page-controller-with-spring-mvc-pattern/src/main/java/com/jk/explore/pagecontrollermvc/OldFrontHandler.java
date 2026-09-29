package com.jk.explore.pagecontrollermvc;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * Before: one handler for every page under /old. Quantity parsing was added at the top for the basket,
 * so it now runs for every page.
 */
@RestController
public class OldFrontHandler {

    @GetMapping("/old/{page}")
    public String handle(@org.springframework.web.bind.annotation.PathVariable String page,
                         @RequestParam(required = false) String sku,
                         @RequestParam(required = false) String add,
                         @RequestParam(required = false) String qty) {
        int quantity = Integer.parseInt(qty);          // meant for the basket, runs for every page
        if (page.equals("basket")) {
            return "basket: " + quantity + " x " + add;
        }
        return Catalog.price(sku);
    }
}
