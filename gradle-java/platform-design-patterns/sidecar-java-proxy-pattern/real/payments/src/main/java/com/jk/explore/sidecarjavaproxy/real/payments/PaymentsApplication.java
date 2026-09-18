package com.jk.explore.sidecarjavaproxy.real.payments;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * A part of the shop that takes money.
 *
 * <p>One image, started twice: once as {@code checkout} and once as
 * {@code refunds}. In Tier 1 these are separate classes with separate copies of
 * the retry policy, because the copies are what Tier 1 is about. Here the
 * copies are already gone, so what is left of the two services is identical and
 * pretending otherwise would only add code to read.
 *
 * <p>The thing to notice is what is <b>not</b> in this package. There is no
 * retry, no backoff, no deadline, no certificate, no counter, and no address for
 * the payment provider. Search the source for "retry" and you will find this
 * sentence and nothing else. All of it lives in a proxy running beside this
 * process, in a different container, written by somebody else, in a language
 * that is not Java.
 */
@SpringBootApplication
public class PaymentsApplication {

    public static void main(String[] args) {
        SpringApplication.run(PaymentsApplication.class, args);
    }
}
