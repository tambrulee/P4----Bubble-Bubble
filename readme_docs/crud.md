## CRUD Functionality

CRUD (Create, Read, Update, Delete) operations are implemented throughout the project to manage data across key features such as products, user accounts, orders, reviews, and shipping addresses.

The application uses Django’s Model–View–Template (MVT) architecture to ensure CRUD operations are handled securely, consistently, and in line with best practices.

---

## Create

Create operations allow users and staff to add new data to the system.

Examples include:
- **User accounts** created via the registration form
- **Shipping addresses** added during checkout or account management
- **Orders** created when a checkout is successfully completed
- **Product reviews** submitted by authenticated users
- **Products** created by staff users via the custom owner dashboard

Creation is handled using Django Forms and ModelForms to ensure all submitted data is validated server-side before being saved to the database.

---

## Read

Read operations are used extensively across the project to retrieve and display data.

Examples include:
- Viewing product listings and product detail pages
- Displaying cart contents and order summaries
- Showing user order history within account pages
- Displaying reviews associated with individual products
- Allowing staff users to view products and orders in the owner dashboard

Read operations are performed using Django ORM queries and rendered using Django templates to maintain a clear separation between logic and presentation.

---

## Update

Update functionality allows existing records to be modified safely.

Examples include:
- Updating item quantities within the shopping cart
- Editing shipping address details
- Marking an address as the default
- Updating product details (price, description, availability) via the owner dashboard
- Updating order status by staff users

Update operations are restricted where appropriate using authentication and permission checks, ensuring that users can only modify their own data and that administrative actions are limited to staff users.

---

## Delete

Delete operations allow data to be removed where appropriate, with safeguards in place to prevent accidental or unauthorised deletion.

Examples include:
- Removing items from the shopping cart
- Deleting saved shipping addresses
- Removing or moderating product reviews
- Deleting products via the owner dashboard (staff-only)

Where deletion is destructive, actions are protected by permission checks and confirmation flows to reduce the risk of unintended data loss.

---

## Access Control & Security

CRUD operations are protected using:
- Django’s authentication system
- Permission checks such as `login_required` and `user.is_staff`
- CSRF protection on all POST requests

This ensures that:
- Public users can only read publicly available data
- Authenticated users can manage their own data
- Staff users have elevated permissions for administrative CRUD actions

---

## Summary

CRUD functionality is implemented consistently across the project using Django’s ORM, forms, and authentication system.  
This approach ensures that data operations are secure, maintainable, and aligned with real-world application requirements.
