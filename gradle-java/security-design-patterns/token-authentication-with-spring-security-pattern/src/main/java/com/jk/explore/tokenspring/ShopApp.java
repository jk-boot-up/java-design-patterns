package com.jk.explore.tokenspring;

import com.nimbusds.jose.jwk.source.ImmutableSecret;
import java.time.Duration;
import java.time.Instant;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.oauth2.core.DelegatingOAuth2TokenValidator;
import org.springframework.security.oauth2.core.OAuth2Error;
import org.springframework.security.oauth2.core.OAuth2TokenValidatorResult;
import org.springframework.security.oauth2.jose.jws.MacAlgorithm;
import org.springframework.security.oauth2.jwt.JwtClaimsSet;
import org.springframework.security.oauth2.jwt.JwtDecoder;
import org.springframework.security.oauth2.jwt.JwtEncoder;
import org.springframework.security.oauth2.jwt.JwtEncoderParameters;
import org.springframework.security.oauth2.jwt.JwsHeader;
import org.springframework.security.oauth2.jwt.JwtTimestampValidator;
import org.springframework.security.oauth2.jwt.NimbusJwtDecoder;
import org.springframework.security.oauth2.jwt.NimbusJwtEncoder;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.SecurityFilterChain;

/**
 * One instance of the shop's web server, secured by Spring Security. Every instance is started with the
 * same signing secret, so a token issued by one is accepted by all.
 */
@SpringBootApplication
public class ShopApp {

    /** Token identifiers this instance has been told are signed out. Each instance keeps its own. */
    public final Set<String> revoked = ConcurrentHashMap.newKeySet();

    @Bean
    SecretKey signingKey(@Value("${shop.secret}") String secret) {
        return new SecretKeySpec(secret.getBytes(), "HmacSHA256");
    }

    @Bean
    SecurityFilterChain security(HttpSecurity http) throws Exception {
        return http
                .authorizeHttpRequests(a -> a.requestMatchers("/session/**").permitAll().anyRequest().authenticated())
                .httpBasic(Customizer.withDefaults())                              // for signing in at /token
                .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))      // Bearer tokens everywhere else
                .csrf(c -> c.disable())
                .build();
    }

    @Bean
    UserDetailsService users() {
        return new InMemoryUserDetailsManager(User.withUsername("ana").password("{noop}demo-password").roles("CUSTOMER").build());
    }

    @Bean
    JwtEncoder jwtEncoder(SecretKey key) {
        return new NimbusJwtEncoder(new ImmutableSecret<>(key));
    }

    /** Checks the signature, the expiry (with no clock allowance), and this instance's revoked list. */
    @Bean
    JwtDecoder jwtDecoder(SecretKey key) {
        NimbusJwtDecoder decoder = NimbusJwtDecoder.withSecretKey(key).macAlgorithm(MacAlgorithm.HS256).build();
        decoder.setJwtValidator(new DelegatingOAuth2TokenValidator<>(
                new JwtTimestampValidator(Duration.ZERO),
                jwt -> revoked.contains(jwt.getId())
                        ? OAuth2TokenValidatorResult.failure(new OAuth2Error("invalid_token", "revoked", null))
                        : OAuth2TokenValidatorResult.success()));
        return decoder;
    }

    /** Issues a signed token for a customer, lasting {@code lifetime} (negative: already expired). */
    public static String issue(JwtEncoder encoder, String customer, Duration lifetime) {
        Instant now = Instant.now();
        JwtClaimsSet claims = JwtClaimsSet.builder()
                .subject(customer)
                .issuedAt(lifetime.isNegative() ? now.plus(lifetime).minusSeconds(60) : now)
                .expiresAt(now.plus(lifetime))
                .id(UUID.randomUUID().toString())
                .build();
        return encoder.encode(JwtEncoderParameters.from(JwsHeader.with(MacAlgorithm.HS256).build(), claims)).getTokenValue();
    }
}
