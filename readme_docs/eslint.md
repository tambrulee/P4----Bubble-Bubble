# JavaScript Linting (ESLint)

ESLint was used to test and improve the quality of the project’s custom JavaScript code.

The project uses **ESLint v9** with the flat configuration format (`eslint.config.js`). Linting was intentionally limited to source files only (`bubblebubble/static/**/*.js`) to avoid analysing generated or third-party JavaScript.

Generated files such as Django’s collected static files and vendor libraries were excluded using the `ignores` property in the ESLint configuration, in line with current ESLint guidance.

Global browser libraries (e.g. Bootstrap loaded via CDN) were explicitly declared as read-only globals to prevent false `no-undef` errors.

Linting was run using:

```bash
npx eslint "bubblebubble/static/**/*.js"

```
All custom JavaScript files passed ESLint with no remaining errors, confirming consistent, maintainable client-side code.