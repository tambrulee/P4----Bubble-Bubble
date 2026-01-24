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
|---------|-------------------|------------------|--------------|
| Admin login | Login as staff user | Owner dashboard loads successfully | Y |
| Non-staff blocked | Attempt to access owner routes as normal user | Redirected / access denied | Y |
| Dashboard navigation | Use dashboard shortcut cards/links | Correct admin pages open | Y |
| Dashboard image links | Click image / CTA links from dashboard | Redirects correctly (no broken routes) | Y |

---

### Product Management (Owner)

| Test Case | Action Performed | Expected Outcome | Result (Y/N) |
|---------|-------------------|------------------|--------------|
| View products list | Open Products admin list | Products display with correct status labels | Y |
| Filter products | Apply filters (active/inactive/low stock/tags) | Product list updates correctly | Y |
| Pagination limit | Load product list with many products | Max products per page applied + pagination works | Y |
| Create product | Submit new product form | Product saved and appears in store | Y |
| Edit product | Update title/price/stock/tags | Changes persist and display correctly | Y |
| Duplicate product | Duplicate an existing product | New product created with copied fields and unique slug | Y |
| Hide product | Click hide / deactivate action | Product no longer visible to shoppers | Y |
| Activate product | Reactivate a hidden product | Product becomes visible in store again | Y |
| Image manager | Upload/update product images | Images saved and render on product cards/detail pages | Y |
| Delete product (safe) | Delete product that has **no** orders/cart references | Product is deleted successfully | Y |
| Delete product (protected) | Attempt to delete product that is **in a cart** or has **OrderItems** | Deletion blocked; product is archived/inactivated instead and user sees message | Y |
| Stock/availability behaviour | Set stock to 0 | Add-to-cart disabled and “Out of stock” displayed | Y |

---

### Order Management (Owner)

| Test Case | Action Performed | Expected Outcome | Result (Y/N) |
|---------|-------------------|------------------|--------------|
| View orders list | Open Orders admin list | Paid orders display correctly | Y |
| Abandoned checkout hidden | Attempt to view unpaid/abandoned checkouts | Not shown in default admin list | Y |
| Order detail view | Click view on an order | Full order summary loads (items, customer, totals) | Y |
| Fulfilment status grouping | Switch between New/Dispatched/Delivered | Orders filter/group correctly | Y |
| Dispatch order | Mark order as dispatched | Status updates; UI remains usable/responsive | Y |
| Deliver order | Mark order as delivered | Status updates correctly | Y |
| Button layout (admin) | View dispatch/deliver buttons on different screens | Buttons not squished; readable and clickable | Y |

---

### Review Management (Owner)

| Test Case | Action Performed | Expected Outcome | Result (Y/N) |
|---------|-------------------|------------------|--------------|
| View reviews list | Open Reviews admin list | Reviews display with rating, product, user, and status | Y |
| Filter reviews | Filter by rating/replied/hidden/approved | Results update correctly | Y |
| Approve review | Approve a pending review | Review becomes visible on product page | Y |
| Hide review | Hide an approved review | Review removed from public display | Y |
| Reply to review | Submit admin reply | Reply saved and displayed appropriately | Y |
| Toast feedback | Approve/hide/reply actions | Toast/confirmation feedback displayed | Y |
| Verified purchase flag | View a review linked to an order | Verified purchase shown correctly | Y |

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

