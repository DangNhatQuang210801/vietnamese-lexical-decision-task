import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const workspace = "D:/Research 2/outputs/019ebd7f-43a3-77c1-a64d-f9a3f17282cf/presentations/rp2-colloquium2-vietnamese-ldt";
const starterPptx = path.join(workspace, "template-starter.pptx");
const finalPptx = "D:/Research 2/presentation/RP2_Colloquium2_Vietnamese_LDT.pptx";

const C = {
  navy: "#003A61",
  ink: "#263845",
  muted: "#63717A",
  lime: "#8DB600",
  paleBlue: "#EEF4F8",
  paleGreen: "#DDECB3",
  paleGray: "#F3F6F8",
  coral: "#F36C64",
  green: "#00A846",
  blue: "#4D8DFF",
  white: "#FFFFFF",
};

const font = "Poppins";
const mono = "Consolas";
const imageCache = new Map();

function clearSlide(slide) {
  for (const element of [...slide.elements.items]) {
    element.delete?.();
  }
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
  });
  shape.text.set(text);
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
    geometry: "rect",
    position: { left: x, top: y, width: w, height: h },
  });
  if (opts.fill) shape.fill.color = opts.fill;
  if (opts.line) {
    shape.line.color = opts.line.color || C.navy;
    shape.line.width = opts.line.width ?? 1;
  }
  if (opts.fill && w * h > 9500 && opts.contentShape !== false) {
    shape.text.set(".");
    setTextStyle(shape, { typeface: font, fontSize: 1, color: opts.fill });
  }
  return shape;
}

function addRule(slide, x, y, w, color = C.lime, h = 2) {
  return addRect(slide, x, y, w, h, { fill: color });
}

function addKicker(slide, text, num) {
  addRect(slide, 50, 44, 22, 4, { fill: C.lime });
  addText(slide, `${String(num).padStart(2, "0")} | ${text}`, 80, 35, 540, 18, {
    fontSize: 10,
    color: C.muted,
    bold: true,
  });
}

function addTitle(slide, kicker, title, num, source = "") {
  addKicker(slide, kicker, num);
  addText(slide, title, 50, 57, 780, 54, {
    fontSize: 29,
    color: C.navy,
    bold: true,
  });
  if (source) addText(slide, source, 50, 474, 700, 18, { fontSize: 8.5, color: C.muted });
  addText(slide, "Vietnamese LDT | RP2 Colloquium 2", 50, 500, 270, 15, {
    fontSize: 8.5,
    color: C.muted,
  });
}

function addCard(slide, x, y, w, h, title, body, opts = {}) {
  addRect(slide, x, y, w, h, {
    fill: opts.fill || C.paleBlue,
    line: opts.line ? { color: opts.line, width: 1 } : undefined,
  });
  addText(slide, title, x + 12, y + 10, w - 24, 20, {
    fontSize: opts.titleSize || 12,
    color: opts.titleColor || C.navy,
    bold: true,
  });
  addText(slide, body, x + 12, y + 34, w - 24, h - 42, {
    fontSize: opts.bodySize || 13,
    color: opts.bodyColor || C.ink,
  });
}

function addBulletList(slide, items, x, y, w, gap = 34, opts = {}) {
  items.forEach((item, i) => {
    const yy = y + i * gap;
    addRect(slide, x, yy + 6, 6, 6, { fill: opts.dotColor || C.lime });
    addText(slide, item, x + 16, yy, w - 16, gap + 4, {
      fontSize: opts.fontSize || 14,
      color: opts.color || C.ink,
    });
  });
}

function addMetric(slide, x, y, w, value, label, note = "", opts = {}) {
  addRect(slide, x, y, w, 72, { fill: opts.fill || C.paleBlue, line: { color: opts.line || C.navy, width: 0.8 } });
  addText(slide, value, x + 10, y + 10, w - 20, 26, {
    fontSize: opts.valueSize || 23,
    color: opts.valueColor || C.navy,
    bold: true,
    alignment: "center",
  });
  addText(slide, label, x + 10, y + 38, w - 20, 18, {
    fontSize: 10.5,
    color: C.ink,
    alignment: "center",
    bold: true,
  });
  if (note) {
    addText(slide, note, x + 10, y + 56, w - 20, 12, { fontSize: 8.3, color: C.muted, alignment: "center" });
  }
}

function addFlowNode(slide, x, y, w, h, title, body, opts = {}) {
  addRect(slide, x, y, w, h, { fill: opts.fill || C.paleBlue, line: { color: opts.line || C.navy, width: 0.8 } });
  addText(slide, title, x + 9, y + 9, w - 18, 18, { fontSize: 11, color: C.navy, bold: true, alignment: "center" });
  addText(slide, body, x + 9, y + 31, w - 18, h - 38, { fontSize: 9.5, color: C.ink, alignment: "center" });
}

function arrow(slide, x, y) {
  addText(slide, "→", x, y, 26, 25, { fontSize: 24, color: C.lime, bold: true, alignment: "center" });
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
  const rowH = opts.rowH || 27;
  const headerFill = opts.headerFill || C.navy;
  const headerColor = opts.headerColor || C.white;
  const bodyFill = opts.bodyFill || C.white;
  const line = opts.line || C.paleGreen;
  rows.forEach((row, r) => {
    let xx = x;
    row.forEach((cell, c) => {
      const w = colWidths[c];
      addRect(slide, xx, y + r * rowH, w, rowH, {
        fill: r === 0 ? headerFill : bodyFill,
        line: { color: r === 0 ? headerFill : line, width: 0.8 },
      });
      addText(slide, String(cell), xx + 6, y + r * rowH + 6, w - 12, rowH - 8, {
        fontSize: r === 0 ? 9.5 : 9.2,
        color: r === 0 ? headerColor : C.ink,
        bold: r === 0 || c === 0,
        alignment: c === 0 ? "left" : "center",
      });
      xx += w;
    });
  });
}

