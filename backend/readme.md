# Project Requirements Checklist

## User Authentication (Basic Login Simulation)
- [x] User can enter their **Name** and **Email** to access the application.
- [x] Input fields have **validation** to ensure data accuracy and prevent invalid submissions.
- [x] No authentication system (e.g., OAuth, JWT) is required—just basic user identification.

## Product Catalog
- [ ] Fetch products from the **Fake Store API**.
- [ ] Display product details:
  - [ ] Title
  - [ ] Image
  - [ ] Price
  - [ ] Quantity
  - [ ] Description

## Shopping Cart
- [ ] Users can **add products** to the cart.
- [ ] Users can **remove products** from the cart.
- [ ] The cart **persists during the session** (refreshing the page doesn’t clear it).

## Order Submission
- [ ] Users can review their cart and submit an order.
- [ ] Simulate the order submission process and return a **success message** (no payment processing).

## Order History
- [x] Users can view a list of their **past orders**.
- [x] Order details include:
  - [x] Product names
  - [x] Quantities
  - [x] Total price
  - [ x Order date
- [x] Backend persistence for storing order history.

## Responsive Layout
- [ ] Create a **responsive layout**.
- [ ] Use either:
  - [ ] Pure CSS
  - [ ] Tailwind CSS
  - [ ] styled-components

## Testing
- [ ] Write **unit tests** for the code.
