/**
 * {{ interface_name }}
 * {{ interface_description }}
 * 
 * Bounded Context: {{ bounded_context }}
 * Service: {{ service_name }}
 */

export interface {{ interface_name }} {
  {{ methods }}
}

// Data Transfer Objects
{{ dto_definitions }}

// Event Contracts
{{ event_contracts }}

// Domain Types
{{ domain_types }}