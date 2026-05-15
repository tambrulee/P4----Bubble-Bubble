/**
 * Get a cookie value by name.
 *
 * Used mainly for grabbing Django's CSRF token from `document.cookie`.
 *
 * @param {string} name - The cookie name to look up (e.g. `"csrftoken"`).
 * @returns {string|undefined} The cookie value if found; otherwise `undefined`.
 *
 * @example
 * const csrf = getCookie("csrftoken");
 */
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

/**
 * Show a Bootstrap toast message for cart actions.
 *
 * Requires:
 * - A toast element with id `cart-toast`
 * - A toast body element with id `cart-toast-body`
 * - Bootstrap JS available on `window.bootstrap`
 *
 * If required elements/libraries are missing, this function does nothing.
 *
 * @param {string} [message] - The message to display. Defaults to `"Added to cart."`.
 * @returns {void}
 *
 * @example
 * showCartToast("Added to cart!");
 */
function showCartToast(message) {
  const toastEl = document.getElementById("cart-toast");
  const bodyEl = document.getElementById("cart-toast-body");
  if (!toastEl || !bodyEl || !window.bootstrap) return;

  bodyEl.textContent = message || "Added to cart.";
  bootstrap.Toast.getOrCreateInstance(toastEl, { delay: 2200 }).show();
}

/**
 * Update the cart count badge in the navbar (or wherever it's rendered).
 *
 * Updates the element text and toggles the `d-none` class so the badge hides
 * when the count is 0/empty.
 *
 * Requires an element with id `cart-count`.
 *
 * @param {number|string} count - The cart item count.
 * @returns {void}
 *
 * @example
 * setCartCount(3); // shows badge with "3"
 * setCartCount(0); // hides badge
 */
function setCartCount(count) {
  const badge = document.getElementById("cart-count");
  if (!badge) return;
  badge.textContent = count;
  badge.classList.toggle("d-none", !(Number(count) > 0));
}

/**
 * Fetch and render the mini cart HTML into the offcanvas drawer.
 *
 * Reads the mini cart endpoint from `#miniCart[data-mini-url]`.
 * Expects JSON shaped like:
 * - `{ ok: true, html: "<...>", cart_count: 3 }`
 * and optionally `mini_html` in other flows.
 *
 * Side effects:
 * - Updates `#mini-cart-content` with returned HTML.
 * - Updates the cart badge via `setCartCount` when `cart_count` is present.
 *
 * If the URL is missing or the request fails, an error message is rendered.
 *
 * @returns {Promise<void>}
 */
async function refreshMiniCart() {
  const container = document.getElementById("mini-cart-content");
  const offcanvasEl = document.getElementById("miniCart");
  if (!container || !offcanvasEl) return;

  const miniUrl = offcanvasEl.dataset.miniUrl;
  if (!miniUrl) {
    console.error("mini cart URL missing: add data-mini-url to #miniCart");
    container.innerHTML = `<div class="text-danger">Cart unavailable.</div>`;
    return;
  }

  try {
    const res = await fetch(miniUrl, {
      headers: { "X-Requested-With": "XMLHttpRequest" },
    });

    if (!res.ok) {
      console.error("mini cart fetch failed:", res.status);
      container.innerHTML = `<div class="text-danger">Couldn’t load cart.</div>`;
      return;
    }

    const data = await res.json();
    if (data.ok && data.html) {
      container.innerHTML = data.html;
      if (typeof data.cart_count !== "undefined") setCartCount(data.cart_count);
    } else {
      console.error("mini cart bad JSON:", data);
      container.innerHTML = `<div class="text-danger">Couldn’t load cart.</div>`;
    }
  } catch (err) {
    console.error("mini cart exception:", err);
    container.innerHTML = `<div class="text-danger">Couldn’t load cart.</div>`;
  }
}


