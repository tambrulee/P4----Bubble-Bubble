document.addEventListener("DOMContentLoaded", () => {
  const fieldName = document.querySelector("[data-rating-field]")?.dataset.ratingField;
  if (!fieldName) return;

  const starsWrap = document.querySelector(".star-rating");
  if (!starsWrap) return;

  const stars = Array.from(starsWrap.querySelectorAll(".star"));
  const ratingText = document.getElementById("ratingText");

  const selectField = document.querySelector(`select[name="${fieldName}"]`);
  const radioFields = Array.from(document.querySelectorAll(`input[type="radio"][name="${fieldName}"]`));

  function getCurrentValue() {
    if (selectField) return parseInt(selectField.value || "0", 10) || 0;

    if (radioFields.length) {
      const checked = radioFields.find(r => r.checked);
      return checked ? (parseInt(checked.value, 10) || 0) : 0;
    }

    const generic = document.querySelector(`[name="${fieldName}"]`);
    return generic ? (parseInt(generic.value || "0", 10) || 0) : 0;
  }

  function setStars(val) {
    stars.forEach((btn) => {
      const v = parseInt(btn.dataset.value || "0", 10);
      btn.classList.toggle("is-on", v <= val);
    });
    if (ratingText) ratingText.textContent = val ? `${val} / 5` : "Click to rate";
  }

  function setFieldValue(val) {
    if (selectField) {
      selectField.value = String(val);
      selectField.dispatchEvent(new Event("change", { bubbles: true }));
      return;
    }

    if (radioFields.length) {
      radioFields.forEach(r => (r.checked = r.value === String(val)));
      return;
    }

    const generic = document.querySelector(`[name="${fieldName}"]`);
    if (generic) generic.value = String(val);
  }

  // init from existing form value (important after validation errors)
  setStars(getCurrentValue());

  // interactions
  stars.forEach((btn) => {
    btn.addEventListener("click", () => {
      const val = parseInt(btn.dataset.value || "0", 10) || 0;
      setFieldValue(val);
      setStars(val);
    });

    btn.addEventListener("mouseenter", () => {
      const val = parseInt(btn.dataset.value || "0", 10) || 0;
      setStars(val);
    });
  });

  starsWrap.addEventListener("mouseleave", () => {
    setStars(getCurrentValue());
  });

  const comment = document.getElementById("id_comment") || document.querySelector("textarea");
  if (comment) comment.classList.add("review-textarea");
});
