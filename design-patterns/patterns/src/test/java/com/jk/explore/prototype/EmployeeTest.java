package com.jk.explore.prototype;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

public class EmployeeTest {

    @DisplayName("Test prototype design pattern with clone() method")
    @Test
    public void cloneEmployee() throws CloneNotSupportedException {
        Employee employee = new Employee("XYZ", "1234");
        Employee cloned = employee.clone();
        Assertions.assertNotNull(cloned);
        Assertions.assertEquals(employee.getName(), cloned.getName());
        Assertions.assertEquals(employee.getId(), cloned.getId());
    }
}
