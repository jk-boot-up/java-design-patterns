package com.jk.explore.contract;

import java.util.Map;

/** Another consumer. It only reads the sku. */
public class Reports {

    public static final Contract CONTRACT = new Contract("reports", Map.of("sku", Type.STRING));
}
