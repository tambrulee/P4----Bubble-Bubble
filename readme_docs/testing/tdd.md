# Test-Driven Development (TDD) Summary

## Overview

Test-Driven Development principles were applied throughout the project to ensure reliability, maintainability, and predictable behaviour.  
Testing focused on validating core functionality, preventing regressions, and confirming that user stories were met as features were developed.

The approach combined **manual testing**, **automated testing**, and **code quality tools**, reflecting a pragmatic TDD workflow appropriate for a Django e-commerce application.

---

## Testing Strategy

The project followed a **red → green → refactor mindset**, where features were planned against user stories, expected behaviour was defined, and code was iteratively refined until requirements were met.

Testing was carried out at multiple levels:

- Feature and user story validation
- Form and view behaviour testing
- Defensive testing for edge cases
- Code quality and standards enforcement
- Deployment and production testing

---

## Manual Testing

Manual testing was used extensively to validate user-facing functionality.

[Click here to view all manual tests](/readme_docs/testing/manual_testing.md)

### Areas Covered
- Product browsing and category filtering
- Product detail pages rendering correctly
- Cart add, update, and remove functionality
- Checkout flow from cart to confirmation
- Authentication (login, logout, access control)
- Owner dashboard permissions and visibility
- Responsive behaviour across screen sizes

### Outcome
- Issues were identified early during feature development
- UI/UX bugs were resolved before feature completion
- Behaviour was verified against original user stories

---

## Automated Testing

Automated testing was used where appropriate to validate backend logic and reduce the risk of regressions.

### Django Testing
- Model behaviour tested to ensure correct data storage
- Views tested to confirm correct HTTP responses
- URL resolution tested to prevent routing errors
- Form validation tested to ensure defensive input handling

### Key Benefits
- Ensured critical flows remained stable during refactoring
- Helped catch errors such as missing URLs and invalid redirects
- Supported confidence when deploying changes

---

## Form & Validation Testing

Forms were tested to ensure:

- Required fields are enforced
- Invalid data is rejected safely
- Error messages are clear and user-friendly
- CSRF protection is active on POST requests

This was especially important for checkout, authentication, and owner-only forms.

---

## Code Quality & Linting

Static analysis tools were used as part of the testing process.

### Tools Used
- **Flake8** for Python code quality and PEP8 compliance
- **ESLint** for JavaScript validation
- **HTML & CSS validation tools**

### Common Issues Identified & Resolved
- Line length and formatting issues
- Unused imports and variables
- Undefined JavaScript references
- Template and URL mismatches

Linting helped maintain consistency and readability across the codebase.

---

## Defensive & Edge Case Testing

The application was tested against common edge cases, including:

- Empty carts
- Invalid quantities
- Unauthenticated access to protected views
- Non-staff access to owner routes
- Duplicate or malformed requests
- Missing CSRF tokens

These tests ensured the application fails safely and securely.

---

## Deployment Testing

Testing continued after deployment to ensure parity between development and production environments.

### Areas Tested
- Environment variables loading correctly
- Static files and media handling
- Stripe integration in production
- Authentication and permissions
- Error handling and logging

Deployment logs were monitored and issues resolved iteratively.

---

## Outcome

Applying TDD principles resulted in:
- A more stable and predictable codebase
- Faster identification of bugs during development
- Improved confidence when refactoring and deploying
- Clear traceability between user stories and tested behaviour

Testing was an ongoing process throughout the project lifecycle rather than a single final step.

---

# Known Bugs & Limitations

## Overview

This section outlines known bugs and current limitations within the application at the time of submission.  
None of the issues listed prevent core functionality or critical user journeys, and all were assessed as acceptable within the scope of the project.

---

## Known Bugs

| ID | Description | Impact | Status |
|----|------------|--------|--------|
| KB-01 | Cart quantity updates require form submission rather than instant update | Minor UX limitation | Accepted |
| KB-02 | Toast notifications may briefly overlap on rapid successive actions | Cosmetic | Accepted |
| KB-03 | Stripe webhook delays can cause brief lag before order status updates | Low | Accepted |
| KB-04 | Browser back button after checkout may display cached cart data | Low | Accepted |

---

## Technical Limitations

| ID | Description | Reason | Mitigation |
|----|------------|--------|------------|
| TL-01 | Cart is session-based rather than persistent across devices | Scope limitation | Acceptable for MVP |
| TL-02 | Limited automated test coverage for front-end interactions | Time constraints | Manual testing performed |
| TL-03 | Single-currency checkout | Project scope | Documented for future work |
| TL-04 | No guest order history | Design choice | Users encouraged to register |

---

## UX & Design Limitations

| ID | Description | Reason |
|----|------------|--------|
| UX-01 | No product search functionality | Not prioritised for MVP |
| UX-02 | Limited product filtering options | Reduced complexity |
| UX-03 | No customer review submission | Out of scope |

---

## Performance & Scalability Considerations

| ID | Description | Notes |
|----|------------|-------|
| PS-01 | Product images not aggressively optimised | Acceptable for current scale |
| PS-02 | Order management not paginated for large datasets | Suitable for small catalogue |
| PS-03 | No caching layer implemented | Not required at current traffic levels |

---

## Security Considerations

| ID | Description | Status |
|----|------------|--------|
| SC-01 | Rate limiting not implemented on authentication views | Low risk for MVP |
| SC-02 | No CAPTCHA on forms | Acceptable within scope |

All core security best practices such as CSRF protection, authentication checks, and permission restrictions are in place.

---

## Future Improvements

Potential enhancements identified for future development include:
- Enhanced order analytics for owners
- Improved test automation coverage
- Delivery/dispatch order user updates

---

## Sign-Off

All known issues were reviewed and deemed non-critical.  
The application meets the project requirements and performs reliably within its defined scope.


