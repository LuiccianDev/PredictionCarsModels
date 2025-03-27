# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript and enable type-aware lint rules. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

## About the Project

This project is part of the **PyPredictionCarModels** application, which aims to predict car models based on various input parameters. The `frontend` folder contains the client-side code for the application, built using React and Vite. It provides an interactive user interface for users to input data, view predictions, and interact with the system.

### Key Features

- **User Interface**: A responsive and user-friendly interface for interacting with the prediction system.
- **Data Input**: Forms and components to collect user input for car model predictions.
- **Visualization**: Display of prediction results and other relevant data.
- **Routing**: Organized navigation between different pages of the application.

## Project Structure

The `frontend` folder is organized as follows:

```
frontend/
├── public/               # Static assets (e.g., images, icons)
├── src/                  # Source code
│   ├── assets/           # Static files imported into the app (e.g., images, fonts)
│   ├── components/       # Reusable React components
│   ├── pages/            # Page components for routing
│   ├── styles/           # Global and component-specific styles
│   ├── utils/            # Utility functions and helpers
│   ├── App.jsx           # Main application component
│   ├── main.jsx          # Entry point for the React app
│   └── ...               # Other files (e.g., context, hooks)
├── .eslintrc.cjs         # ESLint configuration
├── vite.config.js        # Vite configuration
├── package.json          # Project dependencies and scripts
└── README.md             # Project documentation
```

This structure ensures a clean and maintainable codebase for the project.

## Getting Started

To run the frontend locally:

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:3000` to view the application.
