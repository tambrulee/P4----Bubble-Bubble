import { defineConfig } from "eslint/config";

export default defineConfig([
  {
    ignores: [
      "node_modules/**",
      "staticfiles/**",
      "dist/**",
      "build/**",
    ],
  },
  {
    files: ["bubblebubble/static/**/*.js"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        window: "readonly",
        document: "readonly",
        console: "readonly",
      },
    },
    rules: {
      "no-unused-vars": "warn",
      eqeqeq: ["error", "always"],
    },
  },
]);

