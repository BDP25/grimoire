export type ButtonProps = {
  type?: "default" | "rounded";
  color?: "violet" | "pink" | "red" | "orange" | "yellow" | "lime" | "cyan";
  label?: string;
  onClick?: () => void;
};

export const createButton = ({
  type = "default",
  color = "cyan",
  label = "Button",
  onClick,
}: ButtonProps) => {
  const btn = document.createElement("neon-button");
  btn.innerText = label;
  btn.setAttribute("color", color);
  btn.setAttribute("variant", type);
  if (onClick) btn.addEventListener("click", onClick);
  return btn;
};
