import type { Meta, StoryObj } from "@storybook/html";

import type { BadgeProps } from "./NeoBadge";
import { createBadge } from "./NeoBadge";

const meta = {
  title: "Swisstination/Badge",
  tags: ["autodocs"],
  render: (args) => {
    return createBadge(args);
  },
  argTypes: {
    color: {
      control: "select",
      options: ["violet", "pink", "red", "orange", "yellow", "lime", "cyan"]
    },
    label: {
      control: {
        type: "text"
      }
    }
  }
} satisfies Meta<BadgeProps>;

export default meta;
type Story = StoryObj<BadgeProps>;

export const Default: Story = {
  args: {
    color: "cyan"
  }
};
