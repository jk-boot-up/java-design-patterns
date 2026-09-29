package com.jk.explore.stijpa.single;

import jakarta.persistence.DiscriminatorColumn;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Inheritance;
import jakarta.persistence.InheritanceType;
import jakarta.persistence.Table;

/**
 * The pattern: every kind of product in one table, called product. A column named type says which class
 * each row is; Hibernate writes it on save and reads it to build the right class on load.
 */
@Entity
@Table(name = "product")
@Inheritance(strategy = InheritanceType.SINGLE_TABLE)
@DiscriminatorColumn(name = "type")
public abstract class Product {

    @Id
    private String sku;
    private String name;
    private int pence;

    protected Product() {
    }

    protected Product(String sku, String name, int pence) {
        this.sku = sku;
        this.name = name;
        this.pence = pence;
    }

    public String getSku() {
        return sku;
    }

    public String getName() {
        return name;
    }

    /** What the warehouse needs to know about this kind of product. */
    public abstract String detail();
}
