import fs from "node:fs/promises";
import path from "node:path";

const workspace = "D:/Research 2/outputs/019ebd7f-43a3-77c1-a64d-f9a3f17282cf/presentations/rp2-colloquium2-vietnamese-ldt";
const inspectPath = path.join(workspace, "template-inspect", "template-inspect.ndjson");
const outPath = path.join(workspace, "template-frame-map.json");

const slideSpecs = [
  [1, "opening thesis", 3],
  [2, "story arc and contents", 3],
  [3, "orthography timeline evidence", 3],
  [4, "tokenization problem map", 3],
  [5, "scope boundary and project contribution", 3],
  [6, "research question and hypotheses", 3],
  [7, "balanced design matrix", 3],
  [8, "stimulus construction and pseudoword proof", 3],
  [9, "task procedure flow", 3],
  [10, "bias controls and monitoring", 3],
  [11, "experiment demo placeholder", 6],
  [12, "methodology pipeline", 3],
  [13, "cleaning and quality-control method", 3],
  [14, "data quality evidence", 3],
  [15, "reproducibility architecture", 3],
  [16, "analysis plan and log RT rationale", 3],
  [17, "mixed-effects model proof", 3],
  [18, "descriptive RT evidence", 3],
  [19, "interaction evidence", 3],
  [20, "model comparison evidence", 3],
  [21, "diagnostics evidence", 3],
  [22, "accuracy and response-quality evidence", 3],
  [23, "cautious interpretation", 3],
  [24, "limitations and next steps", 3],
  [25, "six-month timeline", 3],
  [26, "references page 1", 3],
  [27, "references page 2 and closing", 3],
];

const lines = (await fs.readFile(inspectPath, "utf8")).split(/\r?\n/).filter(Boolean);
const idsBySlide = new Map();
for (const line of lines) {
  const rec = JSON.parse(line);
  if (!Number.isInteger(rec.slide)) continue;
  if (!idsBySlide.has(rec.slide)) idsBySlide.set(rec.slide, []);
  if ((rec.kind === "textbox" || rec.kind === "shape" || rec.kind === "table" || rec.kind === "image") && rec.id) {
    idsBySlide.get(rec.slide).push(rec.id);
  }
}

function inheritedTargetsFor(sourceSlide) {
  const ids = idsBySlide.get(sourceSlide) || [];
  if (ids.length === 0) {
    return [{ action: "delete", sourceElementId: `source-${sourceSlide}-placeholder-cleanup` }];
  }
  return ids.map((id) => ({ action: "delete", sourceElementId: id }));
}

const outputSlides = slideSpecs.map(([outputSlide, narrativeRole, sourceSlide]) => ({
  outputSlide,
  sourceSlide,
  narrativeRole,
  reuseMode: "duplicate-slide",
  editTargets: [
    ...inheritedTargetsFor(sourceSlide),
    {
      action: "add",
      newPrimitiveAllowed: true,
      mustNotOverlapInherited: true,
      zone: { left: 40, top: 40, width: 865, height: 435 },
      reason: "Add project-specific editable academic content within the clean content zone after inherited placeholders are removed.",
    },
  ],
}));

const used = new Set(slideSpecs.map((spec) => spec[2]));
const omittedSourceSlides = [1, 2, 3, 4, 5, 6, 7]
  .filter((slide) => !used.has(slide))
  .map((sourceSlide) => ({ sourceSlide, reason: "Not needed as a distinct final frame." }));

const map = { outputSlides, omittedSourceSlides };
await fs.writeFile(outPath, `${JSON.stringify(map, null, 2)}\n`, "utf8");
console.log(outPath);
