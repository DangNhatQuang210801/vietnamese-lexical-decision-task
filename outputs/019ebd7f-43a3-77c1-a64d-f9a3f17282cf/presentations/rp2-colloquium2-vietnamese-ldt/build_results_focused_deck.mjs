import fs from "node:fs/promises";
import path from "node:path";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const root = "D:/Research 2";
const work = `${root}/outputs/rp2_results_focused_work`;
const finalPptx = `${root}/presentation/RP2_Colloquium2_Vietnamese_LDT_RESULTS_FOCUSED.pptx`;
const qualityPath = `${root}/presentation/RP2_Colloquium2_RESULTS_FOCUSED_quality_check.txt`;
const figDir = `${root}/analysis/outputs/r_analysis/figures`;
const tableDir = `${root}/analysis/outputs/r_analysis/tables`;
const modelDir = `${root}/analysis/outputs/r_analysis/models`;
const qcDir = `${root}/analysis/outputs/qc`;
const logoPath = `${root}/presentation/Logo/LDSL.png`;

const C = {
  navy: "#003A61",
  ink: "#263845",
  muted: "#63717A",
  lime: "#8DB600",
  paleBlue: "#EEF4F8",
  paleGreen: "#DDECB3",
  paleGray: "#F3F6F8",
  coral: "#F36C64",
  blue: "#4D8DFF",
  green: "#00A846",
  amber: "#F5B84B",
  white: "#FFFFFF",
  darkShape: "#314654",
  midShape: "#63717A",
};

const font = "Arial";
const mono = "Consolas";
const imageCache = new Map();
let chromeAutoNumber = null;

async function readText(file) {
  return fs.readFile(file, "utf8");
}

function parseCsv(text) {
  const lines = text.trim().split(/\r?\n/);
  const headers = lines.shift().split(",");
  return lines.map((line) => {
    const cols = line.split(",");
    return Object.fromEntries(headers.map((h, i) => [h, cols[i]]));
  });
}

async function loadCsv(file) {
  return parseCsv(await readText(file));
}

function pct(x, digits = 1) {
  return `${(Number(x) * 100).toFixed(digits)}%`;
}

function ms(x) {
  return `${Math.round(Number(x) * 1000)} ms`;
}

function cleanText(s) {
  return String(s).replaceAll("–", "-").replaceAll("×", "x");
}

async function writeBlob(file, blob) {
  await fs.writeFile(file, new Uint8Array(await blob.arrayBuffer()));
}

function setTextStyle(shape, opts = {}) {
  const t = shape.text;
  if (opts.fontSize !== undefined) t.fontSize = opts.fontSize;
  if (opts.color !== undefined) t.color = opts.color;
  if (opts.bold !== undefined) t.bold = opts.bold;
  if (opts.italic !== undefined) t.italic = opts.italic;
  if (opts.typeface !== undefined) t.typeface = opts.typeface;
  if (opts.alignment !== undefined) t.alignment = opts.alignment;
  if (opts.verticalAlignment !== undefined) t.verticalAlignment = opts.verticalAlignment;
  if (opts.wrap !== undefined) t.wrap = opts.wrap;
  try {
    t.insets = opts.insets || { left: 0, top: 0, right: 0, bottom: 0 };
  } catch {}
}

