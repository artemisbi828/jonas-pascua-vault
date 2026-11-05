+2026-03-05 09:26 PM

```table-of-contents
```

```dataviewjs
const startDate = dv.date("2026-03-04");
const endDate = dv.date("2026-03-06");
const dailyFolder = "02 - Daily";
const projectNotePath = "03 - Projects/2 - Daily - $2KpM"; // without .md

function toIndentWidth(s) {
  return s.replace(/\t/g, "    ").length;
}

function parseTargetFromTitle(title) {
  const m = title.match(/(\d+)/);
  return m ? Number(m[1]) : 1;
}

function parseCadence(title) {
  const lower = title.toLowerCase();
  if (lower.includes("week")) return "weekly";
  return "daily";
}

function dateKey(d) {
  return d.toISODate();
}

function weekKey(d) {
  return `${d.weekYear}-W${String(d.weekNumber).padStart(2, "0")}`;
}

function getPageDate(page) {
  if (page.file.day) return page.file.day;

  // Fallback for decorated filenames, e.g. "📅 2026-03-05 (Thu)"
  const m = page.file.name.match(/(\d{4}-\d{2}-\d{2})/);
  if (m) return dv.date(m[1]);

  return null;
}

function getDaysBetween(from, to) {
  const days = [];
  let cursor = from;
  while (cursor <= to) {
    days.push(cursor);
    cursor = cursor.plus({ days: 1 });
  }
  return days;
}

async function loadProjectGoals() {
  const filePath = `${projectNotePath}.md`;
  const text = await dv.io.load(filePath);

  if (!text) return [];

  const goals = [];
  const lines = text.split(/\r?\n/);

  for (const line of lines) {
    // Example: - [ ] 2 CRM Calls - Social (Practice) ^d4
    const m = line.match(/^\s*-\s*\[[ xX]\]\s*(.*?)\s+\^([A-Za-z0-9_-]+)\s*$/);
    if (!m) continue;

    const title = m[1].trim();
    const blockId = m[2].trim();

    // For this POC, include daily-goal style IDs (d1, d2, ...)
    if (!/^d\d+$/i.test(blockId)) continue;

    goals.push({
      blockId,
      title,
      target: parseTargetFromTitle(title),
      cadence: parseCadence(title)
    });
  }

  return goals;
}

function parseMilestoneActionCounts(markdownText) {
  const lines = markdownText.split(/\r?\n/);
  const counts = {}; // blockId -> action count

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Milestone line example: - [[2 - Daily - $2KpM#^d4]] :
    const headerMatch = line.match(/^(\s*)-\s*\[\[[^\]]+#\^([A-Za-z0-9_-]+)\]\]\s*:?.*$/);
    if (!headerMatch) continue;

    const baseIndent = toIndentWidth(headerMatch[1] || "");
    const blockId = headerMatch[2];

    let localCount = 0;

    for (let j = i + 1; j < lines.length; j++) {
      const childLine = lines[j];
      const childIndentMatch = childLine.match(/^(\s*)/);
      const childIndent = toIndentWidth(childIndentMatch ? childIndentMatch[1] : "");

      if (childLine.trim() === "") continue;
      if (childIndent <= baseIndent) break;

      if (/^\s*-\s+/.test(childLine)) {
        localCount += 1;
      }
    }

    counts[blockId] = (counts[blockId] || 0) + localCount;
  }

  return counts;
}

const goals = await loadProjectGoals();
if (!goals.length) {
  dv.paragraph("No goals with block IDs like ^d1, ^d2 found in the project note.");
  return;
}

const days = getDaysBetween(startDate, endDate);
const dayKeys = days.map(dateKey);

const folderPrefix = `${dailyFolder}/`;
const dailyPages = dv.pages()
  .where(p => p.file.path.startsWith(folderPrefix))
  .where(p => {
    const d = getPageDate(p);
    return d && d >= startDate && d <= endDate;
  })
  .array();

const countsByGoalByDay = {}; // blockId -> { YYYY-MM-DD -> count }
for (const g of goals) {
  countsByGoalByDay[g.blockId] = {};
  for (const dk of dayKeys) countsByGoalByDay[g.blockId][dk] = 0;
}

const perNoteCounts = [];

for (const page of dailyPages) {
  const text = await dv.io.load(page.file.path);
  if (!text) continue;

  const perMilestone = parseMilestoneActionCounts(text);
  const pageDate = getPageDate(page);
  if (!pageDate) continue;
  const dKey = dateKey(pageDate);

  perNoteCounts.push([page.file.link, dKey, JSON.stringify(perMilestone)]);

  for (const g of goals) {
    countsByGoalByDay[g.blockId][dKey] += (perMilestone[g.blockId] || 0);
  }
}

const debugRows = dailyPages.map(p => {
  const parsed = getPageDate(p);
  return [p.file.link, parsed ? parsed.toISODate() : "(no date)"];
});

const headers = ["Goal"];
for (const d of days) {
  headers.push(`W${d.weekNumber}<br>${d.toFormat("ccc MM-dd")}`);
}

const rows = goals.map(g => {
  const row = [`[[${projectNotePath}#^${g.blockId}|${g.title}]]`];

  // Precompute cumulative weekly counts for weekly goals
  let weekTotals = {};
  for (const d of days) {
    const dk = dateKey(d);
    const wk = weekKey(d);
    weekTotals[wk] = (weekTotals[wk] || 0) + countsByGoalByDay[g.blockId][dk];
  }

  for (const d of days) {
    const dk = dateKey(d);
    const count = countsByGoalByDay[g.blockId][dk];

    if (g.cadence === "weekly") {
      const wk = weekKey(d);
      const wkCount = weekTotals[wk] || 0;
      row.push(`${wkCount}/${g.target}${wkCount >= g.target ? " ✅" : ""}`);
    } else {
      row.push(`${count}/${g.target}${count >= g.target ? " ✅" : ""}`);
    }
  }

  return row;
});

