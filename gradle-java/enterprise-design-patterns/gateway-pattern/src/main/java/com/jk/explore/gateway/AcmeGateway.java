package com.jk.explore.gateway;

import com.jk.explore.gateway.vendor.AcmeClient;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * The only class that knows Acme's request fields and result codes. It also keeps the rules about talking to
 * a flaky network in one place: a timeout is tried once more before the shop is told.
 */
public class AcmeGateway implements PaymentGateway {

    private final AcmeClient client;
    private final List<String> log;

    public AcmeGateway(AcmeClient client, List<String> log) {
        this.client = client;
        this.log = log;
    }

    @Override
    public PaymentResult charge(long pence, String card) {
        for (int attempt = 1; ; attempt++) {
            Map<String, String> request = new HashMap<>();
            request.put("amt_minor", String.valueOf(pence));
            request.put("ccy", "GBP");
            request.put("pan_token", card);
            Map<String, String> response = client.postCharge(request);
            switch (response.get("rsp_code")) {
                case "00":
                    return new PaymentResult(PaymentStatus.APPROVED, response.get("txn_ref"));
                case "51":
                    return new PaymentResult(PaymentStatus.DECLINED, null);
                case "91":
                    log.add("acme timed out on attempt " + attempt);
                    if (attempt == 2) {
                        return new PaymentResult(PaymentStatus.UNAVAILABLE, null);
                    }
                    break;
                default:
                    throw new IllegalStateException("unknown Acme code " + response.get("rsp_code"));
            }
        }
    }
}
