package com.jk.explore.proxyspring;

import org.springframework.stereotype.Service;

@Service
public class RefundDesk {
    @RequiresRole(Role.CATALOG_ADMIN)
    public String refund(String orderNumber) {
        return orderNumber + " refunded";
    }
}
