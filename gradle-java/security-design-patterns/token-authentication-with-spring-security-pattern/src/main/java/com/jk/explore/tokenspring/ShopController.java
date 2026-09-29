package com.jk.explore.tokenspring;

import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import java.security.Principal;
import java.time.Duration;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.jwt.JwtEncoder;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * The shop's endpoints: the old session-based ones, the sign-in that issues a token, and the cart.
 */
@RestController
public class ShopController {

    private final JwtEncoder encoder;
    private final ShopApp app;

    public ShopController(JwtEncoder encoder, ShopApp app) {
        this.encoder = encoder;
        this.app = app;
    }

    /** Before: sign-in remembered in this server's own session memory. */
    @GetMapping("/session/login")
    public String sessionLogin(@RequestParam String customer, HttpSession session) {
        session.setAttribute("customer", customer);
        return "signed in";
    }

    @GetMapping("/session/cart")
    public String sessionCart(HttpSession session, HttpServletResponse response) {
        Object customer = session.getAttribute("customer");
        if (customer == null) {
            response.setStatus(401);
            return "please sign in";
        }
        return customer + "'s cart";
    }

    /** Sign in with a password once, and get a token valid for 15 minutes. */
    @PostMapping("/token")
    public String token(Principal user) {
        return ShopApp.issue(encoder, user.getName(), Duration.ofMinutes(15));
    }

    @GetMapping("/cart")
    public String cart(@AuthenticationPrincipal Jwt jwt) {
        return jwt.getSubject() + "'s cart";
    }

    /** Signing out early: this instance adds the token's identifier to its revoked list. */
    @PostMapping("/signout")
    public String signout(@AuthenticationPrincipal Jwt jwt) {
        app.revoked.add(jwt.getId());
        return "signed out";
    }
}
