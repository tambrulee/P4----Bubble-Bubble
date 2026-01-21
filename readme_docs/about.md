
# About

## Executive Summary

**Bubble Bubble (Moon & Moss)** is a full-stack Django e-commerce application showcasing a small online shop for handmade, organic soap products. 

The project focuses on clean UX design, secure user authentication, and robust backend functionality, delivering a calm, accessible shopping experience.

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
- Gentle copywriting
- Emphasis on ritual, comfort, and craftsmanship

The visual identity supports trust and reflects the handcrafted, small-batch nature of the products.

As part of my research for the project, I used two real-life soap ecommerce websites for inspiration to develop branding, UX and user stories:

### [Little Soap Company](https://www.littlesoapcompany.co.uk/)
- Branding - Organic, ethical, sustainable
- Navigation - Mobile Responsive (Burger toggle in mobile view), shop logo, links and account/cart management
- Homepage & Product/Collection UX

### [Highland Soap Co.](https://www.highlandsoaps.com/)
- Homepage & Product/Collection UX
- Customer user stories
- Mini cart (side draw)
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

The user experience (UX) design of this project was developed iteratively and informed by both established UX principles and structured task planning using **GitHub Issues and Milestones**.

Rather than treating UX as a single design phase, usability improvements were planned, implemented, reviewed, and refined throughout development.

The core UX principles guiding the project are:

- **Clarity**  
  Clear navigation, readable layouts, and obvious calls to action ensure users understand what to do at each stage of their journey.

- **Simplicity**  
  Interfaces are intentionally minimal, reducing cognitive load and avoiding unnecessary steps, particularly during shopping and checkout flows.

- **Consistency**  
  Reusable components, predictable layouts, and consistent styling help users build familiarity and confidence as they move through the site.

- **Feedback**  
  Visual confirmation is provided for key user actions (such as adding items to the cart, updating quantities, or completing checkout), reducing uncertainty and improving trust.

- **Responsiveness**  
  All pages are designed to function effectively across mobile, tablet, and desktop devices, with layouts adapting to screen size and interaction patterns.

User journeys are kept short and intentional, particularly around **browsing, cart interaction, and checkout**, where unnecessary friction can lead to abandonment.

---

## UX-Driven Development Using GitHub Issues & Milestones

[GitHub Issues](/readme_docs/milestone-2.png) and [Milestones](/readme_docs/milestones.png) were used as a **UX planning and decision-making tool**, not just a task tracker. Each milestone represented a distinct UX focus area or phase of development, allowing features to be grouped around user needs rather than technical components alone.

Issues were written from a **user-centric perspective**, often framed around usability improvements, clarity, or interaction behaviour. This ensured UX considerations were addressed alongside functional development.

### Milestone-led UX Iteration

Key UX-focused milestones included:

- **Create Shop Front**  
  Focused on establishing a clear visual hierarchy, intuitive navigation, and a welcoming storefront experience.

- **Shopping Cart** and **Shopping UX**  
  Concentrated on reducing friction during product selection, cart updates, and quantity changes. Issues addressed clarity of pricing, feedback on actions, and predictable cart behaviour.

- **User Accounts, Orders and Checkout Functions**  
  Ensured critical flows such as account creation, order review, and checkout were straightforward and easy to follow, with clear validation and feedback.

- **Enhanced UX** and **Last Minute Touch Ups**  
  Dedicated specifically to refinement: spacing, form readability, error messaging, visual polish, and small interaction improvements identified during testing and review.

- **Owner Dashboard UX**  
  Focused on usability for staff users, ensuring that product and order management actions were clear, efficient, and distinct from the customer-facing experience.

Each milestone was closed only once all related UX issues were resolved and reviewed, reinforcing a sense of completion before moving on to the next phase.

---

## UX Validation Through Testing

UX decisions were validated through a dedicated **Testing** milestone, which included:

- Manual testing of key user journeys
- Verification of responsive layouts across screen sizes
- Review of form validation messages and error handling
- Ensuring consistent feedback for user actions

Findings from testing directly informed follow-up UX issues, particularly in later milestones such as **Enhanced UX** and **Last Minute Touch Ups**, reinforcing an iterative design loop.

---

## Summary

By structuring development around GitHub Issues and Milestones, UX design became a **continuous, intentional process** rather than a one-off design exercise.

This approach ensured that:
- UX improvements were planned and tracked explicitly
- Features were developed with real user journeys in mind
- Refinements were prioritised based on usability rather than convenience

