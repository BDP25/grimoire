// Source: https://stackoverflow.com/questions/9899372/vanilla-javascript-equivalent-of-jquerys-ready-how-to-call-a-function-whe
export function documentReady(fn: (this: Document, ev: Event) => any) {
  if (
    document.readyState === "complete" ||
    document.readyState === "interactive"
  ) {
    setTimeout(fn, 1);
  } else {
    document.addEventListener("DOMContentLoaded", fn);
  }
}

// source: https://stackoverflow.com/questions/494143/creating-a-new-dom-element-from-an-html-string-using-built-in-dom-methods-or-pro
export function htmlToNode(html: string) {
  const template = document.createElement("template");
  template.innerHTML = html.trim();
  const nNodes = template.content.childNodes.length;
  if (nNodes !== 1) {
    throw new Error(
      `html parameter must represent a single node; got ${nNodes}. ` +
        "Note that leading or trailing spaces around an element in your " +
        'HTML, like " <img/> ", get parsed as text nodes neighbouring ' +
        "the element; call .trim() on your input to avoid this."
    );
  }
  return template.content.firstChild!;
}

export function formatDuration(duration: number): string {
  if (duration < 60) {
    return `${duration} min`;
  } else if (duration < 1440) {
    const hours = Math.floor(duration / 60);
    const minutes = duration % 60;
    return minutes ? `${hours}h ${minutes}min` : `${hours}h`;
  } else {
    const days = Math.floor(duration / 1440);
    const hours = Math.floor((duration % 1440) / 60);
    return hours ? `${days}d ${hours}h` : `${days}d`;
  }
}