function addNotes(slide, text) {
  slide.speakerNotes.setText(text);
}

async function slide01(slide) {
  addText(slide, "Vietnamese Lexical\nDecision Task", 50, 146, 560, 110, {
    fontSize: 42,
    color: C.navy,
    bold: true,
  });
  addText(slide, "RP2 Colloquium 2 | frequency group x syllable length", 53, 278, 520, 24, {
    fontSize: 16,
    color: C.lime,
    bold: true,
  });
  addText(slide, "Dang Nhat Quang\nSupervisor: Prof. Dr. Tibor Kiss\n12 June 2026", 53, 322, 460, 62, {
    fontSize: 12,
    color: C.ink,
  });
  addMetric(slide, 52, 412, 128, "48", "participants");
  addMetric(slide, 192, 412, 128, "120", "main trials");
  addMetric(slide, 332, 412, 128, "3 x 4", "real-word design");
  addNotes(slide, "Open by framing the project as a controlled lexical-decision study in Vietnamese. Emphasize that the talk focuses on the full research process, especially methodology and QC, not only on results.");
}

async function slide02(slide) {
  addTitle(slide, "RESEARCH STORY", "The talk follows the project from linguistic motivation to cautious preliminary results.", 2);
  const steps = [
    ["Background", "Vietnamese writing and spacing"],
    ["Problem", "syllables are spaced, lexical words may be multi-syllabic"],
    ["Design", "3 x 4 within-participant lexical decision"],
    ["Pipeline", "PsychoPy/Pavlovia, Python/pandas, R Markdown"],
    ["QC", "participant, item, trial, RT, response checks"],
    ["Results", "frequency, length, interaction, diagnostics"],
    ["Next steps", "limitations and six-month plan"],
  ];
  steps.forEach((s, i) => {
    const x = 58 + (i % 4) * 205;
    const y = 135 + Math.floor(i / 4) * 120;
    addCard(slide, x, y, 178, 82, s[0], s[1], { fill: i < 3 ? C.paleBlue : C.paleGreen, bodySize: 11.5 });
    if (i < 6 && i !== 3) arrow(slide, x + 180, y + 28);
  });
  addText(slide, "Aim for the presentation: show that the experiment is methodologically defensible, reproducible, and interpreted carefully.", 58, 405, 720, 44, {
    fontSize: 15,
    color: C.navy,
    bold: true,
  });
  addNotes(slide, "This slide gives the audience a map. The main story is: Vietnamese creates a real segmentation motivation, but the project narrows the question to frequency and syllable length in lexical decision.");
}

async function slide03(slide) {
  addTitle(slide, "BACKGROUND", "Quốc ngữ is the current endpoint of a layered writing history, not a single-inventor story.", 3, "Sources: Fernandes & Assunção, 2017; DeFrancis, 1977; Encyclopaedia Britannica, 2026");
  const nodes = [
    ["Chữ Hán", "Chinese characters\nadministration, scholarship"],
    ["Chữ Nôm", "vernacular Vietnamese\nadapted/created characters"],
    ["Quốc ngữ", "Latin-based Vietnamese\nmissionary codification, later mass adoption"],
  ];
  nodes.forEach((n, i) => {
    const x = 70 + i * 275;
    addFlowNode(slide, x, 170, 205, 95, n[0], n[1], { fill: i === 2 ? C.paleGreen : C.paleBlue });
    if (i < 2) arrow(slide, x + 217, 205);
  });
  addCard(slide, 90, 315, 745, 78, "Clarification", "The modern script was shaped by several European missionaries. Portuguese Jesuits were central in early romanization; Alexandre de Rhodes published an influential Vietnamese-Portuguese-Latin dictionary in 1651. Later French colonial schooling/administration and Vietnamese print culture helped Quốc ngữ spread.", {
    fill: C.paleGray,
    bodySize: 12.2,
  });
  addText(slide, "Why this matters here: the modern script is alphabetic and spaced, but spacing does not make Vietnamese word boundaries simple.", 92, 415, 700, 32, { fontSize: 14, color: C.navy, bold: true });
  addNotes(slide, "Answer the common question gently: it is not accurate to say that one French or Italian person created Quốc ngữ. The better version is a collaborative missionary history, with Portuguese influence and de Rhodes' 1651 publication, followed by colonial and Vietnamese adoption.");
}

async function slide04(slide) {
  addTitle(slide, "TOKENIZATION PROBLEM", "Vietnamese spaces often separate syllables, while lexical words may contain several syllables.", 4, "Sources: Ha, 2003; Đinh et al., 2008; Verdonschot et al., 2022");
  addText(slide, "Example string", 72, 130, 200, 18, { fontSize: 10, color: C.muted, bold: true });
  addText(slide, "sinh viên học tiếng Việt", 72, 154, 550, 40, { fontSize: 30, color: C.navy, bold: true });
  addText(slide, "Syllable-spaced orthography", 72, 232, 240, 20, { fontSize: 12, color: C.muted, bold: true });
  ["sinh", "viên", "học", "tiếng", "Việt"].forEach((txt, i) => {
    addRect(slide, 72 + i * 122, 260, 96, 44, { fill: C.paleBlue, line: { color: C.navy, width: 0.8 } });
    addText(slide, txt, 72 + i * 122, 272, 96, 22, { fontSize: 16, color: C.navy, bold: true, alignment: "center" });
  });
  addText(slide, "Lexical-word interpretation", 72, 338, 240, 20, { fontSize: 12, color: C.muted, bold: true });
  const words = [
    [72, 366, 218, "sinh viên"],
    [315, 366, 96, "học"],
    [438, 366, 218, "tiếng Việt"],
  ];
  words.forEach(([x, y, w, txt]) => {
    addRect(slide, x, y, w, 48, { fill: C.paleGreen, line: { color: C.lime, width: 1 } });
    addText(slide, txt, x, y + 13, w, 22, { fontSize: 16, color: C.navy, bold: true, alignment: "center" });
  });
  addCard(slide, 705, 164, 160, 180, "Key point", "space ≠ lexical word boundary\n\nThis is why Vietnamese word segmentation is non-trivial for NLP and for stimulus selection.", {
    fill: C.paleGray,
    bodySize: 13,
  });
  addNotes(slide, "Use the example sinh viên. Orthographically it has a space, but it is one lexical word. This motivates why syllable count and lexical-word status must be controlled rather than assumed.");
}

