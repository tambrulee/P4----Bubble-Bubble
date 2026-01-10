# User Stories & Feature Implementation

## Project Overview

This document outlines the core user stories that drove the development of the Bubble Bubble / Moon & Moss e-commerce platform and explains how each requirement was implemented.  
The project follows a user-centred design approach aligned with standard e-commerce expectations and Django best practices.

---

## Epic 1: Browsing & Discovering Products

### User Story 1.1  
**As a shopper, I want to browse products by category so that I can easily find items I am interested in.**

**Implementation**
- Products are organised into categories using a dedicated Category model.
- Category navigation is displayed in the main site navigation.
- Category views filter products dynamically based on the selected category.
- Clean URLs and Django views ensure intuitive navigation.

---

### User Story 1.2  
**As a shopper, I want to view detailed product information so that I can decide whether to purchase an item.**

**Implementation**
- Each product has a dedicated product detail page.
- Pages display product name, description, price, image(s), and availability.
- Template inheritance ensures consistent layout across product pages.
- Conditional logic prevents unavailable products from being added to cart.

---

## Epic 2: Shopping Cart Functionality

### User Story 2.1  
**As a shopper, I want to add products to a shopping cart so that I can purchase multiple items at once.**

**Implementation**
- Cart functionality is session-based to support both guest and logged-in users.
- Products can be added to the cart from product listing and detail pages.
- Quantity handling is managed via Django views and context processors.
- Toast notifications provide immediate feedback when items are added.

---

### User Story 2.2  
**As a shopper, I want to view and update my cart so that I can adjust my order before checkout.**

**Implementation**
- A dedicated cart page displays all selected items with quantities and totals.
- Quantity inputs allow users to update or remove items.
- Cart totals update dynamically on submission.
- Defensive validation prevents invalid quantities.

---

## Epic 3: Checkout & Payments

### User Story 3.1  
**As a shopper, I want a secure checkout process so that I can safely complete my purchase.**

**Implementation**
- A multi-step checkout flow collects delivery and contact information.
- Django forms handle validation and error messaging.
- Order data is stored in a dedicated Order model.
- Stripe is integrated to securely process payments.

---

### User Story 3.2  
**As a shopper, I want to receive confirmation after checkout so that I know my order was successful.**

**Implementation**
- Successful payments redirect users to a confirmation page.
- Order summary details are displayed after checkout.
- Confirmation emails are sent using Django’s email framework.
- Webhooks ensure payment status accuracy.

---

## Epic 4: User Accounts

### User Story 4.1  
**As a user, I want to create an account and log in so that I can view my order history.**

**Implementation**
- Django’s authentication system is used for registration and login.
- Secure password handling is provided out of the box.
- Logged-in users can access a “My Orders” area.
- Authentication state is reflected in the navigation UI.

---

### User Story 4.2  
**As a user, I want to log out securely so that my account remains protected.**

**Implementation**
- Django’s built-in logout view is used.
- Logout redirects users to the login page.
- CSRF protection is enforced on all authentication actions.

---

## Epic 5: Admin & Owner Management

### User Story 5.1  
**As a site owner, I want to manage products so that I can add, edit, or remove items.**

**Implementation**
- Custom owner dashboard built on top of Django admin principles.
- Product CRUD functionality restricted to staff users.
- Forms allow controlled editing of product data.
- Staff-only routes are protected via permissions and decorators.

---

### User Story 5.2  
**As a site owner, I want to view orders so that I can manage fulfilment.**

**Implementation**
- Owner dashboard includes an order management view.
- Orders are displayed with status, totals, and customer details.
- Access is restricted to authenticated staff users.
- Clear separation between customer and owner interfaces.

---

## Epic 6: UX, Accessibility & Responsiveness

### User Story 6.1  
**As a user, I want the site to work well on mobile so that I can shop on any device.**

**Implementation**
- Responsive layout built with Bootstrap 5.
- Mobile-first navigation including a collapsible menu.
- Icons and touch-friendly controls improve usability.
- CSS optimised to reduce visual clutter on smaller screens.

---

### User Story 6.2  
**As a user, I want clear feedback when I take actions so that I understand what is happening.**

**Implementation**
- Toast messages confirm cart actions and form submissions.
- Inline validation errors guide users during checkout.
- Disabled states prevent invalid actions.
- Consistent visual language across the site.

---

## Epic 7: Code Quality, Testing & Deployment

### User Story 7.1  
**As a developer, I want the codebase to be maintainable so that it can be extended in the future.**

**Implementation**
- Code follows PEP8 standards and Django best practices.
- Flake8 and ESLint used to identify and resolve issues.
- Reusable templates and components reduce duplication.
- Clear separation of concerns across apps.

---

### User Story 7.2  
**As a developer, I want the project deployed online so that it can be accessed publicly.**

**Implementation**
- Deployed to Heroku with environment variables for security.
- Static and media files configured correctly.
- Production settings separated from development settings.
- Deployment logs monitored and errors resolved iteratively.

---

## Conclusion

The project was driven by real-world e-commerce user stories covering browsing, purchasing, account management, and administration.  
Each feature was implemented with usability, security, and scalability in mind, resulting in a functional and extensible platform.

