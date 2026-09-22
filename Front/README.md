# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is enabled on this template. See [this documentation](https://react.dev/learn/react-compiler) for more information.

Note: This will impact Vite dev & build performances.

## Backend API Setup

The frontend expects the backend API to be available at the URL configured with `VITE_API_BASE`.

By default this project uses:

```bash
VITE_API_BASE=http://127.0.0.1:8000
```

If `VITE_API_BASE` is left empty, Vite will proxy `/api` and `/media` requests to the backend when using the development server.

Make sure your Django backend is running locally before starting Vite.

Example:

```bash
cd ../Back
python manage.py runserver 0.0.0.0:8000
cd ../my-app
npm run dev
```

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
