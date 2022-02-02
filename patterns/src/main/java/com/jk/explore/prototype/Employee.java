package com.jk.explore.prototype;

public class Employee implements Cloneable {

    private final String name;
    private final String id;

    public Employee(String name, String id) {
        this.name = name;
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public String getId() {
        return id;
    }

    public Employee clone() throws CloneNotSupportedException {
        Employee employee = (Employee) super.clone();
        return employee;
    }



}