async function slide05(slide) {
  addTitle(slide, "PROJECT SCOPE", "The project does not solve Vietnamese tokenization; it tests frequency and syllable length in lexical decision.", 5);
  addCard(slide, 60, 150, 240, 160, "Not the goal", "Build a full Vietnamese word segmenter\n\nResolve all lexical boundary ambiguity\n\nClassify every possible multi-syllable string", { fill: C.paleGray });
  addCard(slide, 360, 150, 240, 160, "Actual goal", "Use a controlled lexical decision task\n\nManipulate frequency group and syllable length\n\nMeasure RT and accuracy", { fill: C.paleBlue });
  addCard(slide, 660, 150, 210, 160, "Contribution", "A clean psycholinguistic test case for Vietnamese visual word recognition.", { fill: C.paleGreen });
  addRule(slide, 100, 364, 720, C.lime, 2);
  addText(slide, "Core predictor structure: frequency group (low / mid / high) x syllable length (1 / 2 / 3 / 4)", 110, 382, 700, 30, {
    fontSize: 16,
    color: C.navy,
    bold: true,
    alignment: "center",
  });
  addNotes(slide, "This scope slide protects the project from overclaiming. The broader tokenization problem motivates the work, but the actual experiment tests frequency and syllable-length effects.");
}

async function slide06(slide) {
  addTitle(slide, "RESEARCH QUESTION", "Do frequency group and syllable length predict Vietnamese lexical-decision response times?", 6);
  addRect(slide, 70, 132, 790, 74, { fill: C.paleBlue, line: { color: C.navy, width: 0.8 } });
  addText(slide, "How do corpus frequency group and syllable length affect log reaction time for correct Vietnamese real-word responses?", 96, 151, 738, 36, {
    fontSize: 20,
    color: C.navy,
    bold: true,
    alignment: "center",
  });
  const hyps = [
    ["H1: frequency", "High-frequency words should be recognized faster than low-frequency words."],
    ["H2: length", "Longer syllable length should increase RT because longer words require more visual/lexical processing."],
    ["H3: interaction", "The size of the frequency effect may vary across syllable lengths."],
  ];
  hyps.forEach((h, i) => addCard(slide, 76 + i * 275, 252, 230, 126, h[0], h[1], { fill: i === 2 ? C.paleGreen : C.paleGray }));
  addText(slide, "Interpretation rule: interaction evidence will be treated as preliminary unless it is stable across diagnostics and follow-up checks.", 80, 415, 760, 28, {
    fontSize: 13.5,
    color: C.navy,
    bold: true,
    alignment: "center",
  });
  addNotes(slide, "State the research question slowly. The hypotheses are directional for frequency and length, but the interaction is framed carefully as possible variation rather than a strong prediction.");
}

async function slide07(slide) {
  addTitle(slide, "EXPERIMENTAL DESIGN", "The real-word design is balanced: 3 frequency groups x 4 syllable lengths, within participant.", 7);
  const x = 82, y = 145, rowH = 48;
  const colW = [105, 120, 120, 120, 120];
  const rows = [
    ["Frequency", "1 syll.", "2 syll.", "3 syll.", "4 syll."],
    ["low", "6", "6", "6", "6"],
    ["mid", "6", "6", "6", "6"],
    ["high", "6", "6", "6", "6"],
  ];
  addSmallTable(slide, x, y, colW, rows, { rowH });
  addText(slide, "cell value = number of real-word items", x + 118, y + 212, 360, 16, { fontSize: 10, color: C.muted });
  addMetric(slide, 675, 142, 150, "72", "real words", "6 per real-word cell", { fill: C.paleGreen });
  addMetric(slide, 675, 230, 150, "48", "pseudowords", "12 per length", { fill: C.paleBlue });
  addMetric(slide, 675, 318, 150, "120", "main trials", "per participant", { fill: C.paleGray });
  addText(slide, "All participants see all main trials in randomized order.", 100, 406, 500, 24, { fontSize: 15, color: C.navy, bold: true });
  addNotes(slide, "Explain that within participant means each participant contributes responses across all conditions. The real-word manipulation is balanced, and pseudowords are added for the lexical-decision task.");
}

async function slide08(slide) {
  addTitle(slide, "STIMULI", "Pseudowords keep the task genuinely lexical: participants must distinguish words from nonwords.", 8);
  addSmallTable(slide, 58, 135, [150, 118, 118, 118, 118], [
    ["Type", "Length 1", "Length 2", "Length 3", "Length 4"],
    ["real words", "18", "18", "18", "18"],
    ["pseudowords", "12", "12", "12", "12"],
    ["total", "30", "30", "30", "30"],
  ], { rowH: 38 });
  addCard(slide, 620, 135, 220, 120, "Example real words", "núi\nloại sản phẩm\nđiện thoại di động", { fill: C.paleGreen, bodySize: 14 });
  addCard(slide, 620, 278, 220, 122, "Example pseudowords", "bệc viện ← bệnh viện\nmối quan hế ← mối quan hệ\ntrính độ học vấn ← trình độ học vấn", { fill: C.paleBlue, bodySize: 12.2 });
  addText(slide, "Pseudoword construction changes a syllable while keeping the item Vietnamese-like enough for the task.", 76, 340, 480, 42, {
    fontSize: 15,
    color: C.navy,
    bold: true,
  });
  addBulletList(slide, ["tone changes", "vowel changes", "final-consonant changes"], 92, 404, 360, 24, { fontSize: 12.5 });
  addNotes(slide, "Use one or two examples only when speaking. The point is not that pseudowords are perfect, but that they prevent participants from pressing word for everything.");
}

