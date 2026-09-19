package com.jk.explore.dto.naive;

import com.jk.explore.dto.domain.Customer;
import com.jk.explore.dto.json.MiniJson;

/** <strong>The naive endpoint: return the domain object.</strong> Whatever the object holds goes out. */
public class CustomerEndpointReturningTheDomainObject {

    public String get(Customer customer) {
        return MiniJson.write(customer);
    }
}
