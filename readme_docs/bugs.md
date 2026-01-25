# Bugs, Fixes & Known Issues

This section documents bugs identified during development and testing, how they were resolved, and any remaining known issues. Tracking and resolving these bugs via GitHub Issues ensured stability, usability, and polish prior to final submission.

---

## Resolved Bugs

### Admin & Owner Dashboard

- **Admin orders – dispatch/deliver buttons squished (#152)**  
  Buttons were compressed on smaller screens. Fixed by adjusting responsive layout and spacing.

- **Admin product – max products per page (#151)**  
  Added pagination limits to improve readability and performance.

- **'View' button alignment on order page (#116)**  
  Corrected table and button alignment.

- **Hide abandoned checkouts (#105)**  
  Excluded unpaid/abandoned orders from default admin views.

- **Reviewer name display (#100)**  
  Fixed template context to display reviewer names correctly.

- **Logout issues for shop owners (#90)**  
  Corrected authentication flow to ensure clean logout.

---

### Shopping, Checkout & Forms

- **Checkout form missing address validation (#145)**  
  Added server-side validation to prevent incomplete submissions.

- **Mini cart redirect issue (#120)**  
  Updated JavaScript to allow item removal without page navigation.

- **Shipping addresses not saving (#111)**  
  Corrected form handling and model save logic.

- **Newsletter not working (#106)**  
  Marked as not planned due to scope constraints.

---

### UI / UX & Visual Bugs

- **About page hero sizing on iPad (#150)**  
  Adjusted responsive image sizing.

- **Shop all – product limit view (#149)**  
  Improved grid layout and pagination.

- **Outline buttons not visible (#143, #137)**  
  Updated button styles for better contrast and accessibility.

- **Remove redundant filters (#136)**  
  Simplified filter options to reduce clutter.

- **Our Story CSS missing (#133)**  
  Restored missing stylesheet rules.

- **Category hero banner issues (#131)**  
  Fixed template inheritance and image rendering.

- **Burger icon missing (#130)**  
  Corrected icon imports and markup.

- **404 / 500 pages not rendering (#120)**  
  Wired up custom error handlers and templates.

- **Navigation spacing issues (#118)**  
  Adjusted layout spacing.

- **Mobile icon alignment (#89)**  
  Fixed flexbox alignment for small screens.

- **Footer shop links incorrect (#134)**  
  Corrected URL routing.

- **Dashboard image redirect issue (#135)**  
  Fixed anchor link targets.

---

## Known / Unresolved Issues

- **Button margins on product edit page (#159)**  
  Minor cosmetic spacing issue.
  
  * Resolved: 24/01/2025
  * Resolution: Changes to Bootstrap and Custom CSS

- **Missing page titles (#156)**  
  SEO/accessibility enhancement pending.
  * Resolved: 24/01/2025
  * Resolution: Page titles added to relevant templates

- **Django shell visible on admin access (#155)**  
  Requires stricter access control and custom error handling.
  * Resolved: 24/01/2025
  * Resolution: Added explicit redirect to owner view authentication

---

## Summary

Bug tracking via GitHub Issues enabled structured testing and iterative refinement. The majority of bugs were UX and layout-related rather than core logic issues, demonstrating a stable underlying architecture. Remaining issues are documented for transparency and future improvement.
