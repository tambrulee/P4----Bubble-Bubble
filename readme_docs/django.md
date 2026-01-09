# Project Structure & Architecture

## Project Overview

This project follows a **conventional Django architecture**, with a single project container and multiple modular applications, each responsible for a distinct area of functionality.

The project was originally named **BubbleBubble** and later rebranded to **Moon & Moss**.  
The internal project folder name was intentionally left unchanged to avoid introducing unnecessary risk or breaking existing imports, settings, or deployment configuration.

The main Django project folder containing `settings.py` is located at:


The application is composed of **six Django apps**, each designed with a clear separation of concerns.

---

## Applications Overview

### `accounts`
Handles **user authentication and account management**.

This app is responsible for:
- User registration and login
- User logout
- Account-related views such as order history
- Differentiation between regular users and staff/admin users

The app integrates with Django’s built-in authentication system while providing custom templates and flows tailored to the site’s UX.

---

### `catalog`
Manages the **product catalogue and storefront browsing experience**.

This app includes:
- Product listings
- Product detail pages
- Category-based browsing
- Display logic for pricing, availability, and product metadata

`catalog` acts as the public-facing core of the site, allowing users to explore products before adding them to their cart.

---

### `cart`
Handles **temporary shopping cart functionality** prior to checkout.

Key responsibilities include:
- Adding and removing items from the cart
- Updating quantities
- Persisting cart data using session storage
- Displaying cart contents and totals

This app is deliberately kept lightweight and independent of payment logic, allowing the cart to function without requiring user authentication.

---

### `checkout`
Responsible for the **order processing and payment workflow**.

This app manages:
- Checkout forms and validation
- Order creation and persistence
- Integration with Stripe for secure payments
- Handling success and cancellation flows

The checkout process bridges the gap between the cart and completed orders, ensuring transactional integrity.

---

### `owner`
Provides a **custom administrative interface** for staff users.

This app includes:
- Owner/staff dashboards
- Product management (CRUD operations)
- Order management and fulfilment views
- Restricted access based on staff permissions

The `owner` app exists alongside Django’s admin panel, offering a more user-friendly, brand-aligned management experience tailored specifically to the business owner’s needs.

---

### `reviews`
Manages **user-generated product reviews**.

Responsibilities include:
- Submitting reviews for products
- Rating functionality
- Displaying reviews on product detail pages
- Ensuring only authenticated users can leave reviews

This app enhances user engagement and provides social proof within the storefront.

---

## Architectural Rationale

Each application is designed to:
- Encapsulate a single area of responsibility
- Reduce coupling between unrelated features
- Improve maintainability and readability
- Allow future expansion without impacting existing functionality

This modular approach follows Django best practices and supports scalability as the project evolves.

---

## Why Django?

Django was chosen as the framework for this project due to its **batteries-included philosophy**, strong security features, and suitability for **data-driven web applications** such as e-commerce platforms.

Key reasons for choosing Django include:

- **Rapid development**  
  Django provides built-in functionality for authentication, routing, templating, forms, and administration, allowing development to focus on business logic rather than boilerplate code.

- **Security by default**  
  Django includes protection against common web vulnerabilities such as CSRF, XSS, SQL injection, and clickjacking, which is particularly important for applications handling user accounts and payments.

- **Clear separation of concerns**  
  Django’s app-based structure encourages modular design, making it easier to maintain, test, and extend the codebase as the project grows.

- **ORM and database abstraction**  
  Django’s Object-Relational Mapper allows database interactions to be handled using Python code rather than raw SQL, improving readability and reducing the likelihood of errors.

- **Scalability and extensibility**  
  The framework supports scaling from small projects to production-grade applications and integrates well with third-party services such as Stripe for payments.

- **Industry relevance**  
  Django is widely used in production environments and provides transferable skills applicable to real-world software development.

Overall, Django was selected because it provides a robust, secure, and maintainable foundation well suited to the functional and architectural requirements of this project.
