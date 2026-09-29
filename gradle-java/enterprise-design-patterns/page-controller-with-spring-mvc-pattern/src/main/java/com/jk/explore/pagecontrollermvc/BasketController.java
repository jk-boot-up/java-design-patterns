package com.jk.explore.pagecontrollermvc;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * The basket page's own controller. Spring converts qty to an int, and answers 400 by itself if it is not a number.
 */
@RestController
public class BasketController {

    @GetMapping("/basket")
    public String basket(@RequestParam String add, @RequestParam int qty) {
        return "basket: " + qty + " x " + add;
    }
}
