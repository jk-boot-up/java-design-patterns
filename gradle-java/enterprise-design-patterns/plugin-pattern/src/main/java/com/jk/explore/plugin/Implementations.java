package com.jk.explore.plugin;

/**
 * The real and the safe versions of each service. Which one runs is decided by configuration.
 */
public final class Implementations {

    public static final class CardGateway implements Services.PaymentGateway {
        public String charge(String orderId, long pence) {
            return "REAL card charged " + PluginDemo.pounds(pence) + " for " + orderId;
        }
    }

    public static final class FakeGateway implements Services.PaymentGateway {
        public String charge(String orderId, long pence) {
            return "fake gateway approved " + PluginDemo.pounds(pence) + " for " + orderId;
        }
    }

    public static final class SmtpEmailer implements Services.Emailer {
        public String send(String to, String subject) {
            return "REAL email to " + to + ": " + subject;
        }
    }

    public static final class SandboxEmailer implements Services.Emailer {
        public String send(String to, String subject) {
            return "sandbox inbox kept email to " + to;
        }
    }

    private Implementations() {
    }
}
