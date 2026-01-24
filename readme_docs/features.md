## Features & User Stories

This section demonstrates how core user stories directly informed the design and implementation of features across the BubbleBubble (Moon & Moss) platform. Each feature is mapped to real user needs and supported by screenshots and implementation detail.

---

## Epic 1: Browsing & Discovering Products


### User Stories: Home Page & Brand Story
- **As a visitor, I want to understand the brand’s values quickly so I can decide whether I trust the products.**
- **As a visitor, I want to see best-selling products on the homepage so I can discover popular items easily.**
- **As a visitor, I want to see customer reviews on the homepage so I can feel confident purchasing.**
- **As a visitor, I want clear calls to action on the homepage so I know how to start shopping.**

### User Stories: Product Browsing & Discovery
- **As a shopper, I want to browse all products in one place so I can explore the full range.**
- **As a shopper, I want to browse curated collections so I can find products that suit a theme or season.**
- **As a shopper, I want to filter products so I can narrow down my choices efficiently.**
- **As a shopper, I want consistent product cards so I can compare items easily.**

### User Stories: Product Detail Pages
- **As a shopper, I want to see detailed product information so I can make an informed purchase decision.**
- **As a shopper, I want to see clear pricing and stock status so I know whether I can buy an item.**
- **As a shopper, I want to see reviews on product pages so I can assess product quality.**
- **As a shopper, I want to add products to my cart from the product page so I can proceed to purchase.**

### User Stories: Shopping Cart & Mini Cart
- **As a shopper, I want to add products to my cart without leaving the page so I can continue browsing.**
- **As a shopper, I want to view my cart contents at any time so I can review my selections.**
- **As a shopper, I want to update item quantities in my cart so I can adjust my order.**
- **As a shopper, I want visual confirmation when items are added to my cart so I know the action was successful.**

### Feature: Home Page & Brand Story
[Home page layout and navigation](/readme_docs/features/home.png)  
[About the brand section](/readme_docs/features/home_about.png)  
[Best-selling products showcase](/readme_docs/features/home_bestsellers.png)  
[Homepage customer review highlights](/readme_docs/features/home_review.png)

**How it was achieved**
- A visually led homepage introduces the brand and values immediately.
- Best sellers and reviews provide social proof and guide user decisions.
- Clear calls-to-action direct users into shopping flows.
- Template inheritance ensures consistency across all landing sections.

---

### Feature: Product Browsing & Collections
[Shop all products page with filters](/readme_docs/features/shop_all.png)  
[Winter Isles seasonal collection](/readme_docs/features/winter_isles.png)  
[Refillable products collection](/readme_docs/features/refillables.png)

**How it was achieved**
- Products are organised into collections and surfaced via dynamic views.
- Filtering and pagination improve usability as the catalogue scales.
- Clean URLs and query-based filtering support intuitive navigation.

---

### Feature: Product Detail Pages
[Individual product detail page](/readme_docs/features/product_page.png)

**How it was achieved**
- Each product has a dedicated detail view.
- Information hierarchy prioritises price, scent, weight, and stock status.
- Conditional logic prevents adding out-of-stock items to the cart.
- Verified reviews reinforce trust at the decision point.

---

## Epic 2: Shopping Cart & Checkout

### User Stories: Checkout Flow
- **As a shopper, I want a simple checkout process so I can complete my purchase quickly.**
- **As a shopper, I want to check out as a guest so I am not forced to create an account.**
- **As a shopper, I want clear validation messages so I can fix any errors before submitting the form.**
- **As a shopper, I want to review my order details before payment so I can confirm everything is correct.**

### User Stories: Stripe Payment Integration
- **As a shopper, I want my payment to be processed securely so I can trust the site with my details.**
- **As a shopper, I want to use a familiar payment provider so I feel confident completing checkout.**

### User Stories: Order Confirmation & Success
- **As a shopper, I want confirmation after payment so I know my order was successful.**
- **As a shopper, I want to see a summary of my order so I can confirm what I purchased.**

