  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  function showCartToast(message) {
    const toastEl = document.getElementById("cart-toast");
    const bodyEl = document.getElementById("cart-toast-body");
    if (!toastEl || !bodyEl || !window.bootstrap) return;

    bodyEl.textContent = message;
    const toast = bootstrap.Toast.getOrCreateInstance(toastEl, { delay: 2200 });
    toast.show();
  }

  function setCartCount(count) {
    const badge = document.getElementById("cart-count");
    if (!badge) return;
    badge.textContent = count;

    // optional: hide badge when 0
    if (Number(count) <= 0) badge.classList.add("d-none");
    else badge.classList.remove("d-none");
  }

  document.addEventListener("submit", async (e) => {
    const form = e.target;
    if (!form.classList.contains("js-add-to-cart")) return;

    e.preventDefault();

    const submitBtn = form.querySelector('button[type="submit"], button:not([type])');
    const originalText = submitBtn ? submitBtn.textContent : null;

    try {
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = "Adding…";
      }

      const url = form.action;
      const formData = new FormData(form);

      const res = await fetch(url, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: formData,
      });

      const data = await res.json();

      if (!res.ok || !data.ok) {
        const msg = data && data.message ? data.message : "Sorry — couldn’t add to cart.";
        showCartToast(msg);
        return;
      }

      showCartToast(data.message || "Added to cart!");
      if (typeof data.cart_count !== "undefined") {
        setCartCount(data.cart_count);
      }

      // optional: little success flash on button
      if (submitBtn) {
        submitBtn.textContent = "Added ✓";
        setTimeout(() => {
          submitBtn.textContent = originalText;
        }, 900);
      }

    } catch (err) {
      showCartToast("Network error — please try again.");
    } finally {
      if (submitBtn) submitBtn.disabled = false;
    }
  });

