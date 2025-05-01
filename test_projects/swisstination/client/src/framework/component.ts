import { htmlToNode } from "./utils";

export abstract class Component extends HTMLElement {
  private initalized = false;
  private subsDeconstructors: (() => void)[] = [];

  constructor() {
    super();
    this.internalRender = this.internalRender.bind(this);
  }

  connectedCallback() {
    this.internalInit();
  }
  disconnectedCallback() {
    this.internalUnmount();
  }

  attributeChangedCallback() {
    this.internalRender();
  }

  private internalInit() {
    const shadowRoot = this.attachShadow({ mode: "open" });

    // Inject existing styles into shadow dom
    const styles = [].slice.call(
      document.getElementsByTagName("style")
    ) as HTMLStyleElement[];
    styles.forEach((style) => shadowRoot.appendChild(style.cloneNode(true)));

    // Content placeholder
    const contentPlaceholder = document.createElement("div");
    contentPlaceholder.innerHTML = "Placeholder";
    shadowRoot.appendChild(contentPlaceholder);

    this.init();
    this.subsDeconstructors = this.componentInitSubs();
    this.initalized = true;

    this.internalRender();
    this.componentDidMount();
  }
  private internalUnmount() {
    this.subsDeconstructors.forEach((decon) => decon());
    this.componentWillUnmount();
  }
  protected internalRender() {
    if (!this.initalized) return;

    const rawOutput = this.render();

    let content = null;
    if (typeof rawOutput == "string") {
      content = htmlToNode(rawOutput);
    } else {
      content = rawOutput as HTMLElement;
    }

    this.shadowRoot!.replaceChild(content, this.shadowRoot!.lastChild!);
  }

  protected init(): void {}
  protected componentInitSubs(): (() => void)[] {
    return [];
  }
  protected componentDidMount(): void {}
  protected componentWillUnmount(): void {}
  protected abstract render(): HTMLElement | string;
}

export function registerComponent<T extends HTMLElement>(
  tagName: string,
  component: new (...params: any[]) => T
) {
  customElements.define(tagName, component);
}