async function slide09(slide) {
  addTitle(slide, "TASK PROCEDURE", "The procedure is short, randomized, and keyboard-based to keep lexical decisions clean.", 9);
  const steps = [
    ["Instructions", "F = word\nJ = nonword"],
    ["Practice", "4 trials\nwith feedback"],
    ["Main task", "120 trials\nrandomized"],
    ["Response", "keyboard RT\naccuracy"],
    ["Export", "CSV files\nper participant"],
  ];
  steps.forEach((s, i) => {
    const x = 55 + i * 170;
    addFlowNode(slide, x, 170, 135, 98, s[0], s[1], { fill: i === 2 ? C.paleGreen : C.paleBlue });
    if (i < steps.length - 1) arrow(slide, x + 138, 205);
  });
  addText(slide, "Main-trial order is randomized for each participant.", 92, 326, 390, 28, { fontSize: 17, color: C.navy, bold: true });
  addCard(slide, 540, 312, 272, 86, "Response mapping", "F key: word\nJ key: nonword", { fill: C.paleGray, bodySize: 16 });
  addNotes(slide, "Explain the participant experience. Four practice trials come before the 120 main trials, and F/J responses allow keyboard timing without mouse movement.");
}

async function slide10(slide) {
  addTitle(slide, "BIAS CONTROLS", "The design reduces common task artifacts and monitors the ones it cannot remove.", 10);
  const rows = [
    ["Practice / learning", "Practice trials before the main task; randomized main trials."],
    ["Response bias", "Pseudowords require word/nonword discrimination; QC checks one-key overuse."],
    ["Key / side bias", "F/J supports balanced keyboard responding, but does not fully eliminate side bias."],
    ["Fatigue / automatic pressing", "Monitor accuracy, missing RTs, unusually fast RTs, and one-key patterns."],
  ];
  addSmallTable(slide, 62, 135, [190, 620], [["Potential issue", "Control / monitoring"], ...rows], { rowH: 56 });
  addText(slide, "Important wording: F/J helps reduce motor-response delay and makes responses more balanced; it does not completely remove bias.", 80, 438, 765, 28, {
    fontSize: 13.5,
    color: C.navy,
    bold: true,
    alignment: "center",
  });
  addNotes(slide, "This is a defensibility slide. Avoid saying that F and J solve bias. The stronger claim is that the setup reduces motor delay and makes the response layout balanced, while QC monitors behavior.");
}

async function slide11(slide) {
  addTitle(slide, "EXPERIMENT DEMO", "A short PsychoPy video can show the task more clearly than more procedure text.", 11);
  addRect(slide, 110, 135, 660, 300, { fill: C.paleGray, line: { color: C.navy, width: 1.2 } });
  addText(slide, "Insert PsychoPy demo video here", 180, 230, 520, 36, {
    fontSize: 28,
    color: C.navy,
    bold: true,
    alignment: "center",
  });
  addText(slide, "Suggested file: presentation/Demo.mov", 215, 280, 450, 22, {
    fontSize: 14,
    color: C.muted,
    alignment: "center",
  });
  addText(slide, "Show: stimulus display → F/J keypress → next randomized trial", 185, 327, 510, 24, {
    fontSize: 14,
    color: C.ink,
    alignment: "center",
  });
  addNotes(slide, "Pause here during the talk to play or insert the demo. Keep the spoken explanation short because the next section covers the full data pipeline.");
}

async function slide12(slide) {
  addTitle(slide, "METHODOLOGY PIPELINE", "The project is reproducible from experiment implementation through R Markdown modeling.", 12);
  const logos = [
    ["PsychoPy", "D:/Research 2/presentation/Logo/PsychoPy.png", 58],
    ["Pavlovia", "D:/Research 2/presentation/Logo/Pavlovia.png", 205],
    ["Python", "D:/Research 2/presentation/Logo/Python.png", 352],
    ["pandas", "D:/Research 2/presentation/Logo/pandas.png", 499],
    ["R", "D:/Research 2/presentation/Logo/R.png", 646],
  ];
  for (let i = 0; i < logos.length; i++) {
    const [label, file, x] = logos[i];
    addRect(slide, x, 142, 112, 92, { fill: C.white, line: { color: C.paleGreen, width: 1 } });
    await addImage(slide, file, x + 22, 154, 68, 42, label);
    addText(slide, label, x + 10, 205, 92, 18, { fontSize: 10, color: C.navy, bold: true, alignment: "center" });
    if (i < logos.length - 1) arrow(slide, x + 115, 175);
  }
  addFlowNode(slide, 78, 300, 135, 70, "Experiment", "PsychoPy / Pavlovia", { fill: C.paleBlue });
  arrow(slide, 220, 322);
  addFlowNode(slide, 250, 300, 130, 70, "Raw CSV", "participant files", { fill: C.paleGray });
  arrow(slide, 386, 322);
  addFlowNode(slide, 415, 300, 150, 70, "Cleaning/QC", "Python + pandas", { fill: C.paleGreen });
  arrow(slide, 572, 322);
  addFlowNode(slide, 600, 300, 165, 70, "Analysis", "R Markdown\nlme4 / lmerTest", { fill: C.paleBlue });
  addNotes(slide, "This is the main methods pipeline. Emphasize that every step has an output: raw CSVs, cleaned datasets, QC summaries, R Markdown, tables, figures and model files.");
}

