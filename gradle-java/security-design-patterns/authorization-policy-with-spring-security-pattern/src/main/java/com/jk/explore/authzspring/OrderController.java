package com.jk.explore.authzspring;

import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * The shop's order endpoints, each with its access rule written beside it.
 */
@RestController
public class OrderController {

    /** Before: signed in is enough; each endpoint was meant to check for itself, and this one forgot. */
    @GetMapping("/before/orders/{id}")
    public String viewBefore(@PathVariable String id) {
        return "order " + id;
    }

    /** Roles only: any customer may view orders, any order. */
    @GetMapping("/roles/orders/{id}")
    public String viewByRole(@PathVariable String id) {
        return "order " + id;
    }

    /** The owner, support staff or an admin. */
    @GetMapping("/orders/{id}")
    @PreAuthorize("@orderPolicy.owns(authentication, #id) or hasAnyRole('SUPPORT', 'ADMIN')")
    public String view(@PathVariable String id) {
        return "order " + id;
    }

    /** Support up to 100, admins any amount. */
    @PostMapping("/orders/{id}/refund")
    @PreAuthorize("hasRole('ADMIN') or (hasRole('SUPPORT') and #amount <= 100)")
    public String refund(@PathVariable String id, @RequestParam double amount) {
        return "refunded " + amount;
    }

    /** No rule was ever written for exporting, so the URL rules deny it. */
    @GetMapping("/orders/{id}/export")
    public String export(@PathVariable String id) {
        return "export of " + id;
    }
}
