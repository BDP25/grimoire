export type Tag = Function | string;
export type Props = Record<string, string> | null;
export type Children = (Node | string)[];

declare global {
  namespace JSX {
    interface Element extends HTMLElement {}
    interface IntrinsicElements {
      [elemName: string]: any;
    }
  }
}

function appendChild(parent: HTMLElement, child: Node | any) {
  if (Array.isArray(child)) {
    child.forEach((nestedChild) => appendChild(parent, nestedChild));
    return;
  }
  parent.appendChild(child?.nodeType ? child : document.createTextNode(child));
}

export function h(tag: Tag, props: Props, ...children: Children) {
  if (typeof tag === "function") return tag(props, children);

  const element = document.createElement(tag);

  // Add attributes, events and classes
  Object.entries(props || {}).forEach(([name, value]) => {
    if (name.startsWith("on")) {
      element.addEventListener(name.toLowerCase().substr(2), value as any);
    } else if (name === "className") {
      const classes = ((value as string) || "")
        .trim()
        .split(" ")
        .filter((c) => c);
      classes.forEach((c) => element.classList.add(c));
    } else if (name.startsWith("data-")) {
      // Complex object cannot be set via attribute
      (element as any)[name.replace("data-", "")] = value;
    } else {
      element.setAttribute(name, value.toString());
    }
  });

  // Append child elements into the parent
  children.forEach((child) => {
    appendChild(element, child);
  });

  return element;
}

export function Fragment(props: Props, ...children: Children) {
  return children;
}
