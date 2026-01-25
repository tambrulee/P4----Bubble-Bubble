## Performance & Lighthouse Optimisation

Performance was evaluated using **Google Lighthouse** in Chrome DevTools, with a focus on real-world user experience rather than chasing artificial 100/100 scores. The application achieves a **strong overall Performance score (mid-to-high 70s and above)**, with clear evidence of deliberate optimisation across images, CSS delivery, caching, and render behaviour.

## Initial Analysis (Lighthouse)

An initial Lighthouse analysis was conducted early in development to act primarily as an **accessibility diagnostic tool**, rather than as a performance benchmarking exercise.

The purpose of this first audit was to:
- identify accessibility issues affecting real users (screen readers, keyboard navigation, low-vision users)
- highlight semantic and structural problems in templates and forms
- surface contrast, labelling, and ARIA-related issues that are difficult to detect visually

While Lighthouse also reports performance metrics, these were treated as **contextual signals** rather than absolute targets. Performance optimisation was considered where it aligned naturally with accessibility improvements or where issues were clearly impacting user experience.

---

### Accessibility Focus of the Initial Analysis

The initial Lighthouse reports highlighted several common accessibility concerns, including:
- form inputs without explicit label associations
- low-contrast text and outline-only buttons
- misuse or overuse of ARIA attributes
- layout instability caused by images without intrinsic dimensions
- inconsistent navigation visibility across categories

These findings informed a series of targeted refinements across both user-facing and administrative templates.

---

### Performance Considerations During Initial Analysis

Although accessibility was the primary focus, opportunities to improve performance were addressed where they supported accessibility goals, such as:

- resizing and compressing images to reduce load time and visual delay
- reducing layout shift to improve reading and interaction stability
- reviewing render-blocking CSS that delayed meaningful content display
- improving asset caching behaviour to support repeat visits

These changes were made pragmatically, without attempting to eliminate all Lighthouse warnings or artificially inflate performance scores.

---

### Outcome of the Initial Analysis

The initial Lighthouse analysis served as a **baseline reference point**, guiding subsequent iterations rather than acting as a final measure of success.

Insights from this stage directly informed the v2 accessibility and performance refinements documented below, enabling:
- more robust form semantics
- clearer navigation and hierarchy
- improved contrast and readability
- better layout predictability across devices

This approach ensured that Lighthouse was used as an **evidence-based auditing tool**, supporting meaningful accessibility improvements rather than superficial optimisation.

The following results were achieve during the initial Lighthouse audit:

## User Reports :
[Home](/readme_docs/lighthouse/home.png)
[Shop All](/readme_docs/lighthouse/shop.png)
[Refillables](/readme_docs/lighthouse/refill.png)
[About](/readme_docs/lighthouse/about.png)
[Cart](/readme_docs/lighthouse/cart.png)
[Checkout](/readme_docs/lighthouse/checkout.png)
[Product](/readme_docs/lighthouse/prod_detail.png)
[Orders](/readme_docs/lighthouse/user_orders.png)

## Admin Reports:
[Dashboard](/readme_docs/lighthouse/admin_dash.png)
[Orders](/readme_docs/lighthouse/admin_order.png)
[Order Detail](/readme_docs/lighthouse/admin_order_det.png)
[Product](/readme_docs/lighthouse/admin_prod.png)
[Product Edit](/readme_docs/lighthouse/admin_prod_edit.png)
[Reviews](/readme_docs/lighthouse/admin_review.png)

---

## Summary of Key Improvements

- Reduced unused CSS by splitting global and page-specific stylesheets
- Introduced responsive images and modern formats (WebP) to reduce image payload
- Implemented cache-friendly static asset handling with hashed filenames
- Improved Largest Contentful Paint (LCP) by optimising hero imagery
- Addressed layout shift (CLS) by defining intrinsic image dimensions
- Reduced render-blocking resources where practical

---

## Image Optimisation

Images were identified as the **largest contributor to initial page weight**, particularly product images and homepage hero imagery.

To address this:

- All decorative and product imagery uses the **WebP** format where possible
- Homepage hero images use **responsive `srcset` definitions**, ensuring smaller images are delivered to smaller viewports
- Product images are lazy-loaded to avoid unnecessary network requests on initial page load
- Explicit `width` and `height` attributes are applied to images to prevent layout shift

