package com.jk.explore.facade;

public class InventoryService {

    public boolean reserveStock(String productId, int quantity) {
        System.out.println("Inventory: reserving " + quantity + " unit(s) of " + productId);
        return true;
    }
}