dv.header(3, `Goal Completion Grid (${startDate.toISODate()} to ${endDate.toISODate()})`);
dv.paragraph(`Daily notes found: ${dailyPages.length} in folder "${dailyFolder}"`);
//dv.table(["Daily Note", "Parsed Date"], debugRows);
//dv.table(["Daily Note", "Date Key", "Milestone Counts"], perNoteCounts);
dv.table(headers, rows);

// Optional quick weekly summary
const weeklySummary = [];
const weekSet = [...new Set(days.map(weekKey))];
for (const wk of weekSet) {
  let met = 0;
  for (const g of goals) {
    if (g.cadence === "weekly") {
      let total = 0;
      for (const d of days) {
        if (weekKey(d) !== wk) continue;
        total += countsByGoalByDay[g.blockId][dateKey(d)] || 0;
      }
      if (total >= g.target) met += 1;
    } else {
      // Daily goals: count a goal as met for week if met on at least one day that week
      let metAny = false;
      for (const d of days) {
        if (weekKey(d) !== wk) continue;
        const c = countsByGoalByDay[g.blockId][dateKey(d)] || 0;
        if (c >= g.target) {
          metAny = true;
          break;
        }
      }
      if (metAny) met += 1;
    }
  }
  weeklySummary.push([wk, `${met}/${goals.length} goals hit`]);
}

dv.header(3, "Weekly Snapshot");
dv.table(["Week", "Status"], weeklySummary);
```


- [ ] Daily Activities
	- [ ] 1 interview a week -- senior BI ^d1
	- [ ] 3 entrepreneur calls a week ^d2
	- [ ] 1 workout ^d3
	- [ ] 2 CRM Calls - Social (Practice) ^d4
	- [ ] 2 CRM Calls - Professional ^d5
- [ ] Baby Projects @ $25/month
	- [ ] [[04 - People/Mary-Townsend (T) Bourque]] ^m1
	- [ ] 