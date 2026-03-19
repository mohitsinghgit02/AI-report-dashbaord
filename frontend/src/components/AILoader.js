import React from "react";
import "../styles/loader.css";

export default function AILoader() {

    return (
        <div className="loader-container">

            <div className="ai-brain"></div>

            <h2>AI is analysing your data</h2>

            <p>
                Generating insights and building dashboard...
            </p>

        </div>
    );
}