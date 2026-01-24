## Features

The BubbleBubble (Moon & Moss) platform provides a full end-to-end e-commerce experience for both customers and shop administrators. Features were designed to support clear user journeys, reduce friction during checkout, and provide practical tools for managing products, orders, and reviews.

---

## Customer-Facing Features

### Home Page & Brand Story
[Home page layout and navigation](/readme_docs/features/home.png)  
[About the brand section](/readme_docs/features/home_about.png)  
[Best-selling products showcase](/readme_docs/features/home_bestsellers.png)  
[Homepage customer review highlights](/readme_docs/features/home_review.png)

The home page introduces the Moon & Moss brand through a clean, visually led layout. Seasonal collections, best-selling products, and customer reviews are highlighted to build trust and guide users towards popular items.

---

### Product Browsing & Discovery
[Shop all products page with filters](/readme_docs/features/shop_all.png)  
[Winter Isles seasonal collection](/readme_docs/features/winter_isles.png)  
[Refillable products collection](/readme_docs/features/refillables.png)

Users can browse the full catalogue or explore curated collections. Filtering and sorting options support both casual browsing and intentional purchasing.

---

### Product Detail Pages
[Individual product detail page](/readme_docs/features/product_page.png)

Each product page displays detailed information including pricing, weight, scent description, stock status, and verified customer reviews.

---

### Shopping Cart & Mini Cart
[Full shopping cart page](/readme_docs/features/cart.png)  
[Mini cart with quantity controls](/readme_docs/features/mini_cart.png)  
[Toast notification when adding items to cart](/readme_docs/features/toast_add_to_cart.png)

The mini cart allows users to adjust quantities and proceed to checkout without leaving their current page, while toast notifications provide immediate feedback.

---

## Checkout & Payments

### Checkout Flow
[Checkout page layout](/readme_docs/features/checkout.png)  
[Checkout form validation and error handling](/readme_docs/features/checkout_validation.png)
[Validation signals for checkout form](/readme_docs/features/toast_saved_addresses.png)

The checkout process supports both guest checkout and logged-in users, with inline validation to reduce errors and abandonment.

---

### Stripe Payment Integration
[Stripe payment processing](/readme_docs/features/stripe.png)

Payments are handled securely via Stripe, ensuring sensitive payment details are never stored on the application server.

---

### Order Confirmation & Success
[Order confirmation summary](/readme_docs/features/order_confirm.png)  
[Successful payment confirmation screen](/readme_docs/features/payment_successful.png)

Clear confirmation screens reassure users that their order has been placed successfully.

---

## User Accounts & Order History

### Account Creation & Login
[User account creation form](/readme_docs/features/create_account_user.png)  
[User account creation confirmation](/readme_docs/features/create_acc_user2.png)  
[User login page](/readme_docs/features/user_login.png)

Account creation includes password validation and clear feedback to support secure registration.

---

### User Panel & Address Book
[User account dropdown and navigation](/readme_docs/features/user_panel.png)  
[Saved address book management](/readme_docs/features/address_book.png)
[Toast notification when user deletes address](/readme_docs/features/toast_address_delete.png)

Registered users can manage delivery addresses and access their order history through a dedicated account panel.

---

### User Order History & Reviews
[User order history page](/readme_docs/features/user_orders.png)

Users can review previous orders and leave verified product reviews once orders are marked as paid.

---

## Reviews & Community Trust

### Product Reviews
[Customer reviews displayed on product page](/readme_docs/features/home_review.png)

Verified reviews provide social proof and help build trust with new customers.

---

### Review Moderation (Admin)
[Admin reviews management page](/readme_docs/features/reviews_admin.png)  
[Admin review approval and moderation](/readme_docs/features/review_approval_admin.png)  
[Toast notification when a review is added](/readme_docs/features/toast_review_added.png)

Admins can approve, hide, reply to, and filter reviews to maintain quality and engagement.

---

## Admin & Shop Management Features

### Admin Login & Dashboard
[Admin login page](/readme_docs/features/admin_login.png)  
[Owner dashboard overview](/readme_docs/features/dashboard.png)

A custom dashboard provides a high-level overview of store activity, including products, orders, and low-stock alerts.

---

### Product Management
[Admin product list and filters](/readme_docs/features/products_admin.png)  
[Admin product edit form](/readme_docs/features/edit_product_admin.png)  
[Product image management interface](/readme_docs/features/image_manager_admin.png)  
[Toast notification when deleting a product](/readme_docs/features/toast_product_delete.png)
[Error message when owner attempts to delete product that is in the cart or has been ordered - archives instead](/readme_docs/features/product_delete_error.png)

Admins can efficiently manage product listings using bulk actions, filtering, and image management tools.

---

### Order Management
[Admin orders management page](/readme_docs/features/orders_admin.png)

Orders are grouped by fulfilment status, allowing admins to track and update order progress efficiently.

---

## UI, Feedback & Accessibility

### Visual Feedback & Notifications
[Toast feedback for cart updates](/readme_docs/features/toast_add_to_cart.png)  
[Toast feedback for product deletion](/readme_docs/features/toast_product_delete.png)  
[Toast feedback for review submission](/readme_docs/features/toast_review_added.png)

Consistent visual feedback reinforces user actions and improves perceived responsiveness.

---

### Footer & Site Structure
[Site footer layout](/readme_docs/features/footer.png)

The footer provides consistent navigation and reinforces brand identity across the site.

---

## Summary

The feature set reflects a complete, production-ready e-commerce platform with a clear separation between customer and admin functionality. UX decisions prioritise clarity, trust, and efficiency, while admin tools focus on practical day-to-day store management.