Lighthouse continues to report potential savings for product images served from `/media/`. This is expected in a development environment. In a production deployment, these assets would be served via a CDN (e.g. Cloudinary or S3) with automated resizing, compression, and long-term caching.

---

## CSS & Render-Blocking Resources

Initial Lighthouse audits highlighted unused and render-blocking CSS. These issues were mitigated by:

- Splitting CSS into **global styles** (base layout, navigation, shared components) and **page-specific styles**
- Loading page-specific stylesheets only on the pages that require them using Django template blocks
- Reducing duplication by leveraging Bootstrap utility classes where appropriate

Bootstrap remains a render-blocking dependency; however, this is a deliberate trade-off to ensure consistent layout behaviour and rapid UI development. Remaining blocking time is minimal and acceptable within the scope of the project.

---

## Caching Strategy

Static assets (CSS, JavaScript, images) are served using **hashed filenames**, enabling long-term browser caching without the risk of stale assets.

Lighthouse flags cache lifetime warnings for media uploads in development. To reflect production behaviour more accurately:

- A development-only middleware applies `Cache-Control` headers to media files
- In production, media assets would be served via a CDN with aggressive caching policies

This demonstrates an understanding of both development constraints and production-grade performance strategies.

---

## JavaScript & Third-Party Scripts

JavaScript usage is intentionally minimal and focused:

- Custom JavaScript is limited to essential interactive features (cart updates, UI toasts)
- Third-party scripts (Stripe, Font Awesome) are loaded only where required

Some unused JavaScript is reported by Lighthouse due to third-party libraries. This is expected and acceptable given their scope and functionality.

---

## Performance Trade-offs & Intentional Decisions

Not all Lighthouse warnings were eliminated intentionally. Examples include:

- Retaining Font Awesome for design consistency despite font loading costs
- Loading Bootstrap CSS globally to maintain predictable layouts
- Approximating production-level media caching behaviour during development

These decisions prioritise **maintainability, clarity, and user experience** over maximising synthetic performance scores.

---

## Accessibility & Performance Audit (Lighthouse)

Lighthouse audits were conducted primarily as an **accessibility assessment tool**, with performance metrics used as a secondary indicator of overall user experience quality.

While Lighthouse provides synthetic performance scores, the primary objective of this audit was to evaluate and improve:
- semantic HTML structure
- form labelling and control relationships
- colour contrast and readability
- predictable layout behaviour
- keyboard and assistive technology compatibility

Where possible, accessibility improvements were implemented alongside **practical performance enhancements**, recognising that many accessibility fixes (such as layout stability and image optimisation) also contribute positively to perceived performance.

---

## User-Facing Accessibility Audits (v2)

The following Lighthouse reports represent the **final audit state (v2)** after accessibility-focused refinements were applied across the storefront.

- **Home Page**  
  [/readme_docs/lighthouse/home_v2.png](readme_docs/lighthouse/home_v2.png)

- **Shop – All Products**  
  [/readme_docs/lighthouse/shop_v2.png](readme_docs/lighthouse/shop_v2.png)

- **Winter Isles Collection**  
  [/readme_docs/lighthouse/winter_isles.png](readme_docs/lighthouse/winter_isles.png)

  > *Audit correction:*  
  > During accessibility review, it was identified that the **Winter Isles** category was missing from the main shop navigation in earlier iterations.  
  > This was corrected in v2 and positioned alongside **Refillables**, ensuring consistent navigation structure and equal access to all product categories.

Key accessibility considerations addressed in these views include:
- improved colour contrast for product metadata text
- stabilised layouts to prevent content shift during load
- clearer navigation hierarchy and category discoverability
- consistent focus behaviour across interactive elements

---

## Admin Accessibility Audits (v2)

Administrative interfaces were also audited to ensure that internal tooling remains **accessible, readable, and navigable**, particularly for users relying on assistive technologies.

- **Admin Dashboard**  
  [/readme_docs/lighthouse/admin_dash_v2.png](readme_docs/lighthouse/admin_dash_v2.png)

- **Admin – Orders List**  
  [/readme_docs/lighthouse/admin_order_v2.png](readme_docs/lighthouse/admin_order_v2.png)

