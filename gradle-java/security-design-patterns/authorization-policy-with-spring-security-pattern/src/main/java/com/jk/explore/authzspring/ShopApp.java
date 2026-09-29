package com.jk.explore.authzspring;

import jakarta.servlet.DispatcherType;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.context.annotation.Bean;
import org.springframework.context.event.EventListener;
import org.springframework.http.HttpMethod;
import org.springframework.security.authorization.AuthorizationEventPublisher;
import org.springframework.security.authorization.SpringAuthorizationEventPublisher;
import org.springframework.security.authorization.event.AuthorizationDeniedEvent;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.SecurityFilterChain;

/**
 * The shop's web server with Spring Security deciding access. URL rules come first; method rules,
 * written next to each endpoint, decide the rest; anything no rule mentions is denied.
 */
@SpringBootApplication
@EnableMethodSecurity
public class ShopApp {

    /** Every refusal Spring Security announces, with the reason. */
    public final List<String> denials = new CopyOnWriteArrayList<>();

    @Bean
    SecurityFilterChain security(HttpSecurity http) throws Exception {
        return http
                .authorizeHttpRequests(a -> a
                        .dispatcherTypeMatchers(DispatcherType.ERROR).permitAll()                    // Spring's own error page
                        .requestMatchers("/before/**").authenticated()
                        .requestMatchers(HttpMethod.GET, "/roles/orders/**").hasRole("CUSTOMER")    // roles only
                        .requestMatchers("/orders/*", "/orders/*/refund").authenticated()            // method rules decide
                        .anyRequest().denyAll())                                                     // deny by default
                .httpBasic(Customizer.withDefaults())
                .csrf(c -> c.disable())
                .build();
    }

    @Bean
    UserDetailsService users() {
        return new InMemoryUserDetailsManager(
                User.withUsername("ana").password("{noop}pw").roles("CUSTOMER").build(),
                User.withUsername("ben").password("{noop}pw").roles("CUSTOMER").build(),
                User.withUsername("sam").password("{noop}pw").roles("SUPPORT").build(),
                User.withUsername("alex").password("{noop}pw").roles("ADMIN").build());
    }

    /** Spring Security announces each refusal as an event; without this bean, it announces nothing. */
    @Bean
    AuthorizationEventPublisher authorizationEvents(ApplicationEventPublisher publisher) {
        return new SpringAuthorizationEventPublisher(publisher);
    }

    @EventListener
    public void onDenied(AuthorizationDeniedEvent<?> event) {
        denials.add(event.getAuthentication().get().getName() + " refused");
    }
}
