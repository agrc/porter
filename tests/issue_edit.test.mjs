import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { getUpdatedIssueBody } from "../.github/scripts/issue_edit.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

test("updates a completed task line with a placeholder date", () => {
  const currentBody = "- [x] Append title (@stdavis, completed: `2026/00/00`)";

  const updatedBody = getUpdatedIssueBody({
    currentBody,
    currentDate: "2026/04/13",
  });

  assert.equal(
    updatedBody,
    "- [x] Append title (@stdavis, completed: `2026/04/13`)",
  );
});

test("updates a verification line with a placeholder date", () => {
  const currentBody =
    "- [x] [sgid-index](https://example.com) (@stdavis on `2026/00/00`)";

  const updatedBody = getUpdatedIssueBody({
    currentBody,
    currentDate: "2026/04/13",
  });

  assert.equal(
    updatedBody,
    "- [x] [sgid-index](https://example.com) (@stdavis on `2026/04/13`)",
  );
});

test("updates checked placeholder tasks even if they were already checked before the latest edit", () => {
  const currentBody = "- [x] Append title (@stdavis, completed: `2026/00/00`)";

  const updatedBody = getUpdatedIssueBody({
    currentBody,
    currentDate: "2026/04/13",
  });

  assert.equal(
    updatedBody,
    "- [x] Append title (@stdavis, completed: `2026/04/13`)",
  );
});

test("updates multiple checked placeholder tasks in one pass", () => {
  const currentBody = [
    "- [x] Existing task (@stdavis, completed: `2026/00/00`)",
    "- [x] New task (@stdavis, completed: `2026/00/00`)",
  ].join("\n");

  const updatedBody = getUpdatedIssueBody({
    currentBody,
    currentDate: "2026/04/13",
  });

  assert.equal(
    updatedBody,
    [
      "- [x] Existing task (@stdavis, completed: `2026/04/13`)",
      "- [x] New task (@stdavis, completed: `2026/04/13`)",
    ].join("\n"),
  );
});

test("does not update struck-through checked tasks", () => {
  const currentBody = "~- [x] Ignore me (@stdavis, completed: `2026/00/00`)~";

  const updatedBody = getUpdatedIssueBody({
    currentBody,
    currentDate: "2026/04/13",
  });

  assert.equal(updatedBody, currentBody);
});

test("does not update checked tasks without placeholder dates", () => {
  const currentBody = "- [x] Append title (@stdavis, completed: `2026/03/12`)";

  const updatedBody = getUpdatedIssueBody({
    currentBody,
    currentDate: "2026/04/13",
  });

  assert.equal(updatedBody, currentBody);
});

test("does not update unchecked tasks with placeholder dates", () => {
  const currentBody = "- [ ] Append title (@stdavis, completed: `2026/00/00`)";

  const updatedBody = getUpdatedIssueBody({
    currentBody,
    currentDate: "2026/04/13",
  });

  assert.equal(updatedBody, currentBody);
});

test("updates real Porter issue template content without touching unrelated placeholders", () => {
  const templatePath = path.join(
    __dirname,
    "..",
    ".github",
    "ISSUE_TEMPLATE",
    "6-deprecate-sgid-dataset.md",
  );
  const currentBody = fs
    .readFileSync(templatePath, "utf8")
    .replace(
      '- [ ] Append "(Mature Support)" to the end of the item title in the `SGID.META.AGOLItems` table (name, completed: `2026/00/00`)',
      '- [x] Append "(Mature Support)" to the end of the item title in the `SGID.META.AGOLItems` table (@stdavis, completed: `2026/00/00`)',
    )
    .replace(
      "- [ ] [sgid-index](https://gis.utah.gov/products/sgid/sgid-index/) (@stdavis on `2026/00/00`)",
      "- [x] [sgid-index](https://gis.utah.gov/products/sgid/sgid-index/) (@stdavis on `2026/00/00`)",
    );

  const updatedBody = getUpdatedIssueBody({
    currentBody,
    currentDate: "2026/04/13",
  });

  assert.match(
    updatedBody,
    /- \[x\] Append "\(Mature Support\)" to the end of the item title in the `SGID\.META\.AGOLItems` table \(@stdavis, completed: `2026\/04\/13`\)/,
  );
  assert.match(
    updatedBody,
    /- \[x\] \[sgid-index\]\(https:\/\/gis\.utah\.gov\/products\/sgid\/sgid-index\/\) \(@stdavis on `2026\/04\/13`\)/,
  );
  assert.match(
    updatedBody,
    /- \[ \] Remove all tags other than "Deprecated" in the SDE metadata \(name, completed: `2026\/00\/00`\)/,
  );
});