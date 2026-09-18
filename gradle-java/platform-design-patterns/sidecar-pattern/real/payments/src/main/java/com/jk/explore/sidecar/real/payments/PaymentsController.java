package com.jk.explore.sidecar.real.payments;

import java.lang.management.ManagementFactory;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.time.Instant;
import java.util.LinkedHashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestClient;

/**
 * Everything this service knows about taking a payment.
 *
 * <p>It is one call to an address on its own machine. There is no loop, no
 * {@code catch} that tries again, no {@code Thread.sleep}, no timeout worth the
 * name and no idea that a payment provider exists. The entire method is the
 * three lines of {@link #pay}, and that is the whole claim Tier 1 makes in
 * Java, made here across a real process boundary instead.
 */
@RestController
public class PaymentsController {

    private final RestClient sidecar;
    private final String serviceName;
    private final String sidecarAddress;

    PaymentsController(RestClient.Builder builder,
                       @Value("${shop.service-name}") String serviceName,
                       @Value("${shop.sidecar-address}") String sidecarAddress) {
        this.serviceName = serviceName;
        this.sidecarAddress = sidecarAddress;
        this.sidecar = builder.baseUrl(sidecarAddress).build();
    }

    /**
     * Take a payment.
     *
     * <p>If the proxy next door is not running, the exception below is the
     * whole of this service's failure handling, and the payment does not
     * happen. That is not an oversight -- it is the second item on the
     * pattern's bill, and it is printed rather than described.
     */
    @PostMapping("/pay")
    public ResponseEntity<String> pay(@RequestBody String payment) {
        try {
            return sidecar.post()
                    .uri("/pay")
                    .header("Content-Type", "application/json")
                    .body(payment)
                    // `exchange` rather than `retrieve`, for one reason worth
                    // knowing: retrieve() throws on a 4xx or 5xx, and a decline
                    // and a refusal are both ordinary answers here that the
                    // caller is entitled to read. Nothing in this method treats
                    // a failure as something to try again.
                    .exchange((request, response) -> ResponseEntity
                            .status(response.getStatusCode())
                            .contentType(MediaType.APPLICATION_JSON)
                            .body(new String(response.getBody().readAllBytes(),
                                             StandardCharsets.UTF_8)));
        } catch (RuntimeException couldNotReachTheProxyNextDoor) {
            return ResponseEntity.status(502).body(
                    "{\"outcome\":\"no sidecar\",\"service\":\"" + serviceName + "\","
                    + "\"reached\":\"nothing -- " + sidecarAddress + " did not answer\","
                    + "\"note\":\"" + rootCause(couldNotReachTheProxyNextDoor) + "\"}");
        }
    }

    /** Who this container is, what it talks to, and how long it has been up. */
    @GetMapping("/about")
    public Map<String, Object> about() {
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("service", serviceName);
        out.put("talksTo", sidecarAddress);
        out.put("knowsTheProviderAddress", false);
        out.put("retryCode", "none -- see PaymentsController.pay");
        out.put("startedAt", startedAt().toString());
        out.put("upFor", Duration.ofMillis(ManagementFactory.getRuntimeMXBean().getUptime())
                .toSeconds() + "s");
        return out;
    }

    private Instant startedAt() {
        return Instant.ofEpochMilli(ManagementFactory.getRuntimeMXBean().getStartTime());
    }

    private String rootCause(Throwable t) {
        Throwable cause = t;
        while (cause.getCause() != null) {
            cause = cause.getCause();
        }
        String message = cause.getMessage() == null ? cause.getClass().getSimpleName()
                : cause.getMessage();
        return message.replace('"', '\'');
    }
}