document.addEventListener("DOMContentLoaded", () => {
  const offcanvasEl = document.getElementById("miniCart");

  // Load mini cart whenever drawer opens
  if (offcanvasEl) {
    offcanvasEl.addEventListener("shown.bs.offcanvas", refreshMiniCart);
  }

  // Single handler: Ajax add-to-cart (no redirect)
  document.addEventListener("submit", async (e) => {
    const form = e.target.closest("form.js-add-to-cart");
    if (!form) return;

    e.preventDefault();

    const submitBtn = form.querySelector('button[type="submit"], button:not([type])');
    const originalText = submitBtn ? submitBtn.textContent : null;

    try {
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = "Adding…";
      }

      const res = await fetch(form.action, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: new FormData(form),
      });

      if (!res.ok) {
        console.error("add_to_cart failed:", res.status);
        showCartToast("Couldn’t add to cart. Please try again.");
        return;
      }

      const data = await res.json();

      if (!data.ok) {
        showCartToast(data.message || "Sorry — couldn’t add to cart.");
        return;
      }

      showCartToast(data.message || "Added to cart!");
      if (typeof data.cart_count !== "undefined") setCartCount(data.cart_count);

      // If your add_to_cart returns mini_html, inject it immediately
      const container = document.getElementById("mini-cart-content");
      if (container && data.mini_html) container.innerHTML = data.mini_html;

      // Open the drawer after adding
      if (offcanvasEl) bootstrap.Offcanvas.getOrCreateInstance(offcanvasEl).show();

      if (submitBtn) {
        submitBtn.textContent = "Added ✓";
        setTimeout(() => {
          submitBtn.textContent = originalText;
        }, 900);
      }
    } catch (err) {
      console.error("add_to_cart exception:", err);
      showCartToast("Network error — please try again.");
    } finally {
      if (submitBtn) submitBtn.disabled = false;
    }
  });
});

/**
 * POST an updated quantity for a cart line item.
 *
 * Sends `qty` as form data to the provided `updateUrl`, with Django CSRF + AJAX headers.
 * Expects a JSON response such as:
 * - `{ ok: true, cart_count: 3, mini_html: "<...>" }`
 *
 * Throws if the HTTP response is not OK (non-2xx).
 *
 * @param {string} updateUrl - Endpoint URL that accepts `POST qty=<number>`.
 * @param {number|string} qty - Desired quantity.
 * @returns {Promise<any>} Parsed JSON response from the server.
 *
 * @throws {Error} If the request fails at the HTTP level.
 */
async function postQtyUpdate(updateUrl, qty) {
  const formData = new FormData();
  formData.append("qty", qty);

  const res = await fetch(updateUrl, {
    method: "POST",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: formData,
  });

  if (!res.ok) throw new Error("qty update failed");
  return await res.json();
}


document.addEventListener("click", async (e) => {
  const btn = e.target.closest(".js-qty");
  if (!btn) return;

  const updateUrl = btn.dataset.updateUrl;
  const action = btn.dataset.action;
  const stock = Number(btn.dataset.stock || 9999);

  const input = btn.parentElement.querySelector(".js-qty-input");
  if (!input) return;

  let current = Number(input.value || 1);
  let next = current;

  if (action === "inc") next = Math.min(current + 1, stock);
  if (action === "dec") next = Math.max(current - 1, 1);

  if (next === current) return;

  // optimistic UI
  input.value = next;

  try {
    const data = await postQtyUpdate(updateUrl, next);
    if (data.ok) {
      setCartCount(data.cart_count);
      const container = document.getElementById("mini-cart-content");
      if (container && data.mini_html) container.innerHTML = data.mini_html;
      // optional:
      // showCartToast(data.message || "Cart updated.");
    } else {
      showCartToast("Couldn’t update quantity.");
      await refreshMiniCart();
    }
  } catch (err) {
    console.error(err);
    showCartToast("Network error — please try again.");
    await refreshMiniCart();
  }
});


document.addEventListener("change", async (e) => {
  const input = e.target.closest(".js-qty-input");
  if (!input) return;

  const updateUrl = input.dataset.updateUrl;
  const stock = Number(input.dataset.stock || 9999);

  let next = Number(input.value || 1);
  next = Math.max(1, Math.min(next, stock));
  input.value = next;

  try {
    const data = await postQtyUpdate(updateUrl, next);
    if (data.ok) {
      setCartCount(data.cart_count);
      const container = document.getElementById("mini-cart-content");
      if (container && data.mini_html) container.innerHTML = data.mini_html;
    } else {
      showCartToast("Couldn’t update quantity.");
      await refreshMiniCart();
    }
  } catch (err) {
    console.error(err);
    showCartToast("Network error — please try again.");
    await refreshMiniCart();
  }
});


document.addEventListener("submit", async (e) => {
  const form = e.target.closest("form.js-mini-remove");
  if (!form) return;

  e.preventDefault();

  try {
    const res = await fetch(form.action, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    });

    if (!res.ok) {
      showCartToast("Couldn’t remove item.");
      return;
    }

    const data = await res.json();

    if (!data.ok) {
      showCartToast("Couldn’t remove item.");
      return;
    }

    // Refresh mini cart contents
    await refreshMiniCart();

    // Update cart badge
    if (typeof data.cart_count !== "undefined") {
      setCartCount(data.cart_count);
    }
  } catch (err) {
    console.error("mini remove error:", err);
    showCartToast("Network error — please try again.");
  }
});
