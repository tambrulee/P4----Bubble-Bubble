## Form Validation – Account Registration

This project implements robust form validation to ensure **data integrity**, **security**, and a **clear user experience**. Validation is handled primarily server-side using Django Forms, with client-side feedback layered on top to improve usability.

This section uses the account registration flow as a case example.

---

## Case Example: Account Sign-Up Template

**File path:**
```
bubblebubble/accounts/templates/accounts/signup.html
```

The sign-up page is responsible for collecting user credentials and providing immediate, accessible feedback when validation errors occur.

---

## Server-Side Validation Integration

The [sign-up template](/readme_docs/img/pw_valid.png) renders a Django form derived from `UserCreationForm`, which enforces several validation rules automatically, including:

- Password length requirements
- Password confirmation matching
- Protection against weak or common passwords

Additional custom validation is implemented in the form logic to ensure:
- [Email addresses are unique](/readme_docs/img/em_valid.png)
- Email input is normalised (lowercased and trimmed)
- User accounts cannot be duplicated using case variations

All validation occurs server-side before any user data is saved.

---

## Error Handling & Feedback in the Template

The template displays validation feedback clearly and close to the relevant input fields.

Key validation patterns used in `signup.html` include:

- **Non-field errors**
```django
{{ form.non_field_errors }}
```

- **Field-level error rendering**
```django
{{ form.email }}
{% for error in form.email.errors %}
  <div class="text-danger small mt-1">{{ error }}</div>
{% endfor %}
```

- **CSRF protection**
```django
{% csrf_token %}
```

---

## Client-Side Usability Enhancements

While server-side validation is treated as the final authority, the sign-up template enhances the user experience with additional client-side guidance:

- Inline password requirement tips
- A password strength meter
- JavaScript loaded via:
```django
{% block extra_js %}
  <script src="{% static 'accounts/js/password.js' %}"></script>
{% endblock  extra_js %}
```

These enhancements reduce user friction while maintaining full reliance on Django’s secure backend validation.

---

## Accessibility & UX Considerations

The form layout prioritises clarity and accessibility by:
- Using clear labels for all inputs
- Displaying errors in readable, plain language
- Maintaining consistent spacing and visual hierarchy
- Avoiding silent validation failures

The `novalidate` attribute is used so Django’s validation messages take precedence over browser-default messaging.

---

## Summary

The account registration form demonstrates a layered validation strategy:

- **Server-side validation** ensures security and data integrity
- **Template-level error handling** provides clear, contextual feedback
- **Client-side enhancements** improve usability without compromising safety

This approach follows Django best practices and supports a secure, user-friendly authentication flow.
