import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import Chart from "chart.js/auto";

window.Chart = Chart;

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
    <App />
);