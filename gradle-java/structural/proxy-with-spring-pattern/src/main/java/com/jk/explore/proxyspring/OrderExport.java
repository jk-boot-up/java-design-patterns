package com.jk.explore.proxyspring;

import org.springframework.stereotype.Service;

@Service
public class OrderExport {
    @RequiresRole(Role.CATALOG_ADMIN)
    public String exportAll() {
        return "all orders exported";
    }
}