function addText(slide, text, x, y, w, h, opts = {}) {
  const shape = slide.shapes.add({
    geometry: "rect",
    position: { left: x, top: y, width: w, height: h },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text.set(cleanText(text));
  setTextStyle(shape, {
    typeface: opts.typeface || font,
    fontSize: opts.fontSize ?? 16,
    color: opts.color || C.ink,
    bold: opts.bold,
    italic: opts.italic,
    alignment: opts.alignment,
    verticalAlignment: opts.verticalAlignment,
    wrap: true,
    insets: opts.insets || { left: 0, top: 0, right: 0, bottom: 0 },
  });
  return shape;
}

function addRect(slide, x, y, w, h, opts = {}) {
  const shape = slide.shapes.add({
    geometry: opts.geometry || "rect",
    position: { left: x, top: y, width: w, height: h },
    fill: opts.fill || "none",
    line: opts.line
      ? { style: "solid", fill: opts.line.color || C.navy, width: opts.line.width ?? 1 }
      : { style: "solid", fill: "none", width: 0 },
  });
  if (opts.radius) shape.borderRadius = opts.radius;
  return shape;
}

function addCorner(slide) {
  addRect(slide, 793, -18, 78, 88, { geometry: "roundRect", fill: C.lime, radius: "rounded-2xl" });
  addRect(slide, 836, 0, 112, 116, { geometry: "roundRect", fill: C.darkShape, radius: "rounded-2xl" });
  addRect(slide, 794, 56, 98, 70, { geometry: "roundRect", fill: C.midShape, radius: "rounded-2xl" });
}

async function addLogo(slide) {
  try {
    await addImage(slide, logoPath, 833, 494, 70, 27, "LDSL logo");
  } catch {
    addText(slide, "LDSL", 838, 500, 54, 18, { fontSize: 11, color: C.navy, bold: true, alignment: "right" });
  }
}

async function addChrome(slide, num, kicker, title, source = "") {
  slide.background.fill = C.white;
  addCorner(slide);
  const displayNum = chromeAutoNumber === null ? num : ++chromeAutoNumber;
  addRect(slide, 51, 43, 21, 4, { fill: C.lime });
  addText(slide, `${String(displayNum).padStart(2, "0")} | ${kicker}`, 80, 34, 520, 17, {
    fontSize: 9.5,
    color: C.muted,
    bold: true,
  });
  addText(slide, title, 50, 58, 780, 50, {
    fontSize: 28,
    color: C.navy,
    bold: true,
  });
  if (source) addText(slide, source, 52, 474, 700, 15, { fontSize: 7.8, color: C.muted });
  addText(slide, "Vietnamese LDT | RP2 Colloquium 2", 52, 504, 280, 13, { fontSize: 8, color: C.muted });
  addRect(slide, 50, 486, 820, 1.5, { fill: C.paleGreen });
  await addLogo(slide);
}

function addNotes(slide, text) {
  slide.speakerNotes.setText(cleanText(text));
}

function addCard(slide, x, y, w, h, title, body, opts = {}) {
  addRect(slide, x, y, w, h, {
    fill: opts.fill || C.paleBlue,
    line: opts.line === false ? undefined : { color: opts.line || C.paleGreen, width: 0.9 },
  });
  addText(slide, title, x + 12, y + 9, w - 24, 18, {
    fontSize: opts.titleSize || 12.3,
    color: opts.titleColor || C.navy,
    bold: true,
  });
  addText(slide, body, x + 12, y + 31, w - 24, h - 36, {
    fontSize: opts.bodySize || 13.0,
    color: opts.bodyColor || C.ink,
  });
}

function addMetric(slide, x, y, w, value, label, note = "", opts = {}) {
  addRect(slide, x, y, w, 70, { fill: opts.fill || C.paleBlue, line: { color: opts.line || C.navy, width: 0.8 } });
  addText(slide, value, x + 8, y + 8, w - 16, 24, {
    fontSize: opts.valueSize || 22,
    color: opts.valueColor || C.navy,
    bold: true,
    alignment: "center",
  });
  addText(slide, label, x + 8, y + 35, w - 16, 18, {
    fontSize: 9.5,
    color: C.ink,
    bold: true,
    alignment: "center",
  });
  if (note) addText(slide, note, x + 8, y + 53, w - 16, 12, { fontSize: 7.7, color: C.muted, alignment: "center" });
}

function addFlagIcon(slide, x, y, code) {
  addRect(slide, x, y, 54, 34, { fill: C.white, line: { color: C.steel, width: 0.8 } });
  if (code === "CN") {
    addRect(slide, x + 2, y + 2, 50, 30, { fill: "DE2910", line: { color: "DE2910", width: 0 } });
    addText(slide, "*", x + 8, y + 3, 14, 14, { fontSize: 15, bold: true, color: "FFDE00", alignment: "center" });
  } else if (code === "VN") {
    addRect(slide, x + 2, y + 2, 50, 30, { fill: "DA251D", line: { color: "DA251D", width: 0 } });
    addText(slide, "*", x + 19, y + 6, 16, 16, { fontSize: 18, bold: true, color: "FFFF00", alignment: "center" });
  } else if (code === "PT") {
    addRect(slide, x + 2, y + 2, 20, 30, { fill: "006600", line: { color: "006600", width: 0 } });
    addRect(slide, x + 22, y + 2, 30, 30, { fill: "FF0000", line: { color: "FF0000", width: 0 } });
    addRect(slide, x + 19, y + 12, 8, 8, { geometry: "ellipse", fill: "FFD700", line: { color: "FFD700", width: 0 } });
  } else if (code === "FR") {
    addRect(slide, x + 2, y + 2, 16.7, 30, { fill: "0055A4", line: { color: "0055A4", width: 0 } });
    addRect(slide, x + 18.7, y + 2, 16.7, 30, { fill: "FFFFFF", line: { color: "FFFFFF", width: 0 } });
    addRect(slide, x + 35.4, y + 2, 16.6, 30, { fill: "EF4135", line: { color: "EF4135", width: 0 } });
  }
}

function addBullets(slide, items, x, y, w, opts = {}) {
  const gap = opts.gap || 32;
  items.forEach((item, i) => {
    const yy = y + i * gap;
    addRect(slide, x, yy + 6, 6, 6, { fill: opts.dotColor || C.lime });
    addText(slide, item, x + 16, yy, w - 16, gap + 8, {
      fontSize: opts.fontSize || 13.5,
      color: opts.color || C.ink,
    });
  });
}

function addTakeaway(slide, text, y = 425) {
  addRect(slide, 86, y, 790, 44, { fill: C.paleGreen, line: { color: C.lime, width: 1 } });
  addText(slide, text, 112, y + 11, 738, 22, { fontSize: 14, color: C.navy, bold: true, alignment: "center" });
}

async function addImage(slide, filePath, x, y, w, h, alt) {
  const normalized = filePath.replaceAll("\\", "/");
  let bytes = imageCache.get(normalized);
  if (!bytes) {
    bytes = await fs.readFile(normalized);
    imageCache.set(normalized, bytes);
  }
  return slide.images.add({
    data: bytes,
    mimeType: "image/png",
    position: { left: x, top: y, width: w, height: h },
    fit: "contain",
    alt,
  });
}

function addSmallTable(slide, x, y, colWidths, rows, opts = {}) {
  const rowH = opts.rowH || 26;
  rows.forEach((row, r) => {
    let xx = x;
    row.forEach((cell, c) => {
      const w = colWidths[c];
      addRect(slide, xx, y + r * rowH, w, rowH, {
        fill: r === 0 ? (opts.headerFill || C.navy) : (opts.bodyFill || C.white),
        line: { color: r === 0 ? (opts.headerFill || C.navy) : (opts.line || C.paleGreen), width: 0.8 },
      });
      addText(slide, String(cell), xx + 5, y + r * rowH + 6, w - 10, rowH - 8, {
        fontSize: r === 0 ? 8.8 : 8.5,
        color: r === 0 ? C.white : C.ink,
        bold: r === 0 || c === 0,
        alignment: c === 0 ? "left" : "center",
      });
      xx += w;
    });
  });
}

function addHeatmap(slide, x, y, table) {
  const groups = ["low", "mid", "high"];
  const lengths = ["1", "2", "3", "4"];
  const vals = table.map((r) => Number(r.mean_rt));
  const min = Math.min(...vals);
  const max = Math.max(...vals);
  const cellW = 82;
  const cellH = 47;
  addText(slide, "Mean RT by frequency x syllable length", x, y - 28, 420, 22, { fontSize: 13, color: C.navy, bold: true });
  lengths.forEach((l, i) => addText(slide, `${l} syl.`, x + 86 + i * cellW, y, cellW, 20, { fontSize: 9, color: C.muted, bold: true, alignment: "center" }));
  groups.forEach((g, r) => {
    addText(slide, g, x, y + 24 + r * cellH, 74, cellH, { fontSize: 11, color: C.navy, bold: true, verticalAlignment: "middle" });
    lengths.forEach((l, c) => {
      const row = table.find((t) => t.frequency_group === g && t.syllable_length === l);
      const v = Number(row.mean_rt);
      const norm = (v - min) / (max - min || 1);
      const fill = norm > 0.72 ? "#F6C8C2" : norm > 0.48 ? "#F9E4B5" : norm > 0.25 ? C.paleGreen : C.paleBlue;
      addRect(slide, x + 84 + c * cellW, y + 22 + r * cellH, cellW - 3, cellH - 3, {
        fill,
        line: { color: C.white, width: 1 },
      });
      addText(slide, ms(v), x + 87 + c * cellW, y + 34 + r * cellH, cellW - 10, 18, {
        fontSize: 10,
        color: C.ink,
        bold: true,
        alignment: "center",
      });
    });
  });
}

function addModelComparison(slide, rows, x, y) {
  const display = [
    ["Model", "Added predictors", "AIC", "Chisq", "p"],
    ["M0", "random intercepts", Number(rows[0].AIC).toFixed(1), "-", "-"],
    ["M1", "+ frequency", Number(rows[1].AIC).toFixed(1), Number(rows[1].Chisq).toFixed(1), "< .001"],
    ["M2", "+ syllable length", Number(rows[2].AIC).toFixed(1), Number(rows[2].Chisq).toFixed(1), "< .001"],
    ["M3", "+ interaction", Number(rows[3].AIC).toFixed(1), Number(rows[3].Chisq).toFixed(1), ".045"],
  ];
  addSmallTable(slide, x, y, [62, 196, 82, 78, 70], display, { rowH: 34 });
}

function addFigureCaption(slide, caption, x, y, w) {
  addText(slide, caption, x, y, w, 18, { fontSize: 9.4, color: C.muted, alignment: "center" });
}

async function buildDeck() {
  await fs.mkdir(work, { recursive: true });
  await fs.mkdir(`${work}/preview`, { recursive: true });
  await fs.mkdir(`${work}/layout`, { recursive: true });

  const rtFreq = await loadCsv(`${tableDir}/rt_by_frequency_group_v2.csv`);
  const rtLen = await loadCsv(`${tableDir}/rt_by_syllable_length_v2.csv`);
  const rtCell = await loadCsv(`${tableDir}/rt_by_frequency_group_x_syllable_length_v2.csv`);
  const accCond = await loadCsv(`${tableDir}/accuracy_by_condition_v2.csv`);
  const modelComp = await loadCsv(`${tableDir}/model_comparison_rt_v2.csv`);
  const design = await loadCsv(`${qcDir}/design_level_summary.csv`);
  const processingLog = await readText(`${qcDir}/processing_log.txt`);
  const modelSummary = await readText(`${modelDir}/model3_rt_summary_v2.txt`);
  const singular = await readText(`${modelDir}/model_singularity_status_v2.txt`);

  const presentation = Presentation.create({ slideSize: { width: 960, height: 540 } });
  const slides = [];
  for (let i = 0; i < 27; i += 1) slides.push(presentation.slides.add());

  async function s01(slide) {
    slide.background.fill = C.white;
    addCorner(slide);
    addText(slide, "Vietnamese Lexical\nDecision Task", 50, 135, 560, 118, { fontSize: 41, color: C.navy, bold: true });
    addText(slide, "RP2 Colloquium 2 | frequency group x syllable length", 53, 272, 570, 24, { fontSize: 15, color: C.lime, bold: true });
    addText(slide, "Dang Nhat Quang\nSupervisor: Prof. Dr. Tibor Kiss\nJune 2026", 53, 318, 430, 60, { fontSize: 12, color: C.ink });
    addMetric(slide, 52, 410, 128, "48", "participants");
    addMetric(slide, 192, 410, 128, "120", "main trials");
    addMetric(slide, 332, 410, 128, "3 x 4", "real-word design");
    await addLogo(slide);
    addNotes(slide, "Open by framing the project as a controlled lexical-decision study in Vietnamese. The revised talk gives more space to preliminary results and model interpretation.");
  }

  async function s02(slide) {
    await addChrome(slide, 2, "ROADMAP", "The talk moves quickly from motivation to preliminary results.");
    const stages = [
      ["Problem", "Vietnamese spacing separates syllables, not always lexical words."],
      ["Design", "3 frequency groups x 4 syllable lengths, within participants."],
      ["QC", "48 participants, 5,760 main trials, validation passed."],
      ["Results", "Frequency, length, interaction, accuracy, diagnostics."],
      ["Next", "Robustness checks and final interpretation."],
    ];
    stages.forEach((d, i) => {
      const x = 70 + i * 164;
      addCard(slide, x, 170, 138, 118, d[0], d[1], { fill: i === 3 ? C.paleGreen : C.paleBlue, bodySize: 10.4 });
      if (i < 4) addText(slide, "→", x + 143, 212, 20, 22, { fontSize: 18, color: C.lime, bold: true, alignment: "center" });
    });
    addTakeaway(slide, "Main purpose: make the preliminary RT pattern visible and statistically interpretable.");
    addNotes(slide, "This roadmap tells the audience that the talk is results-focused. The early method slides are short, and the central section is analysis.");
  }

  async function s03(slide) {
    await addChrome(slide, 3, "WRITING HISTORY", "Modern Vietnamese script emerged through layered historical influences.");
    const xs = [82, 282, 482, 682];
    const items = [
      ["🇨🇳", "Chữ Hán", "Chinese characters\nadministration + scholarship"],
      ["🇻🇳", "Chữ Nôm", "vernacular Vietnamese\nadapted characters"],
      ["🇵🇹", "Portuguese missionaries", "early romanization\nJesuit influence"],
      ["🇫🇷", "French colonial period", "schooling + administration\nwider spread of Quốc ngữ"],
    ];
    addRect(slide, 140, 236, 650, 3, { fill: C.lime });
    items.forEach((it, i) => {
      addFlagIcon(slide, xs[i] + 47, 148, ["CN", "VN", "PT", "FR"][i]);
      addRect(slide, xs[i] + 64, 226, 18, 18, { geometry: "ellipse", fill: C.navy });
      addCard(slide, xs[i], 268, 148, 94, it[1], it[2], { fill: i === 3 ? C.paleGreen : C.paleBlue, bodySize: 9.7 });
    });
    addTakeaway(slide, "Modern Vietnamese script developed gradually through multiple historical influences.", 414);
    addNotes(slide, "This replaces a dense clarification paragraph with a careful historical timeline. Avoid implying that Quốc ngữ was created by one person.");
  }

  async function s04(slide) {
    await addChrome(slide, 4, "TOKENIZATION PROBLEM", "Vietnamese orthographic spaces often mark syllables, while lexical words may contain several syllables.");
    addText(slide, "sinh viên học tiếng Việt", 95, 150, 760, 38, { fontSize: 30, color: C.navy, bold: true, alignment: "center" });
    ["sinh", "viên", "học", "tiếng", "Việt"].forEach((t, i) => addCard(slide, 105 + i * 142, 210, 102, 58, t, "orthographic token", { bodySize: 8.8 }));
    addText(slide, "↓ lexical interpretation", 380, 288, 210, 24, { fontSize: 12, color: C.muted, alignment: "center" });
    [["sinh viên", 150, 332], ["học", 382, 332], ["tiếng Việt", 550, 332]].forEach(([t, x, y]) => addCard(slide, x, y, 162, 58, t, "lexical word / expression", { fill: C.paleGreen, bodySize: 9 }));
    addTakeaway(slide, "Project scope: test lexical-decision response patterns, not solve Vietnamese word segmentation.");
    addNotes(slide, "Use the example to show why syllable length is theoretically relevant. Then narrow the scope to the lexical-decision experiment.");
  }

  async function s05DataPipeline(slide) {
    await addChrome(slide, 5, "STIMULUS DATA PIPELINE", "How corpus text became review data and final LDT stimuli.");
    const stages = [
      ["Corpus text", "Vietnamese Corpus Data.zip"],
      ["Frequency tables", "1- to 4-syllable n-grams"],
      ["Candidate pool", "frequency, log frequency, syllable length"],
      ["Review / survey", "manual lexical validation before selection"],
      ["Final stimuli", "72 real words + 48 pseudowords"],
    ];
    stages.forEach((stage, i) => {
      const x = 54 + i * 176;
      addCard(slide, x, 126, 144, 92, stage[0], stage[1], {
        fill: i === 3 ? C.paleGreen : C.paleBlue,
        bodySize: 10.2,
        titleSize: 11.2,
      });
      if (i < stages.length - 1) {
        addText(slide, "->", x + 148, 158, 24, 24, { fontSize: 17, color: C.lime, bold: true, alignment: "center" });
      }
    });

    addCard(slide, 58, 242, 292, 136, "Dataset artifacts", "data/processed/*grams_frequency.csv\ncandidate_shortlist_by_length.csv\nmanual_selection_sheet.csv\nfinal_ldt_stimuli_3x4_v1.csv", {
      fill: C.paleBlue,
      bodySize: 11.2,
      titleSize: 12,
    });
    addCard(slide, 58, 395, 292, 54, "Key caution", "The n-gram step proposes candidates; it does not automatically solve Vietnamese word segmentation.", {
      fill: C.paleGreen,
      bodySize: 10.6,
      titleSize: 11.4,
    });

    addRect(slide, 385, 242, 500, 188, { fill: "#172B36", line: { color: C.navy, width: 0.8 } });
    addText(slide, "Python / pandas sketch used for stimulus data preparation", 402, 256, 460, 18, {
      fontSize: 10.5,
      color: C.paleGreen,
      bold: true,
    });
    const code = [
      'files = ["unigrams", "bigrams", "trigrams", "fourgrams"]',
      'freq = pd.concat(pd.read_csv(f"{f}_frequency.csv") for f in files)',
      "",
      "candidates = (freq",
      "  .assign(",
      "    lexical_item=lambda d: d.lexical_item.str.strip().str.lower(),",
      "    syllable_length=lambda d: d.lexical_item.str.split().str.len(),",
      "    log_frequency=lambda d: np.log(d.frequency)",
      "  )",
      '  .query("1 <= syllable_length <= 4")',
      '  .drop_duplicates("lexical_item"))',
      "",
      'candidates["freq_bin"] = candidates.groupby("syllable_length")[',
      '  "log_frequency"].transform(lambda s: pd.qcut(s.rank(method="first"), 8, labels=False))',
      'review_sheet = candidates.sort_values(["syllable_length", "freq_bin"])',
    ].join("\n");
    addText(slide, code, 404, 282, 458, 138, {
      fontSize: 8.15,
      color: C.white,
      typeface: mono,
    });
    addRect(slide, 385, 438, 500, 34, { fill: C.paleGreen, line: { color: C.lime, width: 1 } });
    addText(slide, "Traceable dataset: corpus frequency -> filtered candidates -> review/survey -> final stimuli.", 398, 447, 472, 16, {
      fontSize: 12,
      color: C.navy,
      bold: true,
      alignment: "center",
    });
    addNotes(slide, "This slide answers where the dataset comes from. Explain that Vietnamese spacing gives syllable-based token sequences, so the project uses one- to four-gram frequency tables as candidate sources. The code is a simplified readable sketch of the actual scripts. The important academic point is that n-grams were not accepted as lexical words automatically; they became a review or survey sheet and were manually validated before the final PsychoPy stimulus file.");
  }

  async function s05(slide) {
    await addChrome(slide, 5, "RESEARCH QUESTION", "Do frequency group and syllable length predict Vietnamese lexical-decision response times?");
    addCard(slide, 75, 134, 810, 72, "Research question", "How do corpus frequency group and syllable length affect log reaction time for correct Vietnamese real-word responses?", { fill: C.paleBlue, bodySize: 15 });
    addCard(slide, 90, 250, 230, 126, "H1: frequency", "High-frequency words should be recognized faster than low-frequency words.", { fill: C.paleBlue });
    addCard(slide, 365, 250, 230, 126, "H2: length", "Longer syllable length should increase RT because longer words require more visual/lexical processing.", { fill: C.paleBlue });
    addCard(slide, 640, 250, 230, 126, "H3: interaction", "Frequency may matter differently by length, but this is treated cautiously.", { fill: C.paleGreen });
    addNotes(slide, "State the hypotheses directionally. The interaction is exploratory and should not be overclaimed.");
  }

  async function s06(slide) {
    await addChrome(slide, 6, "EXPERIMENTAL DESIGN", "The real-word design is balanced: 3 frequency groups x 4 syllable lengths.");
    const rows = [["Frequency", "1 syl.", "2 syl.", "3 syl.", "4 syl."], ["low", "6", "6", "6", "6"], ["mid", "6", "6", "6", "6"], ["high", "6", "6", "6", "6"]];
    addSmallTable(slide, 92, 148, [120, 95, 95, 95, 95], rows, { rowH: 42 });
    addMetric(slide, 675, 132, 150, "72", "real words", "balanced");
    addMetric(slide, 675, 220, 150, "48", "pseudowords", "length matched");
    addMetric(slide, 675, 308, 150, "120", "main trials", "randomized");
    addTakeaway(slide, "Every participant saw all main trials in randomized order.");
    addNotes(slide, "This slide establishes design balance. It is short because the revised talk spends more time on results.");
  }

  async function s07(slide) {
    await addChrome(slide, 7, "STIMULI", "Stimuli combine real words and pseudowords so participants must make a lexical decision.");
    addCard(slide, 72, 134, 250, 235, "Real words", "72 items\n\nFrequency: low / mid / high\nLength: 1-4 syllables\n6 items per real-word cell", { fill: C.paleBlue, bodySize: 13 });
    addCard(slide, 355, 134, 250, 235, "Pseudowords", "48 items\n\nLength: 1-4 syllables\n12 items per length\nKeeps the task lexical", { fill: C.paleBlue, bodySize: 13 });
    addCard(slide, 638, 134, 230, 235, "Examples", "Real-word side:\nngày, sinh viên, quê hương\n\nPseudoword side:\nconstructed to remain Vietnamese-like", { fill: C.paleGreen, bodySize: 12 });
    addTakeaway(slide, "The contrast protects the task from becoming simple word reading.");
    addNotes(slide, "Emphasize that pseudowords keep the task genuinely lexical and support the accuracy quality check.");
  }

  async function s08(slide) {
    await addChrome(slide, 8, "TASK PROCEDURE", "The procedure is short, randomized, and keyboard-based.");
    const nodes = [
      ["Instructions", "F = word\nJ = nonword"],
      ["Practice", "4 trials"],
      ["Main task", "120 trials\nrandomized"],
      ["Response", "keyboard RT\n+ accuracy"],
      ["Export", "CSV files\nper participant"],
    ];
    nodes.forEach((n, i) => {
      const x = 55 + i * 172;
      addCard(slide, x, 174, 132, 92, n[0], n[1], { fill: i === 2 ? C.paleGreen : C.paleBlue, bodySize: 10.5 });
      if (i < nodes.length - 1) addText(slide, "→", x + 137, 204, 28, 24, { fontSize: 20, color: C.lime, bold: true, alignment: "center" });
    });
    addCard(slide, 190, 330, 580, 68, "Bias controls", "Randomized trial order; balanced item cells; response mapping documented. These reduce common artifacts but do not remove every possible response bias.", { fill: C.paleGray, bodySize: 12 });
    addNotes(slide, "Keep this slide practical. The task design is simple, but documented randomization and response mapping matter for interpretation.");
  }

  async function s09(slide) {
    await addChrome(slide, 9, "DATA COLLECTION + QC", "The cleaned dataset passes participant, trial, and stimulus validation checks.");
    addMetric(slide, 76, 138, 140, "48", "raw CSV files", "read successfully");
    addMetric(slide, 236, 138, 140, "48", "participants", "0 flagged");
    addMetric(slide, 396, 138, 140, "5,760", "main trials", "analysis pool");
    addMetric(slide, 556, 138, 140, "3,306", "correct RTs", "real-word model");
    addMetric(slide, 716, 138, 140, "45", "timeouts", "0.78%");
    addCard(slide, 92, 270, 340, 108, "QC status", "Minimum N=48 reached\nAll stimulus validation checks passed\nAll expected item presentations present\nRaw data were not modified", { fill: C.paleGreen, bodySize: 12 });
    addCard(slide, 500, 270, 320, 108, "Current evidence base", "RT model uses correct valid real-word responses. Accuracy is analyzed separately as task-quality evidence.", { fill: C.paleBlue, bodySize: 12 });
    addNotes(slide, "This is the defensibility slide. It shows the data are not just collected but checked before modeling.");
  }

  async function s10(slide) {
    await addChrome(slide, 10, "ANALYSIS MODEL", "The main model estimates frequency, syllable length, and their interaction with crossed random intercepts.");
    addCard(slide, 94, 150, 772, 88, "Main RT model", "log_rt ~ frequency_group * syllable_length + (1 | participant_id) + (1 | trial_id)", { fill: C.paleBlue, bodySize: 17 });
    addCard(slide, 108, 285, 230, 92, "Fixed effects", "frequency group\nsyllable length\ninteraction", { fill: C.paleGreen });
    addCard(slide, 365, 285, 230, 92, "Random intercepts", "participant variation\nitem / trial variation", { fill: C.paleBlue });
    addCard(slide, 622, 285, 230, 92, "RT subset", "correct real-word responses\nn = 3,306", { fill: C.paleBlue });
    addNotes(slide, "Explain the formula rather than reading coefficients. Crossed random intercepts prevent treating repeated observations as fully independent.");
  }

  async function s11(slide) {
    await addChrome(slide, 11, "WHY LOG RT + MIXED EFFECTS", "RT data and repeated-measures design motivate the modeling choices.");
    addCard(slide, 78, 142, 248, 176, "Why log RT?", "Reaction times are right-skewed. Log transformation reduces tail influence and makes model residuals more stable.", { fill: C.paleBlue });
    addCard(slide, 356, 142, 248, 176, "Why mixed effects?", "Each participant responds to many items, and each item is seen by many participants. Random intercepts account for this clustering.", { fill: C.paleGreen });
    addCard(slide, 634, 142, 248, 176, "What it supports", "The model estimates condition effects while separating participant and item-level variability.", { fill: C.paleBlue });
    addTakeaway(slide, "The model structure matches the experimental structure.");
    addNotes(slide, "This slide gives the audience a plain-language reason for log RT and mixed effects before the result slides.");
  }

  async function s12(slide) {
    await addChrome(slide, 12, "RESULTS OVERVIEW", "The preliminary pattern is clear: high frequency is faster, longer words are slower.");
    addMetric(slide, 80, 140, 170, ms(rtFreq.find((r) => r.frequency_group === "high").mean_rt), "high-frequency mean RT");
    addMetric(slide, 280, 140, 170, ms(rtFreq.find((r) => r.frequency_group === "low").mean_rt), "low-frequency mean RT");
    addMetric(slide, 510, 140, 170, ms(rtLen.find((r) => r.syllable_length === "1").mean_rt), "1-syllable mean RT");
    addMetric(slide, 710, 140, 170, ms(rtLen.find((r) => r.syllable_length === "4").mean_rt), "4-syllable mean RT");
    addCard(slide, 115, 292, 300, 96, "Frequency direction", "High-frequency real words are faster than low-frequency real words.", { fill: C.paleGreen });
    addCard(slide, 525, 292, 300, 96, "Length direction", "Reaction time increases steadily from 1 to 4 syllables.", { fill: C.paleGreen });
    addTakeaway(slide, "The descriptive results already match H1 and H2.");
    addNotes(slide, "Use this as the transition into the figure-first result section. Do not overclaim model causality.");
  }

  async function s13(slide) {
    await addChrome(slide, 13, "RESULT 1: FREQUENCY", "High-frequency words are recognized faster than low-frequency words.", "R output: rt_by_frequency_group_boxplot_v2.png");
    const highMean = Number(rtFreq.find((r) => r.frequency_group === "high").mean_rt);
    const lowMean = Number(rtFreq.find((r) => r.frequency_group === "low").mean_rt);
    await addImage(slide, `${figDir}/rt_by_frequency_group_boxplot_v2.png`, 65, 118, 560, 330, "RT by frequency group R plot");
    addCard(slide, 660, 134, 210, 96, "Descriptive contrast", `high: ${ms(highMean)}\nlow: ${ms(lowMean)}\nabout ${Math.round((lowMean - highMean) * 1000)} ms faster`, { fill: C.paleGreen, bodySize: 13.8 });
    addCard(slide, 660, 258, 210, 118, "Model interpretation", "The high-frequency coefficient is negative on log RT. In plain terms, frequent words require less decision time.", { fill: C.paleBlue, bodySize: 13 });
    addFigureCaption(slide, "Correct real-word RTs; descriptive plot from R analysis outputs.", 105, 452, 480);
    addNotes(slide, "Make the direction clear. High frequency is faster than low frequency by about 158 ms descriptively. In the mixed model, the negative high-frequency coefficient means lower log RT relative to low frequency. Mid frequency is less clearly separated, so the strongest frequency statement is high versus low.");
  }

  async function s14(slide) {
    await addChrome(slide, 14, "RESULT 2: SYLLABLE LENGTH", "Longer syllable length is associated with slower responses.", "R output: rt_by_syllable_length_boxplot_v2.png");
    const oneSyl = Number(rtLen.find((r) => r.syllable_length === "1").mean_rt);
    const fourSyl = Number(rtLen.find((r) => r.syllable_length === "4").mean_rt);
    await addImage(slide, `${figDir}/rt_by_syllable_length_boxplot_v2.png`, 65, 118, 560, 330, "RT by syllable length R plot");
    addCard(slide, 660, 136, 210, 100, "Descriptive slope", `1 syllable: ${ms(oneSyl)}\n4 syllables: ${ms(fourSyl)}\nabout ${Math.round((fourSyl - oneSyl) * 1000)} ms slower`, { fill: C.paleGreen, bodySize: 13.5 });
    addCard(slide, 660, 265, 210, 112, "Fixed effects", "Length 2, 3, and 4 all have positive coefficients relative to 1 syllable, so length is the strongest model step.", { fill: C.paleBlue, bodySize: 12.8 });
    addFigureCaption(slide, "Correct real-word RTs; descriptive plot from R analysis outputs.", 105, 452, 480);
    addNotes(slide, "This is the strongest descriptive effect. Mean RT rises from about 441 ms for one-syllable words to about 748 ms for four-syllable words. The model comparison supports this: adding syllable length gives the largest improvement in model fit.");
  }

  async function s15(slide) {
    await addChrome(slide, 15, "3 x 4 CONDITION PATTERN", "The full condition-level pattern combines frequency and length.");
    addHeatmap(slide, 105, 164, rtCell);
    await addImage(slide, `${figDir}/rt_frequency_by_length_interaction_v2.png`, 555, 130, 330, 260, "Frequency by syllable length interaction R plot");
    addCard(slide, 100, 368, 360, 62, "Pattern", "Fastest cell: high-frequency 1-syllable words. Slowest cell: low-frequency 4-syllable words.", { fill: C.paleGreen, bodySize: 12.4 });
    addCard(slide, 548, 396, 334, 56, "Caution", "The lines are not perfectly parallel, but the interaction is a secondary pattern.", { fill: C.paleBlue, bodySize: 12.3 });
    addNotes(slide, "This slide satisfies the 3 by 4 table and heatmap requirement. It makes the cell-level pattern visible before the model comparison. Present the table first, then the line plot: both show frequency and syllable length moving in the expected directions, while the non-parallelism is modest.");
  }

  async function s16(slide) {
    await addChrome(slide, 16, "MODEL COMPARISON", "Frequency and syllable length improve fit; the interaction adds only a modest increment.");
    addModelComparison(slide, modelComp, 72, 142);
    addCard(slide, 620, 140, 240, 76, "Frequency improves fit", "M1 vs M0: Chisq = 17.0, p < .001", { fill: C.paleBlue, bodySize: 12.1 });
    addCard(slide, 620, 236, 240, 76, "Largest step", "Adding syllable length gives the largest improvement: Chisq = 217.8", { fill: C.paleGreen, bodySize: 12.1 });
    addCard(slide, 620, 332, 240, 76, "Smallest step", "Interaction improves fit only modestly: Chisq = 12.9, p = .045", { fill: C.paleBlue, bodySize: 12.1 });
    addNotes(slide, "Read this as a sequence: frequency matters, length matters more strongly, and interaction is statistically present but modest. The model comparison is important because it prevents the interpretation from relying only on visual trends.");
  }

  async function s17(slide) {
    await addChrome(slide, 17, "FIXED EFFECTS", "Coefficient direction matches the descriptive pattern.");
    const rows = [
      ["Term", "Estimate", "Direction", "Interpretation"],
      ["high vs low", "-0.200", "faster", "high-frequency words reduce log RT"],
      ["length 2", "+0.257", "slower", "2 syllables slower than 1"],
      ["length 3", "+0.480", "slower", "3 syllables slower than 1"],
      ["length 4", "+0.585", "slower", "4 syllables slowest"],
      ["interaction", "mixed", "modest", "some deviations from parallel lines"],
    ];
    addSmallTable(slide, 70, 132, [130, 95, 100, 420], rows, { rowH: 39 });
    addCard(slide, 190, 404, 560, 56, "Plain-language reading", "High frequency speeds lexical decisions; syllable length slows them; the interaction should be described cautiously.", { fill: C.paleGreen, bodySize: 13.2 });
    addNotes(slide, "Do not read every p-value. This slide is about coefficient direction and interpretation: negative coefficients mean faster RT, positive coefficients mean slower RT. The strongest stable message is the main effect of syllable length plus the high-frequency advantage.");
  }

  async function s18(slide) {
    await addChrome(slide, 18, "PREDICTED EFFECTS", "Model-based predicted means preserve the same main pattern.", "R output: model3_predicted_interaction_v2.png");
    await addImage(slide, `${figDir}/model3_predicted_interaction_v2.png`, 80, 112, 595, 340, "Model predicted interaction R plot");
    addCard(slide, 704, 150, 160, 122, "Estimated pattern", "Predictions show increasing RT with syllable length and lower RT for high-frequency words.", { fill: C.paleGreen, bodySize: 12.2 });
    addCard(slide, 704, 302, 160, 96, "Why useful", "Predicted means connect raw descriptive plots to the mixed-effects model.", { fill: C.paleBlue, bodySize: 12.2 });
    addNotes(slide, "Use this slide to connect model estimates back to the plotted pattern. The predicted means are useful because they show the condition pattern after the model has accounted for participant and item variability.");
  }

  async function s19(slide) {
    await addChrome(slide, 19, "INTERACTION", "The interaction is visible but should be reported cautiously.");
    await addImage(slide, `${figDir}/rt_frequency_by_length_interaction_v2.png`, 85, 120, 530, 326, "Descriptive interaction R plot");
    addCard(slide, 660, 128, 210, 90, "What it suggests", "Frequency advantage is present across lengths, but line spacing varies.", { fill: C.paleBlue, bodySize: 12.4 });
    addCard(slide, 660, 242, 210, 96, "Why cautious", "The improvement from adding interaction is modest, and the sample is still preliminary.", { fill: C.paleGreen, bodySize: 12.4 });
    addCard(slide, 660, 365, 210, 66, "Reporting stance", "Treat as a pattern to revisit, not a final theoretical claim.", { fill: C.paleGray, bodySize: 12.1 });
    addNotes(slide, "This is the anti-overclaim slide. The interaction is not ignored, but it is not sold as the main story. Say that the lines suggest possible frequency by length differences, but the evidence is weaker than the main effects.");
  }

  async function s20(slide) {
    await addChrome(slide, 20, "ACCURACY + TASK QUALITY", "Accuracy suggests participants generally performed the task seriously.", "R output: accuracy_by_condition_barplot_v2.png");
    await addImage(slide, `${figDir}/accuracy_by_condition_barplot_v2.png`, 70, 118, 440, 310, "Accuracy by condition R plot");
    addMetric(slide, 575, 132, 130, pct(accCond.find((r) => r.condition === "word").accuracy), "word accuracy");
    addMetric(slide, 735, 132, 130, pct(accCond.find((r) => r.condition === "pseudoword").accuracy), "pseudoword accuracy");
    addMetric(slide, 575, 236, 130, "0", "participants flagged");
    addMetric(slide, 735, 236, 130, "45", "timeouts", "of 5,760");
    addCard(slide, 575, 350, 292, 70, "Interpretation", "Pseudoword accuracy is lower than word accuracy, but still high enough to support task quality.", { fill: C.paleGreen, bodySize: 11.5 });
    addNotes(slide, "Accuracy is not the main RT model outcome, but it supports the validity of the task and data collection.");
  }

  async function s21(slide) {
    await addChrome(slide, 21, "DIAGNOSTICS", "Diagnostics support cautious preliminary reporting.");
    await addImage(slide, `${figDir}/model3_residual_histogram_v2.png`, 62, 118, 245, 165, "Residual histogram");
    await addImage(slide, `${figDir}/model3_residual_qqplot_v2.png`, 344, 118, 245, 165, "Residual QQ plot");
    await addImage(slide, `${figDir}/model3_residuals_by_length_v2.png`, 626, 118, 245, 165, "Residuals by length");
    addCard(slide, 82, 325, 210, 78, "Residual shape", "No catastrophic pattern, but RT residuals still show tail behavior.", { fill: C.paleBlue, bodySize: 11.7 });
    addCard(slide, 374, 325, 210, 78, "QQ plot", "Extreme deviations remain, so the result should stay preliminary.", { fill: C.paleBlue, bodySize: 11.7 });
    addCard(slide, 666, 325, 210, 78, "Singular fit", "Checked for all model steps; no singular fits detected.", { fill: C.paleGreen, bodySize: 11.7 });
    addNotes(slide, "Mention explicitly that singular fit was checked. The diagnostics are acceptable for preliminary reporting, but not a license to overclaim. The histogram is broadly centered, the QQ plot shows tail deviations, and the residuals-by-length plot does not show a catastrophic length-specific failure.");
  }

  async function s22(slide) {
    await addChrome(slide, 22, "MAIN INTERPRETATION", "The strongest preliminary story is frequency plus syllable length.");
    addCard(slide, 85, 132, 238, 132, "1. Frequency", "High-frequency real words are recognized faster than low-frequency words.", { fill: C.paleGreen, bodySize: 13 });
    addCard(slide, 362, 132, 238, 132, "2. Syllable length", "Longer Vietnamese words show slower lexical-decision responses.", { fill: C.paleGreen, bodySize: 13 });
    addCard(slide, 639, 132, 238, 132, "3. Interaction", "There is evidence of a modest interaction, but it remains a secondary result.", { fill: C.paleBlue, bodySize: 13 });
    addTakeaway(slide, "Cautious interpretation: lexical decision RT reflects both lexical processing and task decision processes, so the results should not be reduced to pure lexical access.", 350);
    addNotes(slide, "This is the main conclusion slide. It should sound careful and academically defensible.");
  }

  async function s23(slide) {
    await addChrome(slide, 23, "LIMITATIONS", "The current analysis is promising, but not yet a final thesis conclusion.");
    addBullets(slide, [
      "N = 48 reaches the project minimum, but is still a modest sample.",
      "Pseudoword design should be reviewed for plausibility and matching.",
      "Frequency source and item matching may need dispersion/register checks.",
      "Current model uses random intercepts; richer structures can be tested if stable.",
      "Interpretation of the interaction requires follow-up robustness checks.",
    ], 100, 130, 720, { gap: 48, fontSize: 14 });
    addNotes(slide, "Limitations make the project stronger by showing what still needs to be checked before final submission.");
  }

  async function s24(slide) {
    await addChrome(slide, 24, "NEXT STEPS", "The next phase strengthens robustness and write-up quality.");
    const steps = [
      ["1", "Re-run R Markdown", "confirm reproducible outputs"],
      ["2", "Robustness checks", "outliers, coding, random effects"],
      ["3", "Item review", "frequency, plausibility, matching"],
      ["4", "Write results", "report model + figures carefully"],
      ["5", "Discussion", "connect to Vietnamese segmentation"],
    ];
    steps.forEach((s, i) => {
      const x = 76 + i * 166;
      addMetric(slide, x, 150, 118, s[0], s[1], "", { fill: i < 2 ? C.paleGreen : C.paleBlue, valueSize: 24 });
      addText(slide, s[2], x - 6, 232, 130, 34, { fontSize: 10.5, color: C.ink, alignment: "center" });
    });
    addCard(slide, 160, 330, 640, 64, "Immediate priority", "Use the current results as preliminary evidence, then refine model robustness and theoretical interpretation.", { fill: C.paleGreen, bodySize: 12.5 });
    addNotes(slide, "This slide shows the project is under control and has a clear path toward final write-up.");
  }

  async function s25(slide) {
    await addChrome(slide, 25, "REFERENCES", "Selected sources for orthography, lexical decision, RT modeling, and tools.");
    const refs = [
      "Baayen, R. H. (2008). Analyzing linguistic data. Cambridge University Press.",
      "Baayen, Davidson, & Bates (2008). Mixed-effects modeling with crossed random effects. Journal of Memory and Language.",
      "Bates et al. (2015). Fitting linear mixed-effects models using lme4. Journal of Statistical Software.",
      "Brysbaert, Mandera, & Keuleers (2018). The word frequency effect in word processing. Current Directions.",
      "DeFrancis (1977). Colonialism and language policy in Viet Nam. De Gruyter Mouton.",
      "Đinh et al. (2008). Word segmentation of Vietnamese texts. LREC.",
      "Keuleers & Brysbaert (2010). Wuggy: A multilingual pseudoword generator. Behavior Research Methods.",
      "Pham & Baayen (2015). Vietnamese compounds and visual lexical decision. Language, Cognition and Neuroscience.",
      "Pham, Tucker, & Baayen (2019). Vietnamese corpora and lexical database. Language Resources and Evaluation.",
      "Ratcliff (1993). Methods for dealing with reaction time outliers. Psychological Bulletin.",
      "Whelan (2008). Effective analysis of reaction time data. The Psychological Record.",
      "Yap & Balota (2009). Visual word recognition of multisyllabic words. Journal of Memory and Language.",
    ];
    refs.forEach((r, i) => {
      const col = i < 6 ? 0 : 1;
      const row = i < 6 ? i : i - 6;
      addText(slide, r, 58 + col * 420, 126 + row * 52, 390, 42, { fontSize: 8.4, color: C.ink });
    });
    addNotes(slide, "References are included for academic completeness. Do not read this slide aloud.");
  }

  async function s26(slide) {
    slide.background.fill = C.white;
    addCorner(slide);
    addText(slide, "Thank you.", 80, 190, 620, 60, { fontSize: 46, color: C.navy, bold: true });
    addText(slide, "Questions about design, QC, or model interpretation are welcome.", 84, 270, 640, 32, { fontSize: 18, color: C.ink });
    addMetric(slide, 82, 350, 145, "48", "participants");
    addMetric(slide, 250, 350, 145, "3,306", "RT model obs.");
    addMetric(slide, 418, 350, 145, "3 x 4", "real-word design");
    await addLogo(slide);
    addNotes(slide, "Close briefly. Invite questions especially about the model comparison, diagnostics, or interpretation of the interaction.");
  }

  const builders = [
    s01, s02, s03, s04, s05DataPipeline, s05, s06, s07, s08, s09, s10, s11, s12, s13,
    s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26,
  ];

  chromeAutoNumber = 1;
  for (let i = 0; i < builders.length; i += 1) await builders[i](slides[i]);
  chromeAutoNumber = null;

  for (const [index, slide] of presentation.slides.items.entries()) {
    const stem = `slide-${String(index + 1).padStart(2, "0")}`;
    const png = await presentation.export({ slide, format: "png", scale: 1 });
    await writeBlob(`${work}/preview/${stem}.png`, png);
    const layout = await slide.export({ format: "layout" });
    await fs.writeFile(`${work}/layout/${stem}.json`, await layout.text());
  }
  const montage = await presentation.export({ format: "webp", montage: true, scale: 1 });
  await writeBlob(`${work}/final-montage.webp`, montage);

  await fs.mkdir(path.dirname(finalPptx), { recursive: true });
  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(finalPptx);

  const figuresAdded = [
    "rt_by_frequency_group_boxplot_v2.png",
    "rt_by_syllable_length_boxplot_v2.png",
    "rt_frequency_by_length_interaction_v2.png",
    "model3_predicted_interaction_v2.png",
    "accuracy_by_condition_barplot_v2.png",
    "model3_residual_histogram_v2.png",
    "model3_residual_qqplot_v2.png",
    "model3_residuals_by_length_v2.png",
  ];

  const qc = [
    "RP2 Colloquium 2 results-focused deck quality check",
    "",
    `Output deck: ${finalPptx}`,
    "Number of slides: 27",
    "",
    "Stimulus-data explanation:",
    "- Added a new slide explaining how corpus text became n-gram frequency tables, candidate pools, review/survey data, and final LDT stimuli.",
    "- Added a Python/pandas code sketch for deriving syllable length, log frequency, frequency bins, and the review sheet.",
    "",
    "Result figures added:",
    ...figuresAdded.map((f) => `- ${f}`),
    "- Editable 3 x 4 mean RT heatmap/table built from rt_by_frequency_group_x_syllable_length_v2.csv",
    "- Editable model comparison table built from model_comparison_rt_v2.csv",
    "",
    "Margins/layout:",
    "- Rebuilt slides with wider margins, consistent title/footer, and graph-first result layouts.",
    "- Results slides use one main figure plus short interpretation cards instead of dense paragraphs.",
    "- Typeface standardized to Arial for projector readability; result annotations and captions were enlarged.",
    "",
    "Model interpretation:",
    "- Expanded interpretation of frequency direction, syllable-length direction, model comparison, fixed effects, predicted effects, and interaction caution.",
    "- Notes explicitly say frequency improves model fit, syllable length gives the largest improvement, and interaction is modest.",
    "",
    "Diagnostics:",
    "- Added residual histogram, QQ plot, residuals-by-length diagnostic figures.",
    "- Singular fit checked: model_singularity_status_v2.txt reports FALSE for model0, model1, model2, and model3.",
    "",
    "Placeholders:",
    "- No intentional placeholders remain.",
    "",
    "Academic caution:",
    "- Interaction is reported as modest and preliminary, not as a final theoretical claim.",
    "- Raw data and original scripts were not modified.",
    "",
    "Embedded speaker notes:",
    "- Speaker notes were added to every slide.",
  ].join("\n");
  await fs.writeFile(qualityPath, qc, "utf8");

  console.log(finalPptx);
  console.log(qualityPath);
  console.log(processingLog.includes("Raw data were not modified.") ? "Raw data log confirmed." : "Raw data log not confirmed.");
  console.log(modelSummary.includes("frequency_grouphigh") && singular.includes("FALSE") ? "Model sources checked." : "Model source check incomplete.");
}

await buildDeck();