async function slide13(slide) {
  addTitle(slide, "CLEANING AND QC", "Cleaning was designed to preserve raw data while making analysis copies auditable.", 13);
  const checks = [
    ["Read participant CSVs", "multiple encodings: utf-8-sig, utf-8, cp1258"],
    ["Validate IDs", "participant ID in filename and file content"],
    ["Check trial counts", "4 practice + 120 main trials per participant"],
    ["Check response mapping", "F/J labels and accuracy recomputed"],
    ["Convert RT", "numeric RT, log_rt, missing/timeout flags"],
    ["Validate stimuli", "trial_id and stimulus list matched against final design"],
    ["Create outputs", "cleaned datasets + participant/item/design QC"],
    ["Preserve raw files", "raw CSVs are read, not modified"],
  ];
  checks.forEach((c, i) => {
    const col = i < 4 ? 0 : 1;
    const row = i % 4;
    const x = 64 + col * 405;
    const y = 128 + row * 72;
    addCard(slide, x, y, 345, 55, c[0], c[1], { fill: i % 2 ? C.paleGray : C.paleBlue, titleSize: 10.5, bodySize: 10.7 });
  });
  addNotes(slide, "Walk through the cleaning steps as quality protection, not as technical detail for its own sake. The raw data were preserved; the script creates separate analysis copies.");
}

async function slide14(slide) {
  addTitle(slide, "QC STATUS", "The current dataset passes the main participant, trial, and stimulus-validation checks.", 14);
  const metrics = [
    ["48", "files read", "participant CSVs"],
    ["48", "participants", "unique IDs"],
    ["0", "flagged", "participant QC"],
    ["5,760", "main trials", "48 x 120"],
    ["5,715", "valid RTs", "main trials"],
    ["3,306", "RT model rows", "correct real words"],
  ];
  metrics.forEach((m, i) => addMetric(slide, 55 + (i % 3) * 175, 138 + Math.floor(i / 3) * 92, 145, m[0], m[1], m[2], { fill: i % 2 ? C.paleGray : C.paleBlue }));
  addCard(slide, 620, 145, 230, 210, "Validation passed", "Stimulus file readable\n120 unique main trial IDs\n72 real words, 48 pseudowords\nEvery trial_id has 48 presentations\nNo unexpected trial IDs\nRaw data were not modified", {
    fill: C.paleGreen,
    bodySize: 12.3,
  });
  addText(slide, "Current stage: ready for Colloquium 2 presentation, but results remain preliminary.", 86, 414, 720, 28, {
    fontSize: 15,
    color: C.navy,
    bold: true,
    alignment: "center",
  });
  addNotes(slide, "Use this slide to show that the analysis is not based on uninspected files. The project has reached the minimum N, but keep the interpretation preliminary.");
}

async function slide15(slide) {
  addTitle(slide, "REPRODUCIBILITY", "The workflow keeps raw data, cleaned analysis copies, QC outputs, and the analysis report separate.", 15);
  const nodes = [
    ["Raw PsychoPy CSVs", "data/experiment_results\nread only"],
    ["Cleaning script", "analysis/01_prepare_clean_data.py"],
    ["Cleaned datasets", "all_trials_clean\nmain_trials_clean\nrt_realword_correct"],
    ["QC outputs", "participant/item/design\nstimulus validation"],
    ["R Markdown", "analysis/RP2_final_analysis_v2.Rmd"],
    ["Analysis outputs", "figures, tables,\nmodel summaries"],
  ];
  nodes.forEach((n, i) => {
    const x = 60 + (i % 3) * 270;
    const y = 138 + Math.floor(i / 3) * 118;
    addFlowNode(slide, x, y, 210, 78, n[0], n[1], { fill: i === 0 ? C.paleGray : i === 4 ? C.paleGreen : C.paleBlue });
    if (i % 3 < 2) arrow(slide, x + 214, y + 26);
  });
  addText(slide, "Reproducibility principle: every transformation has a named script or output file.", 98, 412, 700, 28, {
    fontSize: 15,
    color: C.navy,
    bold: true,
    alignment: "center",
  });
  addNotes(slide, "This slide is useful for questions about reproducibility. The key point is separation: raw data are preserved, cleaned copies are generated, and the R Markdown report can be rendered again.");
}

async function slide16(slide) {
  addTitle(slide, "ANALYSIS PLAN", "Log RT and mixed-effects models match the structure of repeated lexical-decision data.", 16, "Sources: Baayen et al., 2008; Bates et al., 2015; Ratcliff, 1993; Whelan, 2008");
  addCard(slide, 70, 135, 245, 180, "Why log RT?", "Reaction-time data are typically right-skewed.\n\nUsing log_rt reduces skew and makes linear-model assumptions more plausible.\n\nDiagnostics are still checked.", { fill: C.paleBlue });
  addCard(slide, 357, 135, 245, 180, "Why mixed effects?", "Each participant sees many items.\n\nEach item is seen by many participants.\n\nRandom intercepts account for participant and item variability.", { fill: C.paleGreen });
  addCard(slide, 645, 135, 215, 180, "RT model data", "Correct real-word main trials only\n\nn = 3,306\nparticipants = 48\nitems = 72", { fill: C.paleGray });
  addText(slide, "Accuracy is summarized separately because pseudowords are central for task quality but not part of the real-word RT model.", 85, 378, 740, 40, {
    fontSize: 14.5,
    color: C.navy,
    bold: true,
    alignment: "center",
  });
  addNotes(slide, "Explain log RT in simple terms: reaction times have a long right tail, so log transformation makes the model better behaved. Mixed effects are needed because observations are crossed by participant and item.");
}

