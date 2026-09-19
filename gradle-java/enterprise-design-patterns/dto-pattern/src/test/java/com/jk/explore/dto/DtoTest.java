package com.jk.explore.dto;

import com.jk.explore.dto.domain.Customer;
import com.jk.explore.dto.dto.CustomerDetailDto;
import com.jk.explore.dto.dto.CustomerDto;
import com.jk.explore.dto.dto.CustomerMapper;
import com.jk.explore.dto.json.MiniJson;
import com.jk.explore.dto.naive.CustomerAfterRename;
import com.jk.explore.dto.naive.CustomerEndpointReturningTheDomainObject;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class DtoTest {

    @Test
    void returningTheDomainObjectLeaksThePasswordHash() {
        String json = new CustomerEndpointReturningTheDomainObject().get(Customer.ada());
        assertTrue(json.contains("passwordHash"));
        assertTrue(json.contains("$2a$10$"));
    }

    @Test
    void serialisingTheDomainObjectTouchesTheLazyOrderHistory() {
        Customer ada = Customer.ada();
        assertEquals(0, ada.orders().loadCount());
        String json = new CustomerEndpointReturningTheDomainObject().get(ada);
        assertEquals(1, ada.orders().loadCount());
        assertTrue(json.contains("\"orders\""));
        assertTrue(json.length() > 5_000, "the payload is enormous: " + json.length());
    }

    @Test
    void theJsonKeysAreTheNamesOfPrivateFieldsSoARenameBreaksTheClient() {
        String before = new CustomerEndpointReturningTheDomainObject().get(Customer.ada());
        assertEquals("Ada Lovelace", MiniJson.field(before, "name"));
        assertNull(MiniJson.field(MiniJson.write(new CustomerAfterRename()), "name"));
    }

    @Test
    void aDtoCarriesOnlyWhatTheClientNeedsAndTouchesNothingElse() {
        Customer ada = Customer.ada();
        String json = MiniJson.write(CustomerMapper.toDto(ada));
        assertEquals("{\"id\":7,\"name\":\"Ada Lovelace\",\"city\":\"London\"}", json);
        assertFalse(json.contains("passwordHash"));
        assertEquals(0, ada.orders().loadCount());
    }

    @Test
    void aDetailDtoThatNeedsTheOrderCountDoesLoadTheHistory() {
        Customer ada = Customer.ada();
        CustomerDetailDto detail = CustomerMapper.toDetail(ada);
        assertEquals(25, detail.orderCount());
        assertEquals(1, ada.orders().loadCount(), "the mapping decides what gets loaded");
    }

    @Test
    void aDtoIsARecordWithNoBehaviourAndTheDomainObjectEnforcesRules() {
        assertTrue(CustomerDto.class.isRecord());
        assertThrows(IllegalArgumentException.class, () -> Customer.ada().changeEmail("nonsense"));
        assertEquals("nonsense", new CustomerDetailDto(1, "n", "nonsense", "c", 0, 0).email(),
                "a DTO carries a bad email without complaint");
    }

    @Test
    void fourDtosCarryMoreFieldsThanTheDomainObjectHas() {
        int dtoFields = 0;
        for (Class<?> d : new Class<?>[]{CustomerDto.class, com.jk.explore.dto.dto.CustomerSummaryDto.class,
                com.jk.explore.dto.dto.CustomerListItemDto.class, CustomerDetailDto.class}) {
            dtoFields += d.getRecordComponents().length;
        }
        assertEquals(15, dtoFields);
    }
}
