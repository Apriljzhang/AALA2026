(function () {
    "use strict";

    const data = window.AALA_PROGRAM;
    const legendRoot = document.getElementById("programLegend");
    const tabsRoot = document.getElementById("dayTabs");
    const panelsRoot = document.getElementById("dayPanels");

    function element(tag, className, text) {
        const node = document.createElement(tag);
        if (className) node.className = className;
        if (text !== undefined) node.textContent = text;
        return node;
    }

    function categoryClass(category) {
        return `category-${category}`;
    }

    function displayTime(value) {
        return value.replace(/^0/, "");
    }

    const roomOrder = [
        "Culture Centre Room 1",
        "Culture Centre Room 2",
        "HG01",
        "HG02",
        "HG03",
        "L205",
        "L206",
        "L207",
        "L305",
        "L306",
        "L307",
    ];

    function roomRank(event) {
        const index = roomOrder.indexOf(event.room);
        return index < 0 ? roomOrder.length : index;
    }

    function authorText(author) {
        return author.affiliation ? `${author.name} (${author.affiliation})` : author.name;
    }

    function makeExpandMark() {
        const mark = element("span", "expand-mark");
        mark.setAttribute("aria-hidden", "true");
        return mark;
    }

    function makeTitleContent(event) {
        const row = element("span", "session-title-row");
        const text = element("span", "session-title-text");
        if (event.id) text.append(element("em", "submission-id", event.id));
        text.append(element("strong", "session-title", event.title));
        row.append(text);
        return row;
    }

    function makeTitle(event) {
        if (!event.abstract) return makeTitleContent(event);
        const details = element("details", "title-details");
        const summary = element("summary");
        const content = makeTitleContent(event);
        content.append(makeExpandMark());
        summary.append(content);
        const panel = element("div", "abstract-panel");
        panel.append(element("span", "abstract-label", "Abstract"));
        panel.append(element("p", "", event.abstract));
        details.append(summary, panel);
        return details;
    }

    function makeAuthors(authors) {
        if (!authors || !authors.length) return null;
        const list = element("ul", "authors");
        authors.forEach((author) => {
            const item = element("li");
            if (author.bio) {
                const details = element("details", "author-details");
                const summary = element("summary");
                summary.append(element("span", "author-summary-text", authorText(author)), makeExpandMark());
                const panel = element("div", "bio-panel");
                panel.append(element("span", "bio-label", "Biography"));
                panel.append(element("p", "", author.bio));
                details.append(summary, panel);
                item.append(details);
            } else {
                item.append(element("span", "author-line", authorText(author)));
            }
            list.append(item);
        });
        return list;
    }

    function makeMeta(event) {
        const meta = element("p", "session-meta");
        const type = element("span", "session-type");
        type.append(element("span", "legend-swatch"), document.createTextNode(event.categoryLabel));
        meta.append(type);
        meta.append(element("span", "session-time", `${displayTime(event.start)}–${displayTime(event.end)}`));
        if (event.room) meta.append(element("span", "session-room", `Venue: ${event.room}`));
        return meta;
    }

    function makeSession(event, extraClass) {
        const card = element("article", `session-card ${categoryClass(event.category)}${extraClass ? ` ${extraClass}` : ""}`);
        card.append(makeMeta(event), makeTitle(event));
        if (event.note) card.append(element("p", "session-note", event.note));
        const authors = makeAuthors(event.authors);
        if (authors) card.append(authors);
        return card;
    }

    function makePosterBand(event) {
        const band = element("section", `poster-band ${categoryClass("poster")}`);
        band.append(makeMeta(event));
        band.append(element("strong", "poster-band-title", event.title));
        if (event.abstract) band.append(element("p", "poster-band-intro", event.abstract));
        const list = element("div", "poster-list");
        event.posters.forEach((poster) => list.append(makeSession(poster, "poster-item")));
        band.append(list);
        return band;
    }

    function makeDayPanel(day, index) {
        const panel = element("section", "day-panel");
        panel.id = `panel-${day.key}`;
        panel.setAttribute("role", "tabpanel");
        panel.setAttribute("aria-labelledby", `tab-${day.key}`);
        panel.hidden = index !== 0;

        const heading = element("header", "day-heading");
        const dayLabel = day.key === "sep19" ? "Day 1 - 19 September" : day.key === "sep20" ? "Day 2 - 20 September" : `${day.weekday}, ${day.date}`;
        heading.append(element("h2", "", dayLabel));
        heading.append(element("p", "", day.subtitle));
        panel.append(heading);

        const timeline = element("div", "timeline");
        const posterEvents = day.events.filter((event) => event.posters);
        const groups = new Map();
        day.events.filter((event) => !event.posters).forEach((event) => {
            if (!groups.has(event.start)) groups.set(event.start, []);
            groups.get(event.start).push(event);
        });

        groups.forEach((events, start) => {
            const group = element("section", "time-group");
            group.append(element("h3", "time-marker", displayTime(start)));
            const eventList = element("div", `time-events${events.length > 1 ? " concurrent-grid" : " single-event"}`);
            events.sort((a, b) => roomRank(a) - roomRank(b) || a.room.localeCompare(b.room));
            events.forEach((event) => eventList.append(makeSession(event)));
            group.append(eventList);
            timeline.append(group);
        });
        if (posterEvents.length) {
            const group = element("section", "time-group poster-time-group");
            group.append(element("h3", "time-marker", "Posters"));
            const eventList = element("div", "time-events poster-events");
            posterEvents.forEach((event) => eventList.append(makePosterBand(event)));
            group.append(eventList);
            timeline.append(group);
        }
        panel.append(timeline);
        return panel;
    }

    function selectDay(index, updateHash) {
        const tabs = [...tabsRoot.querySelectorAll("[role='tab']")];
        const panels = [...panelsRoot.querySelectorAll("[role='tabpanel']")];
        tabs.forEach((tab, tabIndex) => {
            const active = tabIndex === index;
            tab.setAttribute("aria-selected", String(active));
            tab.tabIndex = active ? 0 : -1;
            panels[tabIndex].hidden = !active;
        });
        if (updateHash) history.replaceState(null, "", `#${data.days[index].key}`);
    }

    function render() {
        if (!data || !legendRoot || !tabsRoot || !panelsRoot) return;

        data.legend.forEach((entry) => {
            const item = element("span", `legend-item ${categoryClass(entry.key)}`);
            item.append(element("span", "legend-swatch"), document.createTextNode(entry.label));
            legendRoot.append(item);
        });

        data.days.forEach((day, index) => {
            const tabLabel = day.key === "sep19" ? "Day 1 - 19 Sep" : day.key === "sep20" ? "Day 2 - 20 Sep" : day.date.replace("September", "Sep");
            const tab = element("button", "day-tab", tabLabel);
            tab.id = `tab-${day.key}`;
            tab.type = "button";
            tab.setAttribute("role", "tab");
            tab.setAttribute("aria-controls", `panel-${day.key}`);
            tab.setAttribute("aria-selected", String(index === 0));
            tab.tabIndex = index === 0 ? 0 : -1;
            tab.addEventListener("click", () => selectDay(index, true));
            tabsRoot.append(tab);
            panelsRoot.append(makeDayPanel(day, index));
        });

        tabsRoot.addEventListener("keydown", (event) => {
            const tabs = [...tabsRoot.querySelectorAll("[role='tab']")];
            const current = tabs.indexOf(document.activeElement);
            if (current < 0) return;
            let next = current;
            if (event.key === "ArrowRight") next = (current + 1) % tabs.length;
            else if (event.key === "ArrowLeft") next = (current - 1 + tabs.length) % tabs.length;
            else if (event.key === "Home") next = 0;
            else if (event.key === "End") next = tabs.length - 1;
            else return;
            event.preventDefault();
            selectDay(next, true);
            tabs[next].focus({ preventScroll: true });
        });

        const hashIndex = data.days.findIndex((day) => `#${day.key}` === window.location.hash);
        if (hashIndex >= 0) selectDay(hashIndex, false);
    }

    const menuButton = document.getElementById("menuToggle");
    const nav = document.getElementById("navLinks");
    if (menuButton && nav) {
        menuButton.addEventListener("click", () => {
            const open = nav.classList.toggle("is-open");
            menuButton.setAttribute("aria-expanded", String(open));
        });
    }

    render();
}());
