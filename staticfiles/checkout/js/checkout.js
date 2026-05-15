// Get saved addresses and apply to form fields
(function () {
  const select = document.getElementById("id_saved_address");
  if (!select) return;

  const dataEl = document.getElementById("saved-addresses-data");
  if (!dataEl) return;

  let map = {};
  try { map = JSON.parse(dataEl.textContent || "{}"); }
  catch (e) { console.warn("Bad saved address JSON", e); return; }

  const f = {
    full_name: document.getElementById("id_full_name"),
    address_line1: document.getElementById("id_address_line1"),
    address_line2: document.getElementById("id_address_line2"),
    city: document.getElementById("id_city"),
    postcode: document.getElementById("id_postcode"),
  };

  function nudgeFloating(input) {
    if (!input) return;
    input.dispatchEvent(new Event("input", { bubbles: true }));
    input.dispatchEvent(new Event("change", { bubbles: true }));
  }

  /***
   * Apply the saved address with primary key `pk` to the form fields.
   */
  function apply(pk) {
    const a = map[String(pk)];
    if (!a) return;

    if (f.full_name) f.full_name.value = a.full_name || "";
    if (f.address_line1) f.address_line1.value = a.address_line1 || "";
    if (f.address_line2) f.address_line2.value = a.address_line2 || "";
    if (f.city) f.city.value = a.city || "";
    if (f.postcode) f.postcode.value = a.postcode || "";

    const saveCb = document.getElementById("id_save_address");
    if (saveCb) saveCb.checked = false;

    Object.values(f).forEach(nudgeFloating);
  }

  select.addEventListener("change", () => {
    if (!select.value) return;
    apply(select.value);
  });

  if (select.value) apply(select.value);
})();


// Bootstrap form validation with opt-out for specific fields
(() => {
  "use strict";

  const forms = document.querySelectorAll(".needs-validation");

  Array.from(forms).forEach((form) => {
    form.addEventListener("submit", (event) => {
      const skip = form.querySelectorAll("[data-no-validate]");
      skip.forEach(el => el.disabled = true);

      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }

      skip.forEach(el => el.disabled = false);
      form.classList.add("was-validated");
    }, false);
  });
})();
