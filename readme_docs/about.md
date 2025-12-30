
# About

## Executive Summary

**Bubble Bubble (Moon & Moss)** is a full-stack Django e-commerce application showcasing a small online shop for handmade, organic soap products.  
The project focuses on clean UX design, secure user authentication, and robust backend functionality, delivering a calm, accessible shopping experience while meeting all Code Institute Full Stack Project assessment criteria.

---

## Project Description: Purpose & Value

Bubble Bubble is designed to demonstrate the development of a production-style e-commerce platform using Django.  
The application allows users to browse products, manage a shopping cart, and complete secure online purchases, while providing administrators with tools to manage products and orders.

**Value provided:**
- A frictionless customer journey from browsing to checkout
- Secure handling of user accounts and payments
- Clear separation of customer-facing and admin functionality
- Scalable architecture suitable for future expansion

---

## Branding

The **Moon & Moss** brand is intentionally calm, minimal, and nature-inspired.

Branding principles include:
- Soft, organic colour palettes
- Clean typography and generous white space
- Gentle, non-aggressive copywriting
- Emphasis on ritual, comfort, and craftsmanship

The visual identity supports trust and reflects the handcrafted, small-batch nature of the products.

---

## Target Market

The target audience includes:
- Adults interested in natural and organic skincare
- Environmentally conscious consumers
- Customers who value handmade and small-batch goods
- Users seeking a simple, distraction-free online shopping experience

The site is designed to be accessible to users with varying levels of technical confidence.

---

## Users & Permissions (Log In & Registration)

The application supports role-based access using Django’s authentication system.

### Anonymous Users
- View products and site content
- Browse the shop
- Add items to the cart
- Register for an account

### Registered Users
- Log in and log out securely
- Complete checkout and place orders
- Receive order confirmation
- Save personal details for faster checkout

### Staff / Admin Users
- Access the Django admin interface
- Create, edit, and deactivate products
- View and manage customer orders
- Update order statuses (e.g. paid, dispatched, delivered)

Admin-only functionality is protected using Django permissions and decorators.

---

## Dependencies

### Backend
- Python
- Django
- PostgreSQL (production)
- SQLite (development)

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Tools & Services
- Stripe (payment processing)
- Django Allauth (authentication)
- Gunicorn (production server)
- Whitenoise (static files)
- Heroku (deployment)

All dependencies are documented in `requirements.txt`.

---

## UX Design Principles

The UX design is guided by the following principles:

- **Clarity:** Clear navigation and readable layouts
- **Simplicity:** Minimal interface elements to reduce cognitive load
- **Consistency:** Reusable components and predictable interactions
- **Feedback:** Visual confirmation for user actions (e.g. cart updates, checkout completion)
- **Responsiveness:** Optimised for mobile, tablet, and desktop devices

User journeys are short and intentional, particularly around browsing and checkout flows.

---

## Wireframes

Wireframes were created during the planning stage to define:
- Page structure and layout
- Navigation hierarchy
- Core user journeys

Wireframes include:
- Homepage
- Product listing page
- Product detail page
- Cart
- Checkout
- Account pages

These wireframes informed layout decisions and ensured a consistent experience across the site.

---

## Database

The project uses a relational database managed through Django’s ORM.

Core models include:
- **User** – authentication and user accounts
- **Product** – product details, pricing, stock, and availability
- **Order** – completed customer orders
- **OrderLineItem** – individual products within each order

Model relationships enforce data integrity and allow for future scalability, such as adding reviews, wishlists, or extended product categorisation.