- **Admin – Products List**  
  [/readme_docs/lighthouse/admin_prod_v2.png](readme_docs/lighthouse/admin_prod_v2.png)

- **Admin – Product Edit Page**  
  [/readme_docs/lighthouse/admin_prod_edit_v2.png](readme_docs/lighthouse/admin_prod_edit_v2.png)

- **Admin – Reviews**  
  [/readme_docs/lighthouse/admin_review_v2.png](readme_docs/lighthouse/admin_review_v2.png)

Accessibility improvements applied to admin views include:
- explicit `<label for>` associations for all form inputs
- removal of prohibited ARIA attributes and correction of ARIA roles
- improved contrast for buttons, cards, and metadata text
- predictable button layout across desktop, tablet, and mobile breakpoints
- reduced cognitive load through clearer section grouping and headings

These changes ensure that administrative workflows are usable with screen readers and keyboard navigation, while also improving clarity for all users.

---

## Accessibility Improvements Identified & Implemented

Across both user-facing and admin areas, the Lighthouse audit highlighted several opportunities for improved accessibility. These were addressed as follows:

### Semantic Structure & Form Labelling
- All form controls were explicitly associated with labels
- Visually-hidden labels were used where a visual label would be redundant, ensuring screen reader compatibility without visual clutter
- Form grouping was clarified using section headings and consistent layout patterns

### Colour Contrast & Readability
- Low-contrast metadata and muted text styles were adjusted to meet WCAG contrast requirements
- Outline-only buttons with insufficient contrast were replaced or reinforced with solid variants where appropriate
- Text opacity was avoided in favour of contrast-safe colour values

### Layout Stability & Predictability
- Intrinsic dimensions (`width` and `height`) were applied to images to prevent layout shift
- Section spacing was standardised to avoid visual crowding
- Button groups were explicitly managed at mobile, tablet, and desktop breakpoints to prevent wrapping or unpredictable reflow

### Navigation & Discoverability
- Missing navigation elements (e.g. Winter Isles category) were restored and aligned with existing category structures
- Admin navigation and action buttons were reorganised to maintain consistent placement across viewports

---

## Relationship Between Accessibility & Performance

While accessibility was the primary audit goal, several accessibility-driven changes also improved perceived performance:

- Layout stability improvements reduced cumulative layout shift (CLS)
- Image resizing and compression reduced visual loading delays
- Reduced render-blocking behaviour improved time-to-interaction
- Clearer visual hierarchy reduced cognitive load during page use

These changes demonstrate an understanding that **accessible design and good performance are closely linked**, particularly in real-world usage scenarios.

---

## Heading Hierarchy & Lighthouse Considerations

During development, heading levels were chosen to balance **semantic HTML structure**, **visual design**, and **automated audit feedback**.

In some components (such as product cards within grid layouts), using lower-level heading elements (e.g. `h5`) is visually appropriate but can trigger Lighthouse or accessibility warnings if the surrounding document hierarchy does not follow a strict, linear heading order.

To address this:
- Higher-level page sections use consistent `h1`–`h3` headings to define the overall document structure.
- Product card titles use smaller heading levels or Bootstrap heading utility classes (e.g. `.h5`, `.h6`) to maintain visual hierarchy without disrupting the page’s semantic outline.
- Where appropriate, Bootstrap’s heading utility classes are used to control appearance while preserving meaningful heading structure.

This approach ensures:
- Clear visual hierarchy for users
- A logical document structure for assistive technologies
- Minimal false-positive warnings from automated tools such as Lighthouse

Any remaining Lighthouse warnings related to heading order were reviewed and deemed acceptable trade-offs in favour of consistent UX and maintainable component design.

---

## Final Accessibility Summary

The final Lighthouse audits demonstrate a **clear and deliberate approach to accessibility** across the application.

Accessibility improvements were not treated as isolated fixes, but instead integrated into:
- layout structure
- form design
- navigation hierarchy
- visual contrast decisions
- responsive behaviour across devices

The resulting interface is:
- usable with assistive technologies
- predictable and readable across screen sizes
- compliant with key WCAG principles
- improved through iterative, evidence-based refinement

Within the scope of this project, the application demonstrates a **strong accessibility foundation**, with Lighthouse audits used appropriately as a diagnostic and validation tool rather than as a target for superficial scoring optimisation.