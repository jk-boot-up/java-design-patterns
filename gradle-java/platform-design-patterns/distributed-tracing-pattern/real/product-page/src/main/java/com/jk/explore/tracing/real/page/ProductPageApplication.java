package com.jk.explore.tracing.real.page;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * The front door, and the service that mints the trace id.
 *
 * <p>Tier 1's {@code ProductPageDemo} did all of this in one JVM with a
 * {@code Tracer} of its own. Here the tracer is OpenTelemetry's, the spans leave
 * the process over OTLP, and the interesting line of code is the one that is
 * missing: nothing in this service writes a {@code traceparent} header.
 */
@SpringBootApplication
public class ProductPageApplication {

    public static void main(String[] args) {
        SpringApplication.run(ProductPageApplication.class, args);
    }
}
