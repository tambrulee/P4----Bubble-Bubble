(function () {
  // Works for signup (id_password1) and reset confirm (id_new_password1)
  const pwInput =
    document.getElementById("id_password1") ||
    document.getElementById("id_new_password1");

  if (!pwInput) return;

  const bar = document.getElementById("pwStrengthBar");
  const label = document.getElementById("pwStrengthLabel");

  const ruleLength = document.getElementById("rule-length");
  const ruleNumber = document.getElementById("rule-number");
  const ruleLetter = document.getElementById("rule-letter");
  const ruleCommon = document.getElementById("rule-common");

  /***
   * Set or clear a rule tick
   */
  function setRule(el, ok) {
    if (!el) return;
    el.textContent = el.textContent.replace(/^✔|^✖/, ok ? "✔" : "✖");
    el.classList.toggle("text-success", ok);
    el.classList.toggle("text-muted", !ok);
  }

  // Very small common-password heuristic (client-side only).
  // Django still enforces real "CommonPasswordValidator" server-side.
  const common = new Set([
    "password", "password1", "password123", "12345678", "123456789",
    "qwerty", "qwerty123", "letmein", "iloveyou", "admin", "welcome"
  ]);

  /**
    * Score the password and return { score, text }
   */
  function scorePassword(pw) {
    const lengthOK = pw.length >= 8;
    const hasNumber = /\d/.test(pw);
    const hasLetter = /[a-zA-Z]/.test(pw);
    const notCommon = pw.length > 0 && !common.has(pw.toLowerCase());

    // tick rules
    setRule(ruleLength, lengthOK);
    setRule(ruleNumber, hasNumber);
    setRule(ruleLetter, hasLetter);
    setRule(ruleCommon, notCommon);

    // score
    let score = 0;
    if (lengthOK) score += 35;
    if (hasLetter) score += 20;
    if (hasNumber) score += 20;
    if (/[^a-zA-Z0-9]/.test(pw)) score += 15; // special char bonus
    if (pw.length >= 12) score += 10; // extra length bonus
    if (!notCommon) score = Math.min(score, 25);

    score = Math.max(0, Math.min(100, score));

    let text = "—";
    if (pw.length === 0) text = "—";
    else if (score < 35) text = "Weak";
    else if (score < 70) text = "Okay";
    else text = "Strong";

    return { score, text };
  }

  /*** 
   * Update the UI based on current password */
  function update() {
    const { score, text } = scorePassword(pwInput.value);

    if (bar) {
      bar.style.width = score + "%";
      bar.setAttribute("aria-valuenow", String(score));

      // Bootstrap classes (no custom CSS needed)
      bar.classList.remove("bg-danger", "bg-warning", "bg-success");
      if (pwInput.value.length === 0) {
        // keep neutral
      } else if (score < 35) {
        bar.classList.add("bg-danger");
      } else if (score < 70) {
        bar.classList.add("bg-warning");
      } else {
        bar.classList.add("bg-success");
      }
    }

    if (label) label.textContent = text;
  }

  pwInput.addEventListener("input", update);
  update();
})();