### Feature: Shopping Cart & Mini Cart
[Full shopping cart page](/readme_docs/features/cart.png)  
[Mini cart with quantity controls](/readme_docs/features/mini_cart.png)  
[Toast notification when adding items to cart](/readme_docs/features/toast_add_to_cart.png)

**How it was achieved**
- Session-based cart supports both guest and logged-in users.
- Mini cart enables quick adjustments without page reloads.
- Toast notifications provide immediate visual feedback.
- Server-side validation prevents invalid quantities.

---

### Feature: Checkout & Validation
[Checkout page layout](/readme_docs/features/checkout.png)  
[Checkout form validation and error handling](/readme_docs/features/checkout_validation.png)  
[Validation signals for checkout form](/readme_docs/features/toast_saved_addresses.png)

**How it was achieved**
- Django forms manage checkout validation and error messaging.
- Required fields are enforced server-side to prevent incomplete orders.
- Guest checkout and logged-in flows converge into a single process.

---

### Feature: Secure Payments & Confirmation
[Stripe payment processing](/readme_docs/features/stripe.png)  
[Order confirmation summary](/readme_docs/features/order_confirm.png)  
[Successful payment confirmation screen](/readme_docs/features/payment_successful.png)

**How it was achieved**
- Stripe handles secure payment processing.
- Orders are persisted using Order and OrderItem models.
- Confirmation screens and emails reassure users post-purchase.
- Webhooks ensure payment status integrity.

---

## Epic 3: User Accounts & Order History

### User Stories: Account Creation & Login
- **As a user, I want to create an account so I can save my details for future purchases.**
- **As a user, I want to log in securely so my account information is protected.**
- **As a user, I want clear feedback during registration so I know if my details are valid.**

### User Stories: User Panel & Address Book
- **As a user, I want to manage my delivery addresses so checkout is faster next time.**
- **As a user, I want to delete or update saved addresses so my information stays accurate.**
- **As a user, I want a central account panel so I can manage everything in one place.**

### User Stories: User Order History & Reviews
- **As a user, I want to view my past orders so I can track my purchases.**
- **As a user, I want to leave reviews for products I’ve purchased so I can share my experience.**
- **As a user, I want reviews to be linked to real orders so the system feels trustworthy.**

### Feature: Account Creation & Login
[User account creation form](/readme_docs/features/create_account_user.png)  
[User account creation confirmation](/readme_docs/features/create_acc_user2.png)  
[User login page](/readme_docs/features/user_login.png)

**How it was achieved**
- Email-based authentication using Django’s auth framework.
- Password validation and feedback improve security.
- Authentication state dynamically updates navigation.

---

### Feature: User Panel & Address Book
[User account dropdown and navigation](/readme_docs/features/user_panel.png)  
[Saved address book management](/readme_docs/features/address_book.png)  
[Toast notification when user deletes address](/readme_docs/features/toast_address_delete.png)

**How it was achieved**
- Users can manage multiple shipping addresses.
- Default address logic handled at model level.
- Toast feedback confirms address actions.

---

### Feature: Order History & Reviews
[User order history page](/readme_docs/features/user_orders.png)

**How it was achieved**
- Paid orders are linked to user accounts.
- Verified purchase logic restricts reviews to completed orders.
- Review submission is surfaced contextually after purchase.

---

## Epic 4: Reviews & Community Trust

### User Stories: Product Reviews
- **As a shopper, I want to read reviews so I can decide whether a product is right for me.**
- **As a shopper, I want to see verified reviews so I can trust the feedback.**

### User Stories: Review Moderation (Admin)
- **As a site owner, I want to approve reviews so inappropriate content is not published.**
- **As a site owner, I want to reply to reviews so I can engage with customers.**
- **As a site owner, I want to hide reviews if necessary so the brand remains professional.**

### Feature: Product Reviews
[Customer reviews displayed on product page](/readme_docs/features/home_review.png)

