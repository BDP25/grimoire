import type { Meta, StoryObj } from "@storybook/html";
import { fn } from "@storybook/test";

import type { ButtonProps } from "./NeoButton";
import { createButton } from "./NeoButton";

const meta = {
  title: "Swisstination/Button",
  tags: ["autodocs"],
  render: (args) => {
    return createButton(args);
  },
  argTypes: {
    type: {
      control: "select",
      options: ["default", "rounded"]
    },
    color: {
      control: "select",
      options: ["violet", "pink", "red", "orange", "yellow", "lime", "cyan"]
    },
    label: {
      control: {
        type: "text"
      }
    }
  },
  args: { onClick: fn() }
} satisfies Meta<ButtonProps>;

export default meta;
type Story = StoryObj<ButtonProps>;

export const Primary: Story = {
  args: {
    type: "default",
    color: "cyan"
  }
};

export const Rounded: Story = {
  args: {
    type: "rounded",
    color: "cyan"
  }
};
