package com.jk.explore.dto.dto;

import com.jk.explore.dto.domain.Customer;

/**
 * <strong>The mapping code, and the bill.</strong> Every DTO needs a method
 * that copies fields across by hand. It is tedious, it is everywhere, and a
 * new field on the domain object silently does not reach a DTO that was not
 * updated.
 */
public final class CustomerMapper {

    private CustomerMapper() {
    }

    public static CustomerDto toDto(Customer c) {
        return new CustomerDto(c.id(), c.name(), c.city());
    }

    public static CustomerSummaryDto toSummary(Customer c) {
        return new CustomerSummaryDto(c.id(), c.name());
    }

    public static CustomerListItemDto toListItem(Customer c) {
        return new CustomerListItemDto(c.id(), c.name(), c.city(), c.loyaltyPoints());
    }

    public static CustomerDetailDto toDetail(Customer c) {
        return new CustomerDetailDto(c.id(), c.name(), c.email(), c.city(), c.loyaltyPoints(), c.orders().size());
    }
}
