package com.jk.explore.circuitbreaker;

/**
 * What a simulated remote call throws when it does not answer.
 *
 * In a real system this would be a timeout, a refused connection or a 503. The
 * only thing the patterns in this category care about is that the call did not
 * produce an answer, so one exception covers all of it.
 */
public class ServiceUnavailableException extends RuntimeException {

    private final String serviceName;

    public ServiceUnavailableException(String serviceName) {
        super(serviceName + " did not answer");
        this.serviceName = serviceName;
    }

    /** Which service failed. Callers use this to decide whether they care. */
    public String serviceName() {
        return serviceName;
    }
}
