// app/static/js/chat.js

document.addEventListener("DOMContentLoaded", () => {
    const messagesEl = document.getElementById("chat-messages");
    const optionsEl = document.getElementById("chat-options");
    const formEl = document.getElementById("chat-form");
    const inputEl = document.getElementById("chat-input");
    const connDot = document.getElementById("connection-dot");
    const connStatus = document.getElementById("connection-status");

    let ws = null;

    function connectWebSocket() {
        const protocol = window.location.protocol === "https:" ? "wss" : "ws";
        const wsUrl = `${protocol}://${window.location.host}/ws`;
        ws = new WebSocket(wsUrl);

        ws.onopen = () => {
            if (connDot) connDot.classList.remove("bg-red-500");
            if (connDot) connDot.classList.add("bg-emerald-400");
            if (connStatus) connStatus.textContent = "Connected";

            // Trigger initial greeting
            ws.send(JSON.stringify({ text: "start" }));
        };

        ws.onclose = () => {
            if (connDot) connDot.classList.remove("bg-emerald-400");
            if (connDot) connDot.classList.add("bg-red-500");
            if (connStatus) connStatus.textContent = "Disconnected";
        };

        ws.onerror = () => {
            if (connDot) connDot.classList.remove("bg-emerald-400");
            if (connDot) connDot.classList.add("bg-red-500");
            if (connStatus) connStatus.textContent = "Error";
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                renderBotResponse(data);
            } catch (err) {
                console.error("Invalid bot response:", err);
            }
        };
    }

    function scrollToBottom() {
        if (!messagesEl) return;
        messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    function createMessageBubble(text, side = "bot") {
        const wrapper = document.createElement("div");
        wrapper.className = `flex ${side === "user" ? "justify-end" : "justify-start"}`;

        const bubble = document.createElement("div");
        bubble.className =
            side === "user"
                ? "max-w-[80%] rounded-2xl px-3 py-2 text-xs sm:text-sm bg-emerald-500 text-slate-900 shadow-md"
                : "max-w-[80%] rounded-2xl px-3 py-2 text-xs sm:text-sm bg-slate-800 text-slate-100 border border-slate-700 shadow-md";

        bubble.innerHTML = text
            .replace(/\n/g, "<br>")
            .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

        wrapper.appendChild(bubble);
        messagesEl.appendChild(wrapper);
        scrollToBottom();
    }

    function clearOptions() {
        if (!optionsEl) return;
        optionsEl.innerHTML = "";
        optionsEl.classList.add("hidden");
    }

    function renderOptions(options) {
        clearOptions();
        if (!options || options.length === 0) return;

        optionsEl.classList.remove("hidden");
        options.forEach((opt) => {
            const btn = document.createElement("button");
            btn.type = "button";
            btn.className =
                "text-xs sm:text-[13px] px-3 py-2 rounded-xl border border-slate-700 bg-slate-800/80 hover:bg-slate-700/80 text-slate-100 transition";
            btn.textContent = opt.label;

            btn.addEventListener("click", () => {
                // Send the value, show label as user message
                sendUserMessage(opt.value, opt.label);
            });

            optionsEl.appendChild(btn);
        });
    }

    function renderProperties(properties) {
        if (!properties || properties.length === 0) return;

        const gridWrapper = document.createElement("div");
        gridWrapper.className = "grid grid-cols-1 sm:grid-cols-2 gap-3 mt-1";

        properties.forEach((p) => {
            const card = document.createElement("div");
            card.className =
                "rounded-2xl bg-slate-900/90 border border-slate-800 px-3 py-3 text-xs text-slate-100 shadow";

            const title = document.createElement("div");
            title.className = "font-semibold mb-1";
            title.textContent = p.title || "Property";

            const meta = document.createElement("div");
            meta.className = "text-[11px] text-slate-300 space-y-0.5";
            meta.innerHTML = `
                <div>📍 ${p.location}</div>
                <div>🛏 ${p.bedrooms} bedrooms</div>
                <div>💷 £${p.price_per_month}/month</div>
                <div>${p.furnished ? "✅ Furnished" : "🚫 Furnished"} · ${p.has_garden ? "🌿 Garden" : "—"} · ${p.parking ? "🚗 Parking" : "—"}</div>
                ${p.score != null ? `<div>⭐ Match score: ${p.score}</div>` : ""}
            `;

            const linkWrap = document.createElement("div");
            linkWrap.className = "mt-2 flex justify-end";

            if (p.url) {
                const a = document.createElement("a");
                a.href = p.url;
                a.target = "_blank";
                a.rel = "noopener noreferrer";
                a.className =
                    "inline-flex items-center gap-1 text-[11px] px-2 py-1 rounded-lg bg-emerald-500/90 text-slate-900 font-semibold hover:bg-emerald-400";
                a.textContent = "View details";
                linkWrap.appendChild(a);
            }

            card.appendChild(title);
            card.appendChild(meta);
            card.appendChild(linkWrap);
            gridWrapper.appendChild(card);
        });

        messagesEl.appendChild(gridWrapper);
        scrollToBottom();
    }

    function renderBotResponse(data) {
        if (!data) return;

        const text = data.text || "";
        createMessageBubble(text, "bot");

        renderOptions(data.options || []);
        renderProperties(data.properties || []);
    }

    function sendUserMessage(value, displayLabel = null) {
        const textToSend = value || inputEl.value.trim();
        if (!textToSend || !ws || ws.readyState !== WebSocket.OPEN) return;

        const labelForUi = displayLabel || textToSend;
        createMessageBubble(labelForUi, "user");
        clearOptions();
        ws.send(JSON.stringify({ text: textToSend }));

        if (!displayLabel) {
            inputEl.value = "";
        }
    }

    // Form submit (manual typing)
    if (formEl) {
        formEl.addEventListener("submit", (e) => {
            e.preventDefault();
            sendUserMessage();
        });
    }

    // Example prompts (right sidebar)
    document.querySelectorAll(".example-prompt").forEach((btn) => {
        btn.addEventListener("click", () => {
            const prompt = btn.getAttribute("data-prompt");
            if (!prompt) return;
            inputEl.value = prompt;
            inputEl.focus();
        });
    });

    // Init WebSocket
    connectWebSocket();
});
