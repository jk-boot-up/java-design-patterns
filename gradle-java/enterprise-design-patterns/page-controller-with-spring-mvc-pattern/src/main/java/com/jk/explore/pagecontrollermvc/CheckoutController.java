package com.jk.explore.pagecontrollermvc;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * The checkout page. Its author forgot the login check that the basket page repeats.
 */
@RestController
public class CheckoutController {

    @GetMapping("/checkout")
    public String checkout() {
        return "checkout: pay £63.44 with the card on file";
    }
}
