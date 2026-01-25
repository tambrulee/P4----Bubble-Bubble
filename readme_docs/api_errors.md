## API Integration & Error Handling

## Overview

The BubbleBubble (Moon & Moss) application integrates with external services in a controlled and defensive manner.  
The primary external API used is **Stripe**, which handles secure payment processing. The application is designed to handle invalid user input, API failures, and asynchronous events gracefully, without exposing sensitive data or breaking user journeys.

---

## Stripe API Integration

Stripe is used to manage all payment-related functionality, ensuring that sensitive payment details are never stored or processed directly by the application.

Key characteristics of the integration include:
- Secure redirection to Stripe Checkout for payment entry
- Server-side creation of payment sessions
- Use of environment variables for all API keys
- Separation of payment logic from core order logic

This approach aligns with industry best practices and reduces the security surface area of the application.

---

## Handling User Input Errors

User input is validated at multiple layers to prevent invalid or incomplete data from reaching business logic or external services.

Examples include:
- **Form-level validation** using Django forms to ensure required checkout fields are completed
- Inline error messages guiding users to correct mistakes
- Defensive handling of edge cases such as:
  - Missing address details
  - Invalid quantities
  - Duplicate account registrations

Invalid submissions are rejected gracefully with clear feedback, allowing users to recover without losing progress.

---

## Handling External API Errors (Stripe)

The application accounts for potential failures when interacting with the Stripe API, including:
- Network interruptions
- Payment cancellations
- Incomplete or failed transactions

Safeguards include:
- Orders remain in a *pending* state until payment is confirmed
- Users who cancel or fail payment are safely returned to the application
- No order is marked as paid unless Stripe confirms success
- Sensitive error information is never exposed to the user

This ensures system integrity even when external services do not respond as expected.

---

## Asynchronous Processes & Webhooks

Stripe webhooks are used to handle asynchronous payment confirmation events.

This allows the application to:
- Confirm payment completion independently of the user’s browser session
- Update order status reliably after checkout
- Prevent race conditions or duplicate order processing

Webhook events are verified using Stripe’s signature validation to ensure authenticity and protect against spoofed requests.

---

## Defensive Programming & System Stability

Across the application, defensive programming techniques are used to maintain stability:

- Permission checks prevent unauthorised access to protected routes
- Database constraints protect referential integrity (e.g. products linked to orders cannot be deleted)
- Try/except handling around critical operations
- Clear separation between user-facing feedback and internal error logging

These measures ensure the application remains stable and predictable even when unexpected inputs or failures occur.

---

## Summary

The application demonstrates robust handling of external dependencies, user input, and asynchronous processes.  
By combining Django’s validation mechanisms with Stripe’s secure API and webhook system, the platform maintains a reliable and user-friendly experience while protecting both user data and system integrity.
