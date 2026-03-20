import React, { useEffect, useState, useRef } from "react";
import Chart from "chart.js/auto";
import AILoader from "../components/AILoader";
import AIDrawerChat from "../components/DataChat";
import "../styles/dashboard.css";

export default function ReportViewer() {

    const [dashboard, setDashboard] = useState(null);
    const [lang, setLang] = useState("en");
    const [refKey, setRefKey] = useState(null);

    const chartRefs = useRef({});

    const chartPalette = [
        "#6366F1",
        "#22C55E",
        "#F59E0B",
        "#3B82F6",
        "#EF4444",
        "#14B8A6",
        "#8B5CF6",
        "#EC4899"
    ];

    const normalizeChartType = (type) => {

        if (!type) return "bar";

        const t = type.toLowerCase();

        if (t === "histogram") return "bar";
        if (t === "box") return "bar";
        if (t === "donut") return "doughnut";
        if (t === "area") return "line";

        return t;
    };

    const cleanChartData = (chart) => {

        if (!chart.values || chart.values.length === 0)
            return chart;

        const unique = [...new Set(chart.values)];

        if (unique.length === 1) {

            return {
                ...chart,
                labels: ["Value"],
                values: [unique[0]]
            };
        }

        return chart;
    };

    const normalizeDashboard = (data) => {

        return {

            ...data,

            kpis: data.kpis.map(k => ({
                label: k.metric || k.label,
                value: k.total || k.value,
                description:
                    `Average ${k.metric || k.label} is ${k.avg?.toFixed?.(2) || ""}`
            })),

            charts: data.charts.slice(0, 8).map(c => {

                const cleaned = cleanChartData(c);

                return {
                    ...cleaned,
                    type: normalizeChartType(cleaned.type),
                    description: `Distribution of ${cleaned.title}`
                };

            }),

            insights: data.insights || [],
            predictions: data.predictions || []

        };

    };

    useEffect(() => {

        const params = new URLSearchParams(window.location.search);

        const file = params.get("file");
        const urlLang = params.get("lang") || "en";

        setLang(urlLang);

        const api =
            `${process.env.REACT_APP_API_URL}/reports/damage_stock?file=${file}&lang=${urlLang}`;

        fetch(api)
            .then(res => res.json())
            .then(data => {

                setRefKey(data.ref_key);

                const normalized = normalizeDashboard(data);

                setDashboard(normalized);

                setTimeout(() => renderCharts(normalized.charts), 200);

            })
            .catch(err => console.error(err));

    }, []);

    const renderCharts = (charts) => {

        charts.forEach((chart, i) => {

            const canvas = document.getElementById(`chart-${i}`);

            if (!canvas) return;

            if (chartRefs.current[i])
                chartRefs.current[i].destroy();

            chartRefs.current[i] = new Chart(canvas, {

                type: chart.type || "bar",

                data: {
                    labels: chart.labels,
                    datasets: [{
                        label: chart.title,
                        data: chart.values,
                        backgroundColor: chartPalette,
                        borderRadius: 6
                    }]
                },

                options: {

                    responsive: true,
                    maintainAspectRatio: false,

                    animation: {
                        duration: 1200
                    },

                    plugins: {
                        legend: { position: "bottom" }
                    },

                    scales: chart.type === "pie" || chart.type === "doughnut"
                        ? {}
                        : {
                            x: { grid: { display: false } },
                            y: { grid: { color: "#e5e7eb" } }
                        }

                }

            });

        });

    };

    const speakText = (text) => {

        if (!("speechSynthesis" in window)) return;

        const utter = new SpeechSynthesisUtterance(text);

        const voices = window.speechSynthesis.getVoices();

        let voice =
            voices.find(v => v.lang.startsWith("gu")) ||
            voices.find(v => v.lang.startsWith("hi")) ||
            voices.find(v => v.lang.startsWith("en"));

        if (voice) utter.voice = voice;

        window.speechSynthesis.speak(utter);
    };

    if (!dashboard) return <AILoader />;

    return (

        <div className="dashboard">

            <div className="hero">

                <div className="hero-left">

                    <h1>{dashboard.title}</h1>

                    <p>{dashboard.summary}</p>

                </div>

                <div className="hero-actions">

                    <button
                        className="btn-secondary"
                        onClick={() => speakText(dashboard.summary)}
                    >
                        🔊 Narrate
                    </button>

                </div>

            </div>

            <div className="kpi-grid">

                {dashboard.kpis.map((kpi, i) => (

                    <div key={i} className="kpi-card gradient-card">

                        <div className="kpi-top">

                            <h4>{kpi.label}</h4>

                            <button
                                className="icon-btn"
                                onClick={() => speakText(kpi.description)}
                            >
                                🔊
                            </button>

                        </div>

                        <h2>{kpi.value.toLocaleString()}</h2>

                        <p>{kpi.description}</p>

                    </div>

                ))}

            </div>

            <h2 className="section-title">📊 Data Visualization</h2>

            <div className="charts-grid">

                {dashboard.charts.map((chart, i) => (

                    <div key={i} className="chart-card">

                        <div className="chart-header">

                            <h3>{chart.title}</h3>

                            <button
                                className="icon-btn"
                                onClick={() => speakText(chart.description)}
                            >
                                🔊
                            </button>

                        </div>

                        <p className="chart-desc">{chart.description}</p>

                        <div className="chart-canvas">
                            <canvas id={`chart-${i}`} />
                        </div>

                    </div>

                ))}

            </div>

            <h2 className="section-title">🤖 AI Insights</h2>

            <div className="insight-card">

                <ul>

                    {dashboard.insights.map((insight, i) => (

                        <li key={i}>

                            {insight.text}

                            <button
                                className="icon-btn"
                                onClick={() => speakText(insight.text)}
                            >
                                🔊
                            </button>

                        </li>

                    ))}

                </ul>

            </div>

            {dashboard.predictions.length > 0 && (

                <>

                    <h2 className="section-title">🔮 AI Predictions</h2>

                    <div className="prediction-card">

                        <ul>

                            {dashboard.predictions.map((p, i) => (

                                <li key={i}>

                                    {p.text}

                                    <button
                                        className="icon-btn"
                                        onClick={() => speakText(p.text)}
                                    >
                                        🔊
                                    </button>

                                </li>

                            ))}

                        </ul>

                    </div>

                </>

            )}

            {/* CHAT */}

            {refKey && <AIDrawerChat refKey={refKey} />}

        </div>

    );
}