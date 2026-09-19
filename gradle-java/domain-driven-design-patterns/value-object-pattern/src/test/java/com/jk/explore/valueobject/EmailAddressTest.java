package com.jk.explore.valueobject;

import com.jk.explore.valueobject.domain.EmailAddress;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class EmailAddressTest {

    @Test
    void normalisesCaseAndSpaces() {
        assertEquals("ada@example.com", EmailAddress.of("  Ada@Example.COM ").value());
        assertEquals(EmailAddress.of("ADA@example.com"), EmailAddress.of("ada@example.com"));
    }

    @Test
    void refusesWhatIsNotAnAddress() {
        for (String bad : new String[]{"", "ada", "ada@", "@example.com", "ada@example", "a da@example.com", null}) {
            assertThrows(IllegalArgumentException.class, () -> EmailAddress.of(bad), String.valueOf(bad));
        }
    }
}
