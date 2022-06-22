package com.jk.explore.builder;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

public class StudentTest {

    @DisplayName("Student creation successful")
    @Test
    public void createStudent() {
        Student.Builder builder = Student.Builder.getInstance();
        Student student = builder.setName("XYZ").setId("1234").build();
        Assertions.assertEquals(student.getName(), "XYZ");
        Assertions.assertEquals(student.getId(), "1234");
    }

}