async function slide17(slide) {
  addTitle(slide, "MODEL", "The main model estimates frequency, syllable length, and their interaction with participant and item intercepts.", 17);
  addRect(slide, 70, 132, 790, 78, { fill: C.paleGray, line: { color: C.navy, width: 0.8 } });
  addText(slide, "log_rt ~ frequency_group * syllable_length +\n(1 | participant_id) + (1 | trial_id)", 92, 150, 746, 42, {
    fontSize: 18,
    color: C.navy,
    bold: true,
    typeface: mono,
    alignment: "center",
  });
  addSmallTable(slide, 92, 250, [205, 140, 140], [
    ["Random effect", "Variance", "Std. dev."],
    ["participant_id", "0.0148", "0.1217"],
    ["trial_id", "0.0008", "0.0291"],
    ["residual", "0.0469", "0.2165"],
  ], { rowH: 34 });
  addCard(slide, 615, 252, 220, 118, "Model status", "Observations: 3,306\nParticipants: 48\nItems: 72\nSingular fit: false", { fill: C.paleGreen, bodySize: 13.2 });
  addText(slide, "This structure avoids treating 3,306 rows as fully independent observations.", 112, 416, 690, 24, { fontSize: 15, color: C.navy, bold: true, alignment: "center" });
  addNotes(slide, "Do not read every coefficient here. The purpose is to justify the model structure: fixed effects for the experimental predictors and random intercepts for participants and items.");
}

async function slide18(slide) {
  addTitle(slide, "PRELIMINARY RESULTS", "Descriptively, high-frequency words are faster and longer words are slower.", 18);
  await addImage(slide, "D:/Research 2/analysis/outputs/r_analysis/figures/rt_by_frequency_group_boxplot_v2.png", 56, 128, 380, 260, "RT by frequency group");
  await addImage(slide, "D:/Research 2/analysis/outputs/r_analysis/figures/rt_by_syllable_length_boxplot_v2.png", 456, 128, 380, 260, "RT by syllable length");
  addSmallTable(slide, 80, 402, [96, 86, 86, 86], [
    ["Frequency", "low", "mid", "high"],
    ["Mean RT", "0.668", "0.618", "0.510"],
  ], { rowH: 28 });
  addSmallTable(slide, 455, 402, [96, 70, 70, 70, 70], [
    ["Length", "1", "2", "3", "4"],
    ["Mean RT", "0.441", "0.528", "0.684", "0.748"],
  ], { rowH: 28 });
  addNotes(slide, "Keep this descriptive. The pattern is clear: high-frequency words are faster, and reaction times increase with syllable length. The model comparison will handle inference.");
}

async function slide19(slide) {
  addTitle(slide, "INTERACTION", "The frequency advantage may vary by syllable length, but the interaction is modest.", 19);
  await addImage(slide, "D:/Research 2/analysis/outputs/r_analysis/figures/model3_predicted_interaction_v2.png", 76, 120, 560, 360, "Predicted interaction plot");
  addCard(slide, 670, 160, 178, 164, "Cautious read", "Interaction model improves fit over the additive model.\n\nLikelihood-ratio p = .0449.\n\nTreat as evidence of possible variation, not a large final conclusion.", {
    fill: C.paleGreen,
    bodySize: 12.1,
  });
  addText(slide, "Result wording: frequency and length effects are clearer than the interaction.", 670, 360, 180, 46, {
    fontSize: 13,
    color: C.navy,
    bold: true,
    alignment: "center",
  });
  addNotes(slide, "Use cautious language. The interaction is statistically borderline and should be described as possible variation in the frequency effect across lengths, not as the central finding.");
}

async function slide20(slide) {
  addTitle(slide, "MODEL COMPARISON", "Adding frequency and syllable length improves model fit; the interaction adds only a small increment.", 20);
  addSmallTable(slide, 74, 140, [100, 105, 105, 105, 105, 120], [
    ["Model", "npar", "AIC", "BIC", "Chisq", "p"],
    ["model0", "4", "-286.3", "-261.9", "-", "-"],
    ["model1 + freq", "6", "-299.2", "-262.6", "16.95", "< .001"],
    ["model2 + length", "9", "-511.0", "-456.1", "217.80", "< .001"],
    ["model3 + interaction", "15", "-511.9", "-420.4", "12.89", ".0449"],
  ], { rowH: 42 });
  addCard(slide, 645, 150, 205, 116, "Largest step", "Adding syllable length gives the biggest model-fit improvement.", { fill: C.paleGreen, bodySize: 13 });
  addCard(slide, 645, 294, 205, 116, "Small step", "The interaction improves fit, but weakly. It should guide follow-up checks rather than stand alone.", { fill: C.paleGray, bodySize: 12.4 });
  addNotes(slide, "Point out the model sequence. Frequency improves over baseline; length strongly improves the model; the interaction is statistically present but modest.");
}

async function slide21(slide) {
  addTitle(slide, "DIAGNOSTICS", "Model checks support cautious reporting, not overconfident final claims.", 21);
  await addImage(slide, "D:/Research 2/analysis/outputs/r_analysis/figures/model3_residual_histogram_v2.png", 58, 125, 245, 170, "Residual histogram");
  await addImage(slide, "D:/Research 2/analysis/outputs/r_analysis/figures/model3_residual_qqplot_v2.png", 318, 125, 245, 170, "Residual QQ plot");
  await addImage(slide, "D:/Research 2/analysis/outputs/r_analysis/figures/model3_residuals_by_length_v2.png", 578, 125, 245, 170, "Residuals by length");
  addCard(slide, 88, 330, 210, 88, "Singularity", "model0, model1, model2, model3:\nFALSE", { fill: C.paleGreen, bodySize: 13 });
  addCard(slide, 360, 330, 210, 88, "VIF check", "Adjusted GVIF values remain below common concern thresholds.", { fill: C.paleBlue, bodySize: 12.3 });
  addCard(slide, 632, 330, 210, 88, "Remaining caution", "RT diagnostics should be reviewed again before thesis-level claims.", { fill: C.paleGray, bodySize: 12.3 });
  addNotes(slide, "This slide is a bridge between statistics and caution. Diagnostics do not show a major singularity issue, but residual behavior and model assumptions still deserve final review.");
}

