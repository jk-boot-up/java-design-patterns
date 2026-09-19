package com.jk.explore.datamapper.pattern;

import com.jk.explore.datamapper.domain.Address;
import com.jk.explore.datamapper.domain.Customer;
import com.jk.explore.datamapper.toydb.Database;
import com.jk.explore.datamapper.toydb.Row;

/**
 * <strong>The bill: a hand-written mapping is easy to get subtly wrong.</strong>
 * This mapper forgets the postcode when it writes the address. Nothing fails.
 * Every call succeeds, and the field simply does not come back.
 */
public class CarelessCustomerMapper extends CustomerMapper {

    public CarelessCustomerMapper(Database database) {
        super(database);
    }

    @Override
    protected Row addressRow(Address address) {
        return Row.of("street", address.street(), "city", address.city());
    }
}
