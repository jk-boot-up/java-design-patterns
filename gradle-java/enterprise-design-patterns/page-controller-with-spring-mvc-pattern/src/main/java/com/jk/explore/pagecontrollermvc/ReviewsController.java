package com.jk.explore.pagecontrollermvc;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * A new page: a new class, and nothing else changed.
 */
@RestController
public class ReviewsController {

    @GetMapping("/reviews")
    public String reviews(@RequestParam String sku) {
        return "reviews for " + sku + ": 4.5 stars from 12 customers";
    }
}
