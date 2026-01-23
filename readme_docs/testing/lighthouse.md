## Performance & Lighthouse Optimisation

Performance was evaluated using **Google Lighthouse** in Chrome DevTools, with a focus on real-world user experience rather than chasing artificial 100/100 scores. The application achieves a **strong overall Performance score (mid-to-high 70s and above)**, with clear evidence of deliberate optimisation across images, CSS delivery, caching, and render behaviour.

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

## Conclusion

The application demonstrates **strong performance fundamentals** and a clear understanding of Lighthouse metrics, browser rendering behaviour, and real-world optimisation techniques. Remaining Lighthouse suggestions primarily relate to production-level infrastructure (CDNs, advanced media pipelines) rather than application-level inefficiencies.

Within the scope of this project, the achieved performance score represents a well-optimised, scalable foundation suitable for further enhancement in a production environment.
