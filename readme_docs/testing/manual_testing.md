# Manual Testing

## Overview

This section documents the manual testing performed during development to verify that core user journeys function as expected.  
Each test includes the expected outcome and a final pass/fail sign-off to confirm correct behaviour.

---

## Product Browsing & Display

| Test Case | Action Performed | Expected Outcome | Result (Y/N) |
|---------|----------------|------------------|--------------|
| View all products | Navigate to shop page | All active products display correctly | Y |
| Filter by category | Select a product category | Only products in selected category display | Y |
| View product detail | Click on a product | Product detail page loads with correct info | Y |
| Out-of-stock handling | Attempt to view unavailable product | Add-to-cart disabled or hidden | Y |

---

## Cart Functionality

| Test Case | Action Performed | Expected Outcome | Result (Y/N) |
|---------|----------------|------------------|--------------|
| Add to cart | Click “Add to cart” on product | Product added and confirmation shown | Y |
| Update quantity | Change item quantity in cart | Quantity updates and totals recalculate | Y |
| Remove item | Remove item from cart | Item removed and totals update | Y |
| Empty cart | View cart with no items | Empty cart message displayed | Y |

---

## Checkout Process

| Test Case | Action Performed | Expected Outcome | Result (Y/N) |
|---------|----------------|------------------|--------------|
| Access checkout | Proceed from cart to checkout | Checkout page loads successfully | Y |
| Required fields | Submit checkout with missing fields | Validation errors displayed | Y |
| Valid submission | Submit valid checkout form | Order created and payment processed | Y |
| Confirmation page | Complete checkout | Order confirmation page displayed | Y |

---

## Authentication & Accounts

| Test Case | Action Performed | Expected Outcome | Result (Y/N) |
|---------|----------------|------------------|--------------|
| Register account | Submit registration form | Account created successfully | Y |
| Login | Submit valid login credentials | User logged in successfully | Y |
| Logout | Click logout | User logged out and redirected | Y |
| Access control | Access protected page while logged out | Redirected to login page | Y |

---

## Owner / Admin Functionality

| Test Case | Action Performed | Expected Outcome | Result (Y/N) |
|---------|----------------|------------------|--------------|
| Staff access | Login as staff user | Owner dashboard accessible | Y |
| Non-staff access | Login as normal user | Owner routes blocked | Y |
| Create product | Add product via owner dashboard | Product saved and visible in store | Y |
| View orders | Access order list | Orders display correctly | Y |

---

## UX & Responsiveness

| Test Case | Action Performed | Expected Outcome | Result (Y/N) |
|---------|----------------|------------------|--------------|
| Mobile navigation | View site on mobile | Menu collapses and works correctly | Y |
| Toast messages | Add item to cart | Feedback message shown | Y |
| Form errors | Submit invalid form | Clear error messages shown | Y |
| Responsive layout | Resize browser window | Layout adapts without breaking | Y |

---

## Security & Defensive Testing

| Test Case | Action Performed | Expected Outcome | Result (Y/N) |
|---------|----------------|------------------|--------------|
| CSRF protection | Submit POST without token | Request blocked | Y |
| Invalid quantities | Enter invalid cart quantity | Input rejected safely | Y |
| Direct URL access | Access staff URL as non-staff | Access denied | Y |

---

## Final Sign-Off

All manually tested features behaved as expected across the tested scenarios.  
No critical bugs were identified during final testing.

**Overall Manual Test Status:** ✅ **PASS**