async function slide22(slide) {
  addTitle(slide, "TASK QUALITY", "Accuracy and response QC suggest participants generally performed the task seriously.", 22);
  await addImage(slide, "D:/Research 2/analysis/outputs/r_analysis/figures/accuracy_by_condition_barplot_v2.png", 72, 128, 430, 285, "Accuracy by condition");
  addMetric(slide, 560, 142, 130, "95.7%", "word accuracy", "main trials", { fill: C.paleGreen });
  addMetric(slide, 720, 142, 130, "82.0%", "pseudoword accuracy", "main trials", { fill: C.paleBlue });
  addMetric(slide, 560, 250, 130, "0", "participants", "flagged by QC", { fill: C.paleGray });
  addMetric(slide, 720, 250, 130, "45", "missing RTs", "of 5,760 main trials", { fill: C.paleGray });
  addText(slide, "Pseudoword accuracy is lower than word accuracy, but still high enough to show nonword discrimination.", 560, 374, 290, 44, {
    fontSize: 13,
    color: C.navy,
    bold: true,
    alignment: "center",
  });
  addNotes(slide, "Use accuracy to support task validity. Word accuracy is high; pseudoword accuracy is lower, which is expected, but participants were not simply pressing one key.");
}

async function slide23(slide) {
  addTitle(slide, "INTERPRETATION", "The strongest preliminary story is frequency plus syllable length, with a tentative interaction.", 23);
  addCard(slide, 76, 142, 235, 130, "1. Frequency", "High-frequency words were responded to faster than low-frequency words.", { fill: C.paleGreen, bodySize: 14 });
  addCard(slide, 360, 142, 235, 130, "2. Syllable length", "Mean RT increased from one-syllable to four-syllable words.", { fill: C.paleBlue, bodySize: 14 });
  addCard(slide, 644, 142, 205, 130, "3. Interaction", "Possible variation in the frequency effect, but modest.", { fill: C.paleGray, bodySize: 13.5 });
  addRect(slide, 118, 330, 700, 72, { fill: C.paleGray, line: { color: C.navy, width: 0.8 } });
  addText(slide, "Cautious interpretation: lexical-decision RT reflects lexical processing plus task-decision processes, so the results should not be reduced to pure lexical access.", 144, 348, 648, 38, {
    fontSize: 15,
    color: C.navy,
    bold: true,
    alignment: "center",
  });
  addNotes(slide, "This is the interpretation slide. Keep the conclusion defensible: frequency and length are the main patterns, interaction is tentative, and lexical decision includes a decision stage.");
}

async function slide24(slide) {
  addTitle(slide, "LIMITATIONS", "The current analysis is ready for discussion, but not yet a final thesis conclusion.", 24);
  addBulletList(slide, [
    "N = 48 reaches the minimum target but is still a minimum sample.",
    "Pseudowords should be reviewed for plausibility and matching before final reporting.",
    "Frequency source and item matching may need dispersion/register checks.",
    "The current model uses random intercepts; richer structures can be tested if stable.",
    "The project does not solve full Vietnamese word segmentation.",
  ], 76, 132, 720, 48, { fontSize: 13.4 });
  addCard(slide, 90, 395, 740, 52, "Next analytical step", "Review diagnostics, check sensitivity decisions, consider supplementary accuracy models, and refine the interaction interpretation.", { fill: C.paleGreen, bodySize: 12.8 });
  addNotes(slide, "Limitations make the project stronger, not weaker. They show what has been controlled and what still needs careful follow-up.");
}

async function slide25(slide) {
  addTitle(slide, "TIMELINE", "The six-month plan moves from design and data collection toward final modeling and write-up.", 25);
  const months = [
    ["Month 1", "literature\nfinal RQ"],
    ["Month 2", "stimuli\npseudowords"],
    ["Month 3", "PsychoPy /\nPavlovia"],
    ["Month 4", "data\ncollection"],
    ["Month 5", "cleaning/QC\nR Markdown"],
    ["Month 6", "final models\nwrite-up"],
  ];
  addRule(slide, 108, 238, 680, C.lime, 3);
  months.forEach((m, i) => {
    const x = 75 + i * 135;
    addRect(slide, x + 48, 229, 18, 18, { fill: i <= 4 ? C.lime : C.white, line: { color: C.lime, width: 1.2 } });
    addText(slide, m[0], x, 170, 110, 22, { fontSize: 13, color: C.navy, bold: true, alignment: "center" });
    addText(slide, m[1], x, 198, 110, 44, { fontSize: 11, color: C.ink, alignment: "center" });
    addText(slide, i <= 4 ? "done / draft" : "next", x, 270, 110, 18, { fontSize: 9.5, color: i <= 4 ? C.lime : C.muted, bold: true, alignment: "center" });
  });
  addCard(slide, 130, 350, 635, 70, "Current position", "Data collection, cleaning, first R Markdown analysis, figures, tables, and diagnostics are ready. Final interpretation and write-up still need review.", { fill: C.paleBlue, bodySize: 13 });
  addNotes(slide, "Use this to show project management. The project is already beyond design and data collection; the remaining work is interpretation, robustness and writing.");
}

