package com.jk.explore.secretsopenbao;

/**
 * The shop's side of OpenBao: store and rotate the payment key, write a policy, give each service
 * its own token, read with a token, and revoke a token.
 */
public final class Secrets {

    private final OpenBao bao;

    public Secrets(OpenBao bao) {
        this.bao = bao;
    }

    /** Writes a new version of the payment key in the key-value store. Returns the version number. */
    public int storePaymentKey(String value) throws Exception {
        OpenBao.Reply r = bao.call("POST", "secret/data/payment-key", OpenBao.ROOT, "{\"data\":{\"value\":\"" + value + "\"}}");
        return Integer.parseInt(r.field("version"));
    }

    /** A policy that may read the payment key and nothing else. */
    public void writePaymentsPolicy() throws Exception {
        String hcl = "path \\\"secret/data/payment-key\\\" { capabilities = [\\\"read\\\"] }";
        bao.call("PUT", "sys/policies/acl/payments", OpenBao.ROOT, "{\"policy\":\"" + hcl + "\"}");
    }

    /** A token for one service, carrying only the given policy. */
    public String tokenFor(String policy) throws Exception {
        return bao.call("POST", "auth/token/create", OpenBao.ROOT,
                "{\"policies\":[\"" + policy + "\"],\"no_default_policy\":true,\"ttl\":\"1h\"}").field("client_token");
    }

    /** Reads the payment key with a service's token: the value, or the refusal. */
    public OpenBao.Reply read(String token) throws Exception {
        return bao.call("GET", "secret/data/payment-key", token, null);
    }

    public OpenBao.Reply readVersion(String token, int version) throws Exception {
        return bao.call("GET", "secret/data/payment-key?version=" + version, token, null);
    }

    public void revoke(String token) throws Exception {
        bao.call("POST", "auth/token/revoke", OpenBao.ROOT, "{\"token\":\"" + token + "\"}");
    }
}