**How it was achieved**
- Reviews are tied to products and users.
- Verified purchase flag ensures authenticity.
- Reviews appear both on product pages and homepage highlights.

---

### Feature: Review Moderation (Admin)
[Admin reviews management page](/readme_docs/features/reviews_admin.png)  
[Admin review approval and moderation](/readme_docs/features/review_approval_admin.png)  
[Toast notification when a review is added](/readme_docs/features/toast_review_added.png)

**How it was achieved**
- Staff-only moderation interface.
- Ability to approve, hide, reply to, and filter reviews.
- Prevents inappropriate or spam content.

---

## Epic 5: Admin & Owner Management

### User Stories: Admin Login & Dashboard
- **As a site owner, I want a secure admin login so only authorised users can manage the store.**
- **As a site owner, I want a dashboard overview so I can see the state of the shop at a glance.**

### User Stories: Product Management
- **As a site owner, I want to add new products so I can expand my catalogue.**
- **As a site owner, I want to edit product details so information remains accurate.**
- **As a site owner, I want to archive products instead of deleting them so order history is preserved.**
- **As a site owner, I want to manage product images so listings look professional.**

### User Stories: Order Management
- **As a site owner, I want to view incoming orders so I can fulfil them efficiently.**
- **As a site owner, I want to update order statuses so I can track fulfilment progress.**
- **As a site owner, I want to hide abandoned checkouts so my order list stays clear.**

### Feature: Admin Dashboard
[Admin login page](/readme_docs/features/admin_login.png)  
[Owner dashboard overview](/readme_docs/features/dashboard.png)

**How it was achieved**
- Custom owner dashboard separate from Django admin.
- Overview metrics surface key store information.
- Staff-only access enforced via decorators.

---

### Feature: Product Management
[Admin product list and filters](/readme_docs/features/products_admin.png)  
[Admin product edit form](/readme_docs/features/edit_product_admin.png)  
[Product image management interface](/readme_docs/features/image_manager_admin.png)  
[Toast notification when deleting a product](/readme_docs/features/toast_product_delete.png)  
[Archive-on-delete error handling](/readme_docs/features/product_delete_error.png)

**How it was achieved**
- Full CRUD for products with safeguards.
- Products with orders cannot be deleted and are archived instead.
- Image management decoupled from raw file handling.

---

### Feature: Order Management
[Admin orders management page](/readme_docs/features/orders_admin.png)

**How it was achieved**
- Orders grouped by fulfilment status.
- Admins can update order progress.
- Abandoned checkouts hidden from default views.

---

## Epic 6: UX, Feedback & Accessibility

### User Stories: Visual Feedback & Notifications
- **As a user, I want confirmation when I perform an action so I know it worked.**
- **As a user, I want error messages to be clear so I know how to fix problems.**
- **As a user, I want consistent feedback across the site so interactions feel predictable.**

### User Stories: Footer & Site Structure
- **As a user, I want consistent navigation links so I can move around the site easily.**
- **As a user, I want access to important links in the footer so I can find information quickly.**


### Feature: Visual Feedback & UI Polish
[Toast feedback for cart updates](/readme_docs/features/toast_add_to_cart.png)  
[Toast feedback for product deletion](/readme_docs/features/toast_product_delete.png)  
[Toast feedback for review submission](/readme_docs/features/toast_review_added.png)

**How it was achieved**
- Toasts provide immediate confirmation of actions.
- Disabled states prevent invalid interactions.
- Responsive layouts ensure usability across devices.

---

### Feature: Footer & Site Structure
[Site footer layout](/readme_docs/features/footer.png)

**How it was achieved**
- Consistent navigation across all pages.
- Reinforces brand identity and site structure.

---

## Summary

By integrating user stories directly into feature design, development remained user-focused throughout. Each feature was implemented with usability, security, and scalability in mind, resulting in a cohesive, production-ready e-commerce platform.