async function slide26(slide) {
  addTitle(slide, "REFERENCES I", "Selected sources for orthography, lexical decision, frequency, and methods.", 26);
  const refs = [
    "Baayen, R. H. (2008). Analyzing linguistic data. Cambridge University Press. https://doi.org/10.1017/CBO9780511801686",
    "Baayen, R. H., Davidson, D. J., & Bates, D. M. (2008). Mixed-effects modeling with crossed random effects. Journal of Memory and Language, 59(4), 390-412. https://doi.org/10.1016/j.jml.2007.12.005",
    "Balota, D. A., & Chumbley, J. I. (1984). Are lexical decisions a good measure of lexical access? JEP: HPP, 10(3), 340-357. https://doi.org/10.1037/0096-1523.10.3.340",
    "Bates, D., Mächler, M., Bolker, B., & Walker, S. (2015). Fitting linear mixed-effects models using lme4. Journal of Statistical Software, 67(1), 1-48. https://doi.org/10.18637/jss.v067.i01",
    "Brysbaert, M., Mandera, P., & Keuleers, E. (2018). The word frequency effect in word processing. Current Directions in Psychological Science, 27(1), 45-50. https://doi.org/10.1177/0963721417727521",
    "DeFrancis, J. (1977). Colonialism and language policy in Viet Nam. De Gruyter Mouton. https://doi.org/10.1515/9783110802405",
    "Encyclopaedia Britannica. (2026). Quoc-ngu. https://www.britannica.com/topic/Quoc-ngu",
    "Đinh, Q. T., Lê, H. P., Nguyễn, T. M. H., Nguyễn, C. T., Rossignol, M., & Vũ, X. L. (2008). Word segmentation of Vietnamese texts: A comparison of approaches. LREC 2008. https://aclanthology.org/L08-1355/",
    "Fernandes, G., & Assunção, C. (2017). First codification of Vietnamese by 17th-century missionaries. Histoire Épistémologie Langage, 39(1), 155-176. https://doi.org/10.3406/hel.2017.3592",
  ];
  refs.forEach((r, i) => {
    const col = i < 5 ? 0 : 1;
    const row = i < 5 ? i : i - 5;
    addText(slide, r, 58 + col * 420, 124 + row * 68, 390, 58, { fontSize: 8.2, color: C.ink });
  });
  addNotes(slide, "References are included for academic completeness. Do not read this slide aloud in detail.");
}

async function slide27(slide) {
  addTitle(slide, "REFERENCES II", "Selected sources for pseudowords, software, and RT handling.", 27);
  const refs = [
    "Ha, L. A. (2003). A method for word segmentation in Vietnamese. Proceedings of Corpus Linguistics 2003, 282-287.",
    "Keuleers, E., & Brysbaert, M. (2010). Wuggy: A multilingual pseudoword generator. Behavior Research Methods, 42(3), 627-633. https://doi.org/10.3758/BRM.42.3.627",
    "McKinney, W. (2010). Data structures for statistical computing in Python. Proceedings of the 9th Python in Science Conference, 56-61. https://doi.org/10.25080/Majora-92bf1922-00a",
    "Meyer, D. E., & Schvaneveldt, R. W. (1971). Facilitation in recognizing pairs of words. Journal of Experimental Psychology, 90(2), 227-234. https://doi.org/10.1037/h0031564",
    "New, B., Ferrand, L., Pallier, C., & Brysbaert, M. (2006). Reexamining the word length effect. Psychonomic Bulletin & Review, 13(1), 45-52. https://doi.org/10.3758/BF03193811",
    "Peirce, J. W., Gray, J. R., Simpson, S., MacAskill, M. R., Höchenberger, R., Sogo, H., Kastman, E., & Lindeløv, J. K. (2019). PsychoPy2. Behavior Research Methods, 51, 195-203. https://doi.org/10.3758/s13428-018-01193-y",
    "Pham, H., & Baayen, H. (2015). Vietnamese compounds show an anti-frequency effect in visual lexical decision. Language, Cognition and Neuroscience, 30(9), 1077-1095. https://doi.org/10.1080/23273798.2015.1054844",
    "Pham, H., Tucker, B. V., & Baayen, R. H. (2019). Constructing two Vietnamese corpora and building a lexical database. Language Resources and Evaluation, 53(3), 465-498. https://doi.org/10.1007/s10579-019-09451-x",
    "R Core Team. (2026). R: A language and environment for statistical computing. R Foundation for Statistical Computing. https://doi.org/10.32614/R.manuals",
    "Ratcliff, R. (1993). Methods for dealing with reaction time outliers. Psychological Bulletin, 114(3), 510-532. https://doi.org/10.1037/0033-2909.114.3.510",
    "Verdonschot, R. G., Hoàng, T. L. P., & Tamaoka, K. (2022). Phonological encoding in Vietnamese. Quarterly Journal of Experimental Psychology, 75(7), 1355-1366. https://doi.org/10.1177/17470218211053244",
    "Whelan, R. (2008). Effective analysis of reaction time data. The Psychological Record, 58(3), 475-482. https://doi.org/10.1007/BF03395630",
    "Yap, M. J., & Balota, D. A. (2009). Visual word recognition of multisyllabic words. Journal of Memory and Language, 60(4), 502-529. https://doi.org/10.1016/j.jml.2009.02.001",
  ];
  refs.forEach((r, i) => {
    const col = i < 7 ? 0 : 1;
    const row = i < 7 ? i : i - 7;
    addText(slide, r, 58 + col * 420, 118 + row * 50, 395, 42, { fontSize: 7.6, color: C.ink });
  });
  addText(slide, "Thank you.", 650, 448, 210, 34, { fontSize: 27, color: C.navy, bold: true, alignment: "right" });
  addNotes(slide, "Close briefly and invite questions about the design, QC, or model interpretation.");
}

const builders = [
  slide01, slide02, slide03, slide04, slide05, slide06, slide07, slide08, slide09,
  slide10, slide11, slide12, slide13, slide14, slide15, slide16, slide17, slide18,
  slide19, slide20, slide21, slide22, slide23, slide24, slide25, slide26, slide27,
];

const presentation = await PresentationFile.importPptx(await FileBlob.load(starterPptx));
if (presentation.slides.items.length !== builders.length) {
  throw new Error(`Expected ${builders.length} slides in starter, found ${presentation.slides.items.length}.`);
}

for (let i = 0; i < builders.length; i += 1) {
  const slide = presentation.slides.items[i];
  clearSlide(slide);
  await builders[i](slide);
}

await fs.mkdir(path.dirname(finalPptx), { recursive: true });
const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(finalPptx);
console.log(finalPptx);
