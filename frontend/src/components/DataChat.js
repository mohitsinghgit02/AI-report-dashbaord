import React, { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function AIDrawerChat({ refKey }) {

    const [open, setOpen] = useState(false);
    const [expanded, setExpanded] = useState(false);

    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);

    const [listening, setListening] = useState(false);
    const [language, setLanguage] = useState("en");

    const recognitionRef = useRef(null);
    const bottomRef = useRef(null);

    const langMap = {
        en: "en-US",
        hi: "hi-IN"
    };

    /* --------------------------
       Auto Scroll
    -------------------------- */

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    /* --------------------------
       CLEAN MARKDOWN FOR SPEECH
    -------------------------- */

    const cleanMarkdownForSpeech = (markdown) => {

        if (!markdown) return "";

        let text = markdown;

        text = text.replace(/```[\s\S]*?```/g, "");
        text = text.replace(/`.*?`/g, "");
        text = text.replace(/\|.*\|/g, "");
        text = text.replace(/^#{1,6}\s*/gm, "");

        text = text.replace(/\*\*(.*?)\*\*/g, "$1");
        text = text.replace(/\*(.*?)\*/g, "$1");
        text = text.replace(/_(.*?)_/g, "$1");

        text = text.replace(/\[(.*?)\]\(.*?\)/g, "$1");

        text = text.replace(
            /([\u2700-\u27BF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|\uD83E[\uDD00-\uDDFF])/g,
            ""
        );

        text = text.replace(/[-*_>#]/g, "");
        text = text.replace(/\s+/g, " ").trim();

        return text;
    };

    /* --------------------------
       SPEECH FUNCTIONS
    -------------------------- */

    const speakText = (markdownText) => {

        window.speechSynthesis.cancel();

        const cleanText = cleanMarkdownForSpeech(markdownText);

        if (!cleanText) return;

        const sentences =
            cleanText.match(/[^\.!\?]+[\.!\?]+/g) || [cleanText];

        let i = 0;

        const speakNext = () => {

            if (i >= sentences.length) return;

            const utterance = new SpeechSynthesisUtterance(sentences[i]);

            utterance.lang = langMap[language];

            utterance.onend = () => {
                i++;
                speakNext();
            };

            window.speechSynthesis.speak(utterance);
        };

        speakNext();
    };

    const stopSpeech = () => {
        window.speechSynthesis.cancel();
    };

    /* --------------------------
       Voice Recognition Setup
    -------------------------- */

    useEffect(() => {

        const SpeechRecognition =
            window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) return;

        const recognition = new SpeechRecognition();

        recognition.continuous = true;
        recognition.interimResults = false;

        recognition.onstart = () => setListening(true);

        recognition.onend = () => setListening(false);

        recognition.onresult = (event) => {

            let transcript = "";

            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript;
            }

            setInput(transcript);
        };

        recognitionRef.current = recognition;

    }, []);

    /* --------------------------
       Voice Input
    -------------------------- */

    const startListening = () => {

        if (!recognitionRef.current) return;

        recognitionRef.current.lang = langMap[language];

        setInput("");

        recognitionRef.current.start();
    };

    const stopListening = () => {

        if (!recognitionRef.current) return;

        recognitionRef.current.stop();

        if (input.trim()) {
            sendMessage(input);
        }
    };

    /* --------------------------
       SEND MESSAGE
    -------------------------- */

    const sendMessage = async (voiceText = null) => {

        const question = voiceText || input;

        if (!question.trim() || loading) return;

        const userMsg = { role: "user", text: question };

        const newMessages = [...messages, userMsg];

        setMessages(newMessages);

        setInput("");

        setLoading(true);

        const response = await fetch(
            `${process.env.REACT_APP_API_URL}/chat/ask`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    ref_key: refKey,
                    question: question,
                    lang: language
                })
            }
        );

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let aiMessage = "";

        while (true) {

            const { done, value } = await reader.read();

            if (done) break;

            const chunk = decoder.decode(value);

            aiMessage += chunk;

            setMessages([
                ...newMessages,
                { role: "ai", text: aiMessage }
            ]);
        }

        setLoading(false);
    };

    return (

        <>
            {/* Floating Button */}

            <button
                className="ai-chat-button"
                onClick={() => setOpen(!open)}
            >
                🤖
            </button>

            {/* Drawer */}

            <div className={`ai-drawer ${open ? "open" : ""} ${expanded ? "expanded" : ""}`}>

                {/* Header */}

                <div className="ai-header">

                    <div>
                        <strong>AI Data Assistant</strong>
                        <div className="ai-subtitle">
                            Ask questions about this dataset
                        </div>
                    </div>

                    <div className="ai-header-buttons">

                        <button
                            className="expand-btn"
                            onClick={() => setExpanded(!expanded)}
                        >
                            {expanded ? "🗗" : "🗖"}
                        </button>

                        <button
                            className="ai-close"
                            onClick={() => setOpen(false)}
                        >
                            ✕
                        </button>

                    </div>

                </div>

                {/* Language Selector */}

                <div className="ai-lang-select">

                    <select
                        value={language}
                        onChange={(e) => setLanguage(e.target.value)}
                    >
                        <option value="en">English</option>
                        <option value="hi">Hindi</option>
                        <option value="gu">Gujarati</option>
                    </select>

                </div>

                {/* Messages */}

                <div className="ai-messages">

                    {messages.map((m, i) => (

                        <div
                            key={i}
                            className={`ai-message ${m.role}`}
                        >

                            <div className="bubble">

                                <div className="markdown-body">

                                    <ReactMarkdown
                                        remarkPlugins={[remarkGfm]}
                                        components={{

                                            table: ({ children }) => (
                                                <div className="table-wrapper">
                                                    <table>{children}</table>
                                                </div>
                                            ),

                                            code({ inline, children }) {

                                                if (inline) {
                                                    return (
                                                        <code className="inline-code">
                                                            {children}
                                                        </code>
                                                    );
                                                }

                                                return (
                                                    <pre className="code-block">
                                                        <code>{children}</code>
                                                    </pre>
                                                );
                                            }

                                        }}
                                    >
                                        {m.text}
                                    </ReactMarkdown>

                                </div>

                                {/* Speech controls for AI message */}

                                {m.role === "ai" && (

                                    <div className="speech-controls">

                                        <button
                                            onClick={() => speakText(m.text)}
                                        >
                                            🔊 Read
                                        </button>

                                        <button
                                            onClick={stopSpeech}
                                        >
                                            ⏹ Stop
                                        </button>

                                    </div>

                                )}

                            </div>

                        </div>

                    ))}

                    {loading && (

                        <div className="ai-message ai">

                            <div className="bubble">
                                AI is thinking...
                            </div>

                        </div>

                    )}

                    <div ref={bottomRef}></div>

                </div>

                {/* Input */}

                <div className="ai-input">

                    <input
                        value={input}
                        placeholder="Ask about the data..."
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) =>
                            e.key === "Enter" && sendMessage()
                        }
                    />

                    <button onClick={() => sendMessage()}>
                        Send
                    </button>

                    {/* Voice Button */}

                    <button
                        className={`voice-btn ${listening ? "listening" : ""}`}
                        onMouseDown={startListening}
                        onMouseUp={stopListening}
                        onTouchStart={startListening}
                        onTouchEnd={stopListening}
                    >
                        {listening ? "🎙 Listening..." : "🎤 Hold"}
                    </button>

                </div>

            </div>

        </>
    );
}