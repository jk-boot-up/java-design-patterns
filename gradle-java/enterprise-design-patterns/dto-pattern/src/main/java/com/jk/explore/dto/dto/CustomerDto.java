package com.jk.explore.dto.dto;

/** <strong>A DTO: flat, immutable, shaped for the boundary.</strong> Exactly what this client needs. No behaviour. */
public record CustomerDto(int id, String name, String city) {
}