The result is a cohesive, user-focused interface that evolved alongside the technical implementation of the project.


---


## Original UX Concept & Wireframe Design

[View or download (recommended) wireframes pdf](/readme_docs/wireframes.pdf)

The initial UX design for this project was developed using low-fidelity wireframes to map out **end-to-end user journeys** before any visual styling or technical implementation took place.

The wireframes focus on functionality, flow, and decision points rather than aesthetics, allowing early validation of how users would interact with the application across key scenarios.

---

## Core Design Goals

The original UX concept was guided by the following goals:

- Provide a **clear and intuitive shopping journey**
- Support both **guest and registered users**
- Minimise friction during checkout
- Separate **customer-facing** and **admin-facing** experiences
- Design reusable flows that could scale with additional features

These goals informed the structure and sequencing of screens shown in the wireframes.

---

## Customer Journey Design

### Browsing & Product Discovery

The wireframes begin with a **Home / Catalogue view**, presenting products in a simple list format with:
- Product name
- Price
- “Add to basket” call-to-action

A filter/search function is explicitly noted at the top of the catalogue view, indicating early consideration of **product discoverability** and scalability as the catalogue grows.

From the catalogue, users can:
- Add products directly to the basket, or
- Navigate to a dedicated **Product Page** for more detailed information

This supports both quick purchasing and more considered browsing behaviour.

---

### Shopping Cart as a Decision Hub

The **Shopping Cart** wireframe acts as a central decision point in the journey.

Key UX decisions visible in the wireframes include:
- Clear line-item breakdown (product name, quantity, price)
- A visible total amount
- Two explicit next-step options:
  - **Checkout as guest**
  - **Login**

Presenting both options at the cart stage avoids forcing authentication too early, reducing friction and supporting faster conversion for new users :contentReference[oaicite:3]{index=3}.

---

### Guest vs Registered Checkout Flow

The wireframes intentionally split the checkout into two paths:

#### Guest Checkout
- Delivery address form
- Order summary
- Checkout basket confirmation

#### Registered User Checkout
- Login step
- Delivery address form
- Checkout basket confirmation

Both paths converge on the same essential steps, ensuring consistency while still supporting different user needs. This early decision reflects a deliberate balance between **conversion optimisation** and **account creation**.

---

### Authentication & Account Creation

Separate wireframes exist for:
- Login
- Forgotten login
- Sign-up

This separation demonstrates early awareness of **error recovery** and alternative paths, rather than assuming a single “happy path” user journey :contentReference[oaicite:4]{index=4}.

---

### Post-Purchase Experience

For authenticated users, the wireframes include an **Order History** view showing:
- Order number
- Date
- Total amount

This reinforces transparency and trust, allowing users to review past purchases and order status.

A **Reviews** section is also included, showing product-level reviews linked to orders, indicating early consideration of user-generated content and post-purchase engagement.

---

## Admin / Shop Manager UX Concept

The wireframes clearly distinguish between **End User** and **Shop Manager / Admin** experiences.

### Product Management
The admin console includes:
- Product creation and editing
- Drag-and-drop image upload (not in final product - replaced with simple upload button)
- Price and stock level management
- Product description fields

This demonstrates a focus on **usability for non-technical users**, rather than relying solely on Django’s default admin interface.

---

### Order Management

An **Order Manager** view is included to:
- View incoming orders
- Track order status (new, delivered, etc.)
- Review order contents

Notably, the wireframes include a comment to “leave order manager & stock level feature to last”, indicating conscious **feature prioritisation** and phased development planning rather than attempting to build everything at once.

---

## Reflections on the Original Design

The wireframes demonstrate that the original concept:

- Prioritised **user flow over visual polish**
- Identified critical decision points early (guest vs registered checkout)
- Anticipated future needs such as reviews, filtering, and stock control
- Distinguished clearly between customer and admin UX

Many of these original ideas directly informed later development milestones, particularly those focused on **Shopping UX**, **Owner Dashboard UX**, and **Enhanced UX**.


---

## Database

[Model Documentation](/readme_docs/models.md)
[Database Schema](/readme_docs/dbschema.png)

The project uses a relational database managed through Django’s ORM.

Core models include:
- **User** – authentication and user accounts
- **Product** – product details, pricing, stock, and availability
- **Order** – completed customer orders
- **OrderLineItem** – individual products within each order

Model relationships enforce data integrity and allow for future scalability, such as adding reviews, wishlists, or extended product categorisation.
