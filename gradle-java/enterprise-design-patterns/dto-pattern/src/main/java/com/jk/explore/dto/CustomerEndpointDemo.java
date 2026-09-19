package com.jk.explore.dto;

import com.jk.explore.dto.domain.Customer;
import com.jk.explore.dto.dto.CustomerDetailDto;
import com.jk.explore.dto.dto.CustomerDto;
import com.jk.explore.dto.dto.CustomerListItemDto;
import com.jk.explore.dto.dto.CustomerMapper;
import com.jk.explore.dto.dto.CustomerSummaryDto;
import com.jk.explore.dto.json.MiniJson;
import com.jk.explore.dto.naive.CustomerAfterRename;
import com.jk.explore.dto.naive.CustomerEndpointReturningTheDomainObject;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.lang.reflect.RecordComponent;
import java.util.Arrays;

/** Six acts. Every size and count is measured from the real payload. */
public final class CustomerEndpointDemo {

    public static void main(String[] args) {
        System.out.println("DTO — the object that crosses the boundary\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    private static void actOne() {
        System.out.println("ONE. A REST endpoint returns the domain object.");
        Customer ada = Customer.ada();
        String json = new CustomerEndpointReturningTheDomainObject().get(ada);
        System.out.println("  the JSON starts: " + json.substring(0, 120) + "...");
        System.out.println("  contains the password hash: " + json.contains("passwordHash"));
        System.out.println("  order history in it: " + json.contains("\"orders\"") + ", history loaded " + ada.orders().loadCount()
                + " time, just to serialise");
        System.out.println("  size: " + json.length() + " characters, for a customer's name and city.\n");
    }

    private static void actTwo() {
        System.out.println("TWO. The field name the client depends on is a private field.");
        Customer ada = Customer.ada();
        String json = new CustomerEndpointReturningTheDomainObject().get(ada);
        System.out.println("  a client reads the key \"name\": " + MiniJson.field(json, "name"));
        ada.rename("Augusta Ada King");
        System.out.println("  the name changes, and the client still gets it: " + MiniJson.field(new CustomerEndpointReturningTheDomainObject().get(ada), "name"));
        String afterRename = MiniJson.write(new CustomerAfterRename());
        System.out.println("  a developer renames the private field name to fullName. the JSON is now: " + afterRename);
        System.out.println("  the client reads the key \"name\": " + MiniJson.field(afterRename, "name"));
        System.out.println("  the JSON keys are the names of private fields. nobody may rename them now.\n");
    }

    private static void actThree() {
        System.out.println("THREE. The pattern — a DTO shaped for the boundary.");
        Customer ada = Customer.ada();
        String domainJson = new CustomerEndpointReturningTheDomainObject().get(Customer.ada());
        String dtoJson = MiniJson.write(CustomerMapper.toDto(ada));
        System.out.println("  domain object: " + domainJson.length() + " characters");
        System.out.println("  DTO:           " + dtoJson.length() + " characters");
        System.out.println("  DTO payload:   " + dtoJson);
        System.out.println("  order history loaded by the DTO: " + ada.orders().loadCount() + " times.\n");
    }

    private static void actFour() {
        System.out.println("FOUR. A DTO is not a domain model — one of each.");
        System.out.println("  CustomerDto is a record: " + CustomerDto.class.isRecord() + ", methods of its own: "
                + ownBehaviour(CustomerDto.class));
        System.out.println("  Customer has rules: " + ownBehaviour(Customer.class));
        Customer c = Customer.ada();
        try {
            c.changeEmail("nonsense");
        } catch (IllegalArgumentException e) {
            System.out.println("  the domain object refuses a bad email: " + e.getMessage());
        }
        System.out.println("  the DTO would carry it without complaint. it is data, not a model.\n");
    }

    private static void actFive() {
        System.out.println("FIVE. The bill — mapping code, everywhere.");
        Class<?>[] dtos = {CustomerDto.class, CustomerSummaryDto.class, CustomerListItemDto.class, CustomerDetailDto.class};
        int dtoFields = 0;
        for (Class<?> d : dtos) {
            dtoFields += d.getRecordComponents().length;
            System.out.println("    " + d.getSimpleName() + ": " + fieldNames(d));
        }
        int domainFields = (int) Arrays.stream(Customer.class.getDeclaredFields())
                .filter(f -> !Modifier.isStatic(f.getModifiers())).count();
        System.out.println("  Customer has " + domainFields + " fields. four DTOs carry " + dtoFields + " between them.");
        System.out.println("  four mapping methods copy them across by hand. add a field and every one is a place to forget.\n");
    }

    private static void actSix() {
        System.out.println("SIX. Where you have already met this.");
        System.out.println("  a Java record returned from a Spring controller is a DTO, and Jackson writes its JSON.");
        System.out.println("  it is Backends for Frontends, at the level of one object instead of one deployment.");
        System.out.println("  MapStruct writes the mapping code for you: worth taking once you have felt the tedium.");
    }

    private static String ownBehaviour(Class<?> type) {
        return Arrays.stream(type.getDeclaredMethods()).filter(m -> !Modifier.isStatic(m.getModifiers())).map(Method::getName)
                .filter(n -> !n.equals("equals") && !n.equals("hashCode") && !n.equals("toString"))
                .filter(n -> !isAccessor(type, n)).sorted().toList().toString();
    }

    private static boolean isAccessor(Class<?> type, String name) {
        if (type.isRecord()) {
            return Arrays.stream(type.getRecordComponents()).anyMatch(c -> c.getName().equals(name));
        }
        return Arrays.stream(type.getDeclaredFields()).anyMatch(f -> f.getName().equals(name));
    }

    private static String fieldNames(Class<?> record) {
        return Arrays.stream(record.getRecordComponents()).map(RecordComponent::getName).toList().toString();
    }
}
