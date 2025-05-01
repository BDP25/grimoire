export type BadgeProps = {
  color?: "violet" | "pink" | "red" | "orange" | "yellow" | "lime" | "cyan";
  label?: string;
};

export const createBadge = ({
  color = "cyan",
  label = "Badge",
}: BadgeProps) => {
  const badge = document.createElement("neon-badge");
  badge.setAttribute("label", label);
  badge.setAttribute("color", color);
  return badge;
};
