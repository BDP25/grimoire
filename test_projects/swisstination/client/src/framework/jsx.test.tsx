import { h, Fragment } from "./jsx";
import { expect, test } from "vitest";

function HTML(element: any) {
  return element.outerHTML;
}

test("simple text with class", () => {
  const output = <p className="blah">Hello world!</p>;
  const expectedHTML = `<p class="blah">Hello world!</p>`;
  expect(HTML(output)).eq(expectedHTML);
});

test("multiple children", () => {
  const output = (
    <div>
      <div id="child-one"></div>
      <div id="child-two"></div>
    </div>
  );
  const expectedHTML = `<div><div id="child-one"></div><div id="child-two"></div></div>`;
  expect(HTML(output)).eq(expectedHTML);
});

test("jsx with map", () => {
  const output = (
    <ul>
      {[1, 2, 3, 4].map((i) => (
        <li>{i}</li>
      ))}
    </ul>
  );
  const expectedHTML = `<ul><li>1</li><li>2</li><li>3</li><li>4</li></ul>`;
  expect(HTML(output)).eq(expectedHTML);
});

class TestComplexAttributeComponent extends HTMLElement {
  public example?: { hello: string };

  constructor() {
    super();
  }
}
customElements.define("test-complex-elm", TestComplexAttributeComponent);

test("passing objects as attributes", () => {
  const data = {
    hello: "WORLD!!!",
  };
  const output = (
    <test-complex-elm data-example={data} />
  ) as unknown as TestComplexAttributeComponent;
  expect(output.example).eq(data);
});
