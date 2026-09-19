(function () {
    "use strict";

    const STORAGE_KEY = "aala2026-banquet-lucky-draw-v2";
    const COLOURS = ["#ee8a13", "#a7c519", "#11a9bd", "#762181", "#0d886c"];
    const AFFILIATIONS = [
        "Duolingo", "Duolingo", "Pearson", "Pearson", "The Language Training & Testing Center (LTTC)", "The Language Training & Testing Center (LTTC)", "The Language Training & Testing Center (LTTC)", "The Language Training & Testing Center (LTTC)", "The Language Training & Testing Center (LTTC)", "The Language Training & Testing Center (LTTC)", "The Language Training & Testing Center (LTTC)", "Beijing Technology and Business University", "Cambridge University Press & Assessment", "Cambridge University Press & Assessment", "Chongqing University", "Chongqing University", "Chongqing University", "Chulalongkorn University", "Chulalongkorn University Language Institute", "City University of Macau", "City University of Macau", "City University of Macau", "City University of Macau", "East China Normal University", "Fudan University", "Fudan University", "Fuzhou University", "Hansung University", "Hong Kong Polytechnic University", "Hunan University", "Independent project \"Oh, my Chinese\"", "Indiana University", "Jinan University", "Konkuk University", "Macao Polytechnic University", "Nanyang Technological University", "NIT Warangal", "Ochanomizu University", "Oxford University Press", "Oxford University Press", "Seoul National University", "Shanghai Baoshan Huayao High School", "Shanghai International Studies University", "Shanghai Jiao Tong University", "Shanghai Jiao Tong University", "Shanghai University of International Business and Economics", "The Hong Kong Polytechnic University", "The University of Hong Kong", "Tokyo University of Foreign Studies.", "Tsinghua University", "Universiti Sains Malaysia", "Universiti Sains Malaysia", "Universiti Teknologi MARA", "University of Hong Kong", "University of Hong Kong", "University of Hong Kong", "University of Illinois Urbana-Champaign", "University of Illinois Urbana-Champaign", "University of Macau", "University of Macau", "University of Ottawa", "University of Southampton", "University of Southampton", "University of Southampton", "Waseda University", "Western Washington University", "",
        "City University of Macau", "City University of Macau", "City University of Macau", "City University of Macau", "Macao Polytechnic University", "University of Macau", "University of Macau", "University of Macau",
        "Ontario Institute for Studies in Education, University of Toronto", "University of Southampton", "University of Illinois Urbana-Champaign", "Oslo Metropolitan University", "South China Business College of Guangdong University of Foreign Studies", "University of Oxford", "Konkuk University Glocal Campus",
        "Nanyang Technological University", "Ocean University of China", "Seoul National University", "Shanghai International Studies University", "University of Melbourne", "VNU University of Languages and International Studies", "Zhejiang University", "Federation University Australia", "Nanyang Technological University", "Zhejiang University",
        "Educational Testing Service (ETS)", "Educational Testing Service (ETS)", "LanguageCert", "Prince Education Co.,Ltd.", "Prince Education Co.,Ltd.", "Shenzhen Explore Future Education Consulting Co., Ltd.", "Shenzhen Explore Future Education Consulting Co., Ltd.", "Pearson", "British Council", "British Council", "Cambridge University Press & Assessment / ALTE", "City University of Macau", "Victoria University of Wellington",
        "Université Laval",
        "Guangzhou Gizzai Technology Co.,Ltd.", "Guangzhou Gizzai Technology Co.,Ltd.", "Guangzhou Gizzai Technology Co.,Ltd.", "Guangzhou Gizzai Technology Co.,Ltd."
    ];
    const PARTICIPANTS = [
        ["Alina A. von Davier", "Paid attendee · Duolingo"], ["Geoff LaFlair", "Paid attendee · Duolingo"], ["Ellen Barrow", "Paid attendee · Pearson"], ["Sarah Hughes", "Paid attendee · Pearson"], ["Aaron Cheng-Yao Liu", "Paid attendee · LTTC"], ["Anita Chunwen Lin", "Paid attendee · LTTC"], ["Hsin-Ying Li", "Paid attendee · LTTC"], ["Kelvin Chien Min Kuo", "Paid attendee · LTTC"], ["Rachel Yifen Wu", "Paid attendee · LTTC"], ["Stan Tsuo Lin Chiu", "Paid attendee · LTTC"], ["Vivian Wen-Chi Liu", "Paid attendee · LTTC"], ["Ling Gan", "Paid attendee"], ["Brigita Séguis", "Paid attendee"], ["Hye-won Lee", "Paid attendee"], ["Shiyao He", "Paid attendee"], ["Xiangdong Gu", "Paid attendee"], ["Yuhang Chen", "Paid attendee"], ["Jirada Wudthayagorn", "Paid attendee"], ["Sasithorn Limgomolvilas", "Paid attendee"], ["He Yang", "Paid attendee"], ["Huimin Duan", "Paid attendee"], ["Zhaorui Xie", "Paid attendee"], ["Zihan Sun", "Paid attendee"], ["Xiaoxian Guan", "Paid attendee"], ["Jiming Zhou", "Paid attendee"], ["Yi Ding", "Paid attendee"], ["Fanrong Weng", "Paid attendee"], ["Il-Sun, Hyun", "Paid attendee"], ["Alan Urmston", "Paid attendee"], ["Jincheng Wu", "Paid attendee"], ["Daria Zhigulskaia", "Paid attendee"], ["Sun-Young Shin", "Paid attendee"], ["Wen Zhao", "Paid attendee"], ["Huidan Zheng", "Paid attendee"], ["Haoming Lin", "Paid attendee"], ["Yun-Yee Cheong", "Paid attendee"], ["Gottimukkala Amrutha", "Paid attendee"], ["David Allen", "Paid attendee"], ["Nathaniel Owen", "Paid attendee"], ["Wenjun (Elyse) Ding", "Paid attendee"], ["Minkyung Kim", "Paid attendee"], ["Xinquan Liu", "Paid attendee"], ["Yuyang Cai", "Paid attendee"], ["Hua Wang", "Paid attendee"], ["Qi Wang", "Paid attendee"], ["Wei Jie", "Paid attendee"], ["Sihui (Echo) Ke", "Paid attendee"], ["Simon Boynton", "Paid attendee"], ["Matthew Miller", "Paid attendee"], ["Wanqing Li", "Paid attendee"], ["Alla Baksh Mohamed Ayub Khan", "Paid attendee"], ["Pingping Liu", "Paid attendee"], ["Norhaslinda Hassan", "Paid attendee"], ["Michelle Reyes Raquel", "Paid attendee"], ["Nicholas Yui Chit Mo", "Paid attendee"], ["Wim Isidoor Lea Vergult", "Paid attendee"], ["Huiying Cai", "Paid attendee"], ["Xinyi Ma", "Paid attendee"], ["Keke Xing", "Paid attendee"], ["Qiqi Han", "Paid attendee"], ["Coral Yiwei Qin", "Paid attendee"], ["Jia Li", "Paid attendee"], ["Yuchen Xing", "Paid attendee"], ["Yuxuan Yang", "Paid attendee"], ["Rachel Yuan Xue", "Paid attendee"], ["Xiaomeng Li", "Paid attendee"], ["Jing LI", "Paid attendee"],
        ["Liying Cheng", "Committee"], ["April Jiawei Zhang", "Committee"], ["Jiayi Li", "Committee"], ["Shelly Xueting Ye", "Committee"], ["Wei Wei", "Committee"], ["Cecilia Guanfang Zhao", "Committee"], ["Matthew Wallace", "Committee"], ["Qin Xie", "Committee"],
        ["Eunice Eunhee Jang", "Speaker"], ["Ying Zheng", "Speaker"], ["Xun Yan", "Speaker"], ["Dina Tsagari", "Workshop facilitator"], ["Quan Zhang", "Workshop facilitator"], ["Yuanyue Hao", "Workshop facilitator"], ["Gwan-Hyeok Im", "Workshop facilitator"],
        ["Limei Zhang", "Executive Board"], ["Ying Chen", "Executive Board"], ["Yong-won Lee", "Executive Board"], ["Mingwei Pan", "Executive Board"], ["Jason Fan", "Executive Board"], ["Nguyen Thi Ngoc Quynh", "Executive Board"], ["Shangchao Min", "Executive Board"], ["Shengkai Yin", "Award winner"], ["Han Yining", "Award winner"], ["Yanxin Wang", "Award winner"],
        ["Mikyung Kim Wolf", "Guest / sponsor · ETS"], ["Saerhim Oh", "Guest / sponsor · ETS"], ["Leda Lampropoulou", "Guest / sponsor · LanguageCert"], ["Chelsea Du", "Guest / sponsor · 中研院"], ["Phyllis Lu", "Guest / sponsor · 中研院"], ["Alicia Yiyin Li", "Guest / sponsor · 人才协会"], ["Yinshan Li", "Guest / sponsor · 人才协会"], ["Felix Leong", "Guest / sponsor · Pearson"], ["Barry Edward O'Sullivan", "Guest / sponsor · BC"], ["Meha Dayal", "Guest / sponsor · BC"], ["Nick Saville", "Guest / sponsor · ALTE"], ["Antony Kunnan", "Guest / sponsor"], ["Peter Yongqi Gu", "Guest / sponsor"],
        ["Shahrzad Saif", "Paid attendee"],
        ["Zhuolei li", "Paid attendee"], ["Lucy Lyu", "Paid attendee"], ["Yi Cun Deng", "Paid attendee"], ["Zehao li", "Paid attendee"]
    ].map(([name], id) => ({ id, name, affiliation: AFFILIATIONS[id] || "" }));

    const drawButton = document.getElementById("draw-button");
    const resetButton = document.getElementById("reset-button");
    const drawSetup = document.getElementById("draw-setup");
    const winnerLimitInput = document.getElementById("winner-limit");
    const setWinnerLimitButton = document.getElementById("set-winner-limit");
    const winnerLimitHint = document.getElementById("winner-limit-hint");
    const candidateName = document.getElementById("candidate-name");
    const candidateAffiliation = document.getElementById("candidate-affiliation");
    const drawStatus = document.getElementById("draw-status");
    const lotteryMachine = document.getElementById("lottery-machine");
    const winnerList = document.getElementById("winner-list");
    const winnerCount = document.getElementById("winner-count");
    const winnersEmpty = document.getElementById("winners-empty");
    const eligibleCount = document.getElementById("eligible-count");
    const rosterContent = document.getElementById("roster-content");
    const nameStreamTracks = document.querySelectorAll(".name-stream-track");
    let isDrawing = false;
    let { drawLimit, winners } = loadDrawState();

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

    function loadDrawState() {
        try {
            const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
            if (!stored || typeof stored !== "object" || Array.isArray(stored)) {
                return { drawLimit: null, winners: [] };
            }
            const storedLimit = stored.drawLimit;
            const storedWinners = stored.winners;
            if (!Number.isInteger(storedLimit) || storedLimit < 1 || storedLimit > PARTICIPANTS.length || !Array.isArray(storedWinners) || storedWinners.length > storedLimit) {
                return { drawLimit: null, winners: [] };
            }
            const unique = new Set(storedWinners);
            if (unique.size !== storedWinners.length || storedWinners.some((id) => !Number.isInteger(id) || !PARTICIPANTS[id])) {
                return { drawLimit: null, winners: [] };
            }
            return { drawLimit: storedLimit, winners: storedWinners };
        } catch {
            return { drawLimit: null, winners: [] };
        }
    }

    function saveDrawState() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({ drawLimit, winners }));
    }

    function hasDrawLimit() {
        return Number.isInteger(drawLimit) && drawLimit >= 1 && drawLimit <= PARTICIPANTS.length;
    }

    function remainingParticipants() {
        const selected = new Set(winners);
        return PARTICIPANTS.filter((participant) => !selected.has(participant.id));
    }

    function updateInterface() {
        const remaining = remainingParticipants();
        const configured = hasDrawLimit();
        eligibleCount.textContent = String(remaining.length);
        winnerCount.textContent = configured ? `${winners.length} / ${drawLimit}` : "Not set";
        winnerLimitInput.max = String(PARTICIPANTS.length);
        winnerLimitInput.disabled = configured || isDrawing;
        setWinnerLimitButton.disabled = configured || isDrawing;
        resetButton.disabled = isDrawing || !configured;
        if (configured) {
            winnerLimitInput.value = String(drawLimit);
            winnerLimitHint.textContent = "Winner count is locked until the draw is reset.";
        } else {
            winnerLimitHint.textContent = `Enter a whole number from 1 to ${PARTICIPANTS.length} before the first draw.`;
        }

        winnerList.replaceChildren();
        winners.forEach((winnerId, index) => {
            const participant = PARTICIPANTS[winnerId];
            const item = document.createElement("li");
            item.className = "winner-card";
            item.style.setProperty("--winner-color", COLOURS[index % COLOURS.length]);
            const number = document.createElement("span");
            number.className = "winner-number";
            number.textContent = String(index + 1);
            const detail = document.createElement("span");
            const name = document.createElement("strong");
            name.className = "winner-name";
            name.textContent = participant.name;
            detail.append(name);
            if (participant.affiliation) {
                const affiliation = document.createElement("span");
                affiliation.className = "winner-affiliation";
                affiliation.textContent = participant.affiliation;
                detail.append(affiliation);
            }
            item.append(number, detail);
            winnerList.append(item);
        });
        winnersEmpty.hidden = winners.length > 0;

        if (!configured) {
            drawButton.disabled = true;
            drawButton.textContent = "Set the number of winners";
            if (!isDrawing) {
                candidateName.textContent = "Ready?";
                candidateAffiliation.textContent = "Set the number of winners first";
                drawStatus.textContent = "Set the number of winners to begin the draw.";
            }
            return;
        }

        if (winners.length === drawLimit) {
            drawButton.disabled = true;
            drawButton.textContent = `All ${drawLimit} winners have been drawn`;
            drawStatus.textContent = `Congratulations to all ${drawLimit} lucky-draw winners.`;
            if (!isDrawing) {
                candidateName.textContent = "Congratulations!";
                candidateAffiliation.textContent = `${drawLimit} winner${drawLimit === 1 ? "" : "s"} selected`;
            }
            return;
        }

        drawButton.disabled = isDrawing;
        drawButton.textContent = isDrawing ? "Drawing…" : `Draw winner ${winners.length + 1} of ${drawLimit}`;
        if (!isDrawing && winners.length === 0) {
            candidateName.textContent = "Ready?";
            candidateAffiliation.textContent = `${drawLimit} winner${drawLimit === 1 ? "" : "s"} to be drawn`;
        } else if (!isDrawing) {
            const latestWinner = PARTICIPANTS[winners[winners.length - 1]];
            candidateName.textContent = latestWinner.name;
            candidateAffiliation.textContent = latestWinner.affiliation;
            drawStatus.textContent = `${winners.length} of ${drawLimit} winner${drawLimit === 1 ? "" : "s"} selected. Draw winner ${winners.length + 1} when ready.`;
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
        if (isDrawing || !hasDrawLimit() || winners.length >= drawLimit) return;
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
            candidateAffiliation.textContent = candidate.affiliation;
        }, 85);

        window.setTimeout(() => {
            window.clearInterval(nameTimer);
            const winner = remaining[secureIndex(remaining.length)];
            winners.push(winner.id);
            saveDrawState();
            candidateName.textContent = winner.name;
            candidateAffiliation.textContent = winner.affiliation;
            lotteryMachine.classList.remove("is-drawing");
            lotteryMachine.classList.add("has-winner");
            drawStatus.textContent = `Winner ${winners.length} goes to ${winner.name}. Congratulations!`;
            isDrawing = false;
            updateInterface();
            makeConfetti();
        }, 3400);
    }

    function configureDraw(event) {
        event.preventDefault();
        if (isDrawing || hasDrawLimit()) return;
        const requestedLimit = Number(winnerLimitInput.value);
        if (!Number.isInteger(requestedLimit) || requestedLimit < 1 || requestedLimit > PARTICIPANTS.length) {
            winnerLimitInput.setCustomValidity(`Enter a whole number from 1 to ${PARTICIPANTS.length}.`);
            winnerLimitInput.reportValidity();
            return;
        }
        winnerLimitInput.setCustomValidity("");
        drawLimit = requestedLimit;
        winners = [];
        saveDrawState();
        candidateName.textContent = "Ready?";
        candidateAffiliation.textContent = `${drawLimit} winner${drawLimit === 1 ? "" : "s"} to be drawn`;
        drawStatus.textContent = `Draw ready: ${drawLimit} winner${drawLimit === 1 ? "" : "s"} will be selected.`;
        lotteryMachine.classList.remove("has-winner", "is-drawing");
        updateInterface();
        drawButton.focus();
    }

    function resetDraw() {
        if (isDrawing || !hasDrawLimit()) return;
        if (!window.confirm("Reset this draw and choose a new number of winners? All selected winners on this device will be cleared.")) return;
        winners = [];
        drawLimit = null;
        localStorage.removeItem(STORAGE_KEY);
        winnerLimitInput.value = "";
        candidateName.textContent = "Ready?";
        candidateAffiliation.textContent = "Set the number of winners first";
        drawStatus.textContent = "Set the number of winners to begin the draw.";
        lotteryMachine.classList.remove("has-winner", "is-drawing");
        updateInterface();
        winnerLimitInput.focus();
    }

    function renderRoster() {
        const list = document.createElement("ul");
        list.className = "roster-list";
        [...PARTICIPANTS].sort((first, second) => first.name.localeCompare(second.name)).forEach((participant) => {
            const item = document.createElement("li");
            item.className = "roster-person";
            const name = document.createElement("strong");
            name.className = "roster-person-name";
            name.textContent = participant.name;
            item.append(name);
            if (participant.affiliation) {
                const affiliation = document.createElement("span");
                affiliation.className = "roster-person-affiliation";
                affiliation.textContent = participant.affiliation;
                item.append(affiliation);
            }
            list.append(item);
        });
        rosterContent.append(list);
    }

    function renderNameStreams() {
        nameStreamTracks.forEach((track, trackIndex) => {
            const offset = Math.floor((PARTICIPANTS.length / nameStreamTracks.length) * trackIndex);
            const rotatedParticipants = [...PARTICIPANTS.slice(offset), ...PARTICIPANTS.slice(0, offset)];
            [...rotatedParticipants, ...rotatedParticipants].forEach((participant) => {
                const item = document.createElement("span");
                item.className = "name-stream-item";
                const name = document.createElement("span");
                name.className = "name-stream-name";
                name.textContent = participant.name;
                item.append(name);
                if (participant.affiliation) {
                    const affiliation = document.createElement("span");
                    affiliation.className = "name-stream-affiliation";
                    affiliation.textContent = `· ${participant.affiliation}`;
                    item.append(affiliation);
                }
                track.append(item);
            });
        });
    }

    drawSetup.addEventListener("submit", configureDraw);
    winnerLimitInput.addEventListener("input", () => winnerLimitInput.setCustomValidity(""));
    drawButton.addEventListener("click", drawWinner);
    resetButton.addEventListener("click", resetDraw);
    renderRoster();
    renderNameStreams();
    updateInterface();
}());
