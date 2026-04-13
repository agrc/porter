const CHECKED_TASK_PATTERN = /^\s*[-*]\s*\[[xX]\]\s+/;
const PLACEHOLDER_DATE_PATTERN = /`\d{4}\/00\/00`/;
const COMPLETED_PATTERN =
  /(\([^\n)]*,\s*completed:\s*)`\d{4}\/\d{2}\/\d{2}`(\))/;
const VERIFIED_PATTERN = /(\([^\n)]*\s+on\s*)`\d{4}\/\d{2}\/\d{2}`(\))/;

export function isCheckedTask(line) {
  return CHECKED_TASK_PATTERN.test(line);
}

export function isStruckThroughTask(line) {
  return /~\s*$/.test(line) || /^\s*~.*~\s*$/.test(line);
}

export function hasPlaceholderDate(line) {
  return PLACEHOLDER_DATE_PATTERN.test(line);
}

export function applyCompletionDate(line, currentDate) {
  const completedLine = line.replace(
    COMPLETED_PATTERN,
    `$1\`${currentDate}\`$2`,
  );

  if (completedLine !== line) {
    return completedLine;
  }

  return line.replace(VERIFIED_PATTERN, `$1\`${currentDate}\`$2`);
}

export function getUpdatedIssueBody({ currentBody, currentDate }) {
  const currentLines = currentBody.split("\n");

  const updatedLines = currentLines.map((currentLine) => {
    if (
      !isCheckedTask(currentLine) ||
      isStruckThroughTask(currentLine) ||
      !hasPlaceholderDate(currentLine)
    ) {
      return currentLine;
    }

    return applyCompletionDate(currentLine, currentDate);
  });

  return updatedLines.join("\n");
}