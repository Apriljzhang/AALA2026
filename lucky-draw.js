(function () {
    "use strict";

    const DRAW_LIMIT = 5;
    const STORAGE_KEY = "aala2026-banquet-lucky-draw-v1";
    const COLOURS = ["#ee8a13", "#a7c519", "#11a9bd", "#762181", "#0d886c"];
    const PARTICIPANTS = [
        ["Alina A. von Davier", "Paid attendee · Duolingo"], ["Geoff LaFlair", "Paid attendee · Duolingo"], ["Ellen Barrow", "Paid attendee · Pearson"], ["Sarah Hughes", "Paid attendee · Pearson"], ["Aaron Cheng-Yao Liu", "Paid attendee · LTTC"], ["Anita Chunwen Lin", "Paid attendee · LTTC"], ["Hsin-Ying Li", "Paid attendee · LTTC"], ["Kelvin Chien Min Kuo", "Paid attendee · LTTC"], ["Rachel Yifen Wu", "Paid attendee · LTTC"], ["Stan Tsuo Lin Chiu", "Paid attendee · LTTC"], ["Vivian Wen-Chi Liu", "Paid attendee · LTTC"], ["Ling Gan", "Paid attendee"], ["Brigita Séguis", "Paid attendee"], ["Hye-won Lee", "Paid attendee"], ["Shiyao He", "Paid attendee"], ["Xiangdong Gu", "Paid attendee"], ["Yuhang Chen", "Paid attendee"], ["Jirada Wudthayagorn", "Paid attendee"], ["Sasithorn Limgomolvilas", "Paid attendee"], ["He Yang", "Paid attendee"], ["Huimin Duan", "Paid attendee"], ["Zhaorui Xie", "Paid attendee"], ["Zihan Sun", "Paid attendee"], ["Xiaoxian Guan", "Paid attendee"], ["Jiming Zhou", "Paid attendee"], ["Yi Ding", "Paid attendee"], ["Fanrong Weng", "Paid attendee"], ["Il-Sun, Hyun", "Paid attendee"], ["Alan Urmston", "Paid attendee"], ["Jincheng Wu", "Paid attendee"], ["Daria Zhigulskaia", "Paid attendee"], ["Sun-Young Shin", "Paid attendee"], ["Wen Zhao", "Paid attendee"], ["Huidan Zheng", "Paid attendee"], ["Haoming Lin", "Paid attendee"], ["Yun-Yee Cheong", "Paid attendee"], ["Gottimukkala Amrutha", "Paid attendee"], ["David Allen", "Paid attendee"], ["Nathaniel Owen", "Paid attendee"], ["Wenjun (Elyse) Ding", "Paid attendee"], ["Minkyung Kim", "Paid attendee"], ["Xinquan Liu", "Paid attendee"], ["Yuyang Cai", "Paid attendee"], ["Hua Wang", "Paid attendee"], ["Qi Wang", "Paid attendee"], ["Wei Jie", "Paid attendee"], ["Sihui (Echo) Ke", "Paid attendee"], ["Simon Boynton", "Paid attendee"], ["Matthew Miller", "Paid attendee"], ["Wanqing Li", "Paid attendee"], ["Alla Baksh Mohamed Ayub Khan", "Paid attendee"], ["Pingping Liu", "Paid attendee"], ["Norhaslinda Hassan", "Paid attendee"], ["Michelle Reyes Raquel", "Paid attendee"], ["Nicholas Yui Chit Mo", "Paid attendee"], ["Wim Isidoor Lea Vergult", "Paid attendee"], ["Huiying Cai", "Paid attendee"], ["Xinyi Ma", "Paid attendee"], ["Keke Xing", "Paid attendee"], ["Qiqi Han", "Paid attendee"], ["Coral Yiwei Qin", "Paid attendee"], ["Jia Li", "Paid attendee"], ["Yuchen Xing", "Paid attendee"], ["Yuxuan Yang", "Paid attendee"], ["Rachel Yuan Xue", "Paid attendee"], ["Xiaomeng Li", "Paid attendee"], ["Jing LI", "Paid attendee"],
        ["Liying Cheng", "Committee"], ["April Jiawei Zhang", "Committee"], ["Jiayi Li", "Committee"], ["Shelly Xueting Ye", "Committee"], ["Wei Wei", "Committee"], ["Cecilia Guanfang Zhao", "Committee"], ["Matthew Wallace", "Committee"], ["Qin Xie", "Committee"],
        ["Eunice Eunhee Jang", "Speaker"], ["Ying Zheng", "Speaker"], ["Xun Yan", "Speaker"], ["Dina Tsagari", "Workshop facilitator"], ["Quan Zhang", "Workshop facilitator"], ["Yuanyue Hao", "Workshop facilitator"], ["Gwan-Hyeok Im", "Workshop facilitator"],
        ["Limei Zhang", "Executive Board"], ["Ying Chen", "Executive Board"], ["Yong-won Lee", "Executive Board"], ["Mingwei Pan", "Executive Board"], ["Jason Fan", "Executive Board"], ["Nguyen Thi Ngoc Quynh", "Executive Board"], ["Shangchao Min", "Executive Board"], ["Shengkai Yin", "Award winner"], ["Han Yining", "Award winner"], ["Yanxin Wang", "Award winner"],
        ["Mikyung Kim Wolf", "Guest / sponsor · ETS"], ["Saerhim Oh", "Guest / sponsor · ETS"], ["Leda Lampropoulou", "Guest / sponsor · LanguageCert"], ["Chelsea Du", "Guest / sponsor · 中研院"], ["Phyllis Lu", "Guest / sponsor · 中研院"], ["Alicia Yiyin Li", "Guest / sponsor · 人才协会"], ["Yinshan Li", "Guest / sponsor · 人才协会"], ["Felix Leong", "Guest / sponsor · Pearson"], ["Barry Edward O'Sullivan", "Guest / sponsor · BC"], ["Meha Dayal", "Guest / sponsor · BC"], ["Nick Saville", "Guest / sponsor · ALTE"], ["Antony Kunnan", "Guest / sponsor"], ["Peter Yongqi Gu", "Guest / sponsor"]
    ].map(([name, group], id) => ({ id, name, group }));

    const drawButton = document.getElementById("draw-button");
    const resetButton = document.getElementById("reset-button");
    const candidateName = document.getElementById("candidate-name");
    const candidateGroup = document.getElementById("candidate-group");
    const drawStatus = document.getElementById("draw-status");
    const lotteryMachine = document.getElementById("lottery-machine");
    const winnerList = document.getElementById("winner-list");
    const winnerCount = document.getElementById("winner-count");
    const winnersEmpty = document.getElementById("winners-empty");
    const eligibleCount = document.getElementById("eligible-count");
    const rosterContent = document.getElementById("roster-content");
    let isDrawing = false;
    let winners = loadWinners();

    function secureIndex(max) {
        if (max <= 1) return 0;
        if (!window.crypto?.getRandomValues) return Math.floor(Math.random() * max);
        const values = new Uint32Array(1);
        const upperLimit = Math.floor(0x100000000 / max) * max;
        do {
            window.crypto.getRandomValues(values);
        } while (values[0] >= upperLimit);
        return values[0] % max;
    }

    function loadWinners() {
        try {
            const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
            if (!Array.isArray(stored) || stored.length > DRAW_LIMIT) return [];
            const unique = new Set(stored);
            if (unique.size !== stored.length || stored.some((id) => !PARTICIPANTS[id])) return [];
            return stored;
        } catch {
            return [];
        }
    }

    function saveWinners() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(winners));
    }

    function remainingParticipants() {
        const selected = new Set(winners);
        return PARTICIPANTS.filter((participant) => !selected.has(participant.id));
    }

    function updateInterface() {
        const remaining = remainingParticipants();
        eligibleCount.textContent = String(remaining.length);
        winnerCount.textContent = `${winners.length} / ${DRAW_LIMIT}`;
        winnerList.replaceChildren();
        winners.forEach((winnerId, index) => {
            const participant = PARTICIPANTS[winnerId];
            const item = document.createElement("li");
            item.className = "winner-card";
            item.style.setProperty("--winner-color", COLOURS[index]);
            const number = document.createElement("span");
            number.className = "winner-number";
            number.textContent = String(index + 1);
            const detail = document.createElement("span");
            const name = document.createElement("strong");
            name.className = "winner-name";
            name.textContent = participant.name;
            const group = document.createElement("span");
            group.className = "winner-group";
            group.textContent = participant.group;
            detail.append(name, group);
            item.append(number, detail);
            winnerList.append(item);
        });
        winnersEmpty.hidden = winners.length > 0;

        if (winners.length === DRAW_LIMIT) {
            drawButton.disabled = true;
            drawButton.textContent = "All five prizes have been drawn";
            drawStatus.textContent = "Congratulations to all five lucky-draw winners.";
            if (!isDrawing) {
                candidateName.textContent = "Congratulations!";
                candidateGroup.textContent = "Five prizes have been awarded";
            }
            return;
        }

        drawButton.disabled = isDrawing;
        drawButton.textContent = isDrawing ? "Drawing…" : `Draw prize ${winners.length + 1} of ${DRAW_LIMIT}`;
        if (!isDrawing && winners.length === 0) {
            candidateName.textContent = "Ready?";
            candidateGroup.textContent = "Five prizes to be drawn";
        }
    }

    function makeConfetti() {
        const colours = ["#ee8a13", "#a7c519", "#11a9bd", "#762181", "#0d886c", "#ffffff"];
        for (let index = 0; index < 70; index += 1) {
            const piece = document.createElement("span");
            piece.className = "confetti";
            piece.style.left = `${secureIndex(100)}vw`;
            piece.style.background = colours[secureIndex(colours.length)];
            piece.style.setProperty("--drift", `${secureIndex(220) - 110}px`);
            piece.style.setProperty("--spin", `${secureIndex(900) - 450}deg`);
            piece.style.setProperty("--fall-time", `${1900 + secureIndex(1500)}ms`);
            piece.style.borderRadius = secureIndex(2) ? "2px" : "50%";
            document.body.append(piece);
            piece.addEventListener("animationend", () => piece.remove(), { once: true });
        }
    }

    function drawWinner() {
        if (isDrawing || winners.length >= DRAW_LIMIT) return;
        const remaining = remainingParticipants();
        if (!remaining.length) return;

        isDrawing = true;
        updateInterface();
        lotteryMachine.classList.remove("has-winner");
        lotteryMachine.classList.add("is-drawing");
        drawStatus.textContent = "Mixing the eligible attendee list…";

        const nameTimer = window.setInterval(() => {
            const candidate = remaining[secureIndex(remaining.length)];
            candidateName.textContent = candidate.name;
            candidateGroup.textContent = candidate.group;
        }, 85);

        window.setTimeout(() => {
            window.clearInterval(nameTimer);
            const winner = remaining[secureIndex(remaining.length)];
            winners.push(winner.id);
            saveWinners();
            candidateName.textContent = winner.name;
            candidateGroup.textContent = winner.group;
            lotteryMachine.classList.remove("is-drawing");
            lotteryMachine.classList.add("has-winner");
            drawStatus.textContent = `Prize ${winners.length} goes to ${winner.name}. Congratulations!`;
            isDrawing = false;
            updateInterface();
            makeConfetti();
        }, 3400);
    }

    function resetDraw() {
        if (isDrawing || !winners.length) return;
        if (!window.confirm("Reset all selected winners on this device? This cannot be undone.")) return;
        winners = [];
        localStorage.removeItem(STORAGE_KEY);
        candidateName.textContent = "Ready?";
        candidateGroup.textContent = "Five prizes to be drawn";
        drawStatus.textContent = "Ready to draw from the eligible attendee list.";
        lotteryMachine.classList.remove("has-winner", "is-drawing");
        updateInterface();
    }

    function renderRoster() {
        const groups = ["Paid attendee", "Committee", "Speaker", "Workshop facilitator", "Executive Board", "Award winner", "Guest / sponsor"];
        groups.forEach((groupName) => {
            const group = document.createElement("section");
            group.className = "roster-group";
            const title = document.createElement("h3");
            const people = PARTICIPANTS.filter((participant) => participant.group.startsWith(groupName));
            title.textContent = `${groupName} (${people.length})`;
            const list = document.createElement("ul");
            people.forEach((participant) => {
                const item = document.createElement("li");
                item.textContent = participant.name;
                list.append(item);
            });
            group.append(title, list);
            rosterContent.append(group);
        });
    }

    drawButton.addEventListener("click", drawWinner);
    resetButton.addEventListener("click", resetDraw);
    renderRoster();
    updateInterface();
}());
