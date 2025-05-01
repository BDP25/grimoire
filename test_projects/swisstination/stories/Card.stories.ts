import type { Meta, StoryObj } from "@storybook/html";
import { fn } from "@storybook/test";

import type { CardProps } from "./Card";
import { createCard } from "./Card";

const meta = {
  title: "Swisstination/Card",
  tags: ["autodocs"],
  render: (args) => {
    return createCard(args);
  },
  argTypes: {
    image: {
      control: "text",
    },
    subtitle: {
      control: "text",
    },
    title: {
      control: "text",
    },
    text: {
      control: "text",
    },
  },
  args: { onClick: fn() },
} satisfies Meta<CardProps>;

export default meta;
type Story = StoryObj<CardProps>;

export const Default: Story = {
  args: {
    image: "https://picsum.photos/300/200",
    subtitle: "Subtitle",
    title: "Title",
    text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent sed felis sit amet massa porttitor dictum. Nullam pellentesque id nunc et dapibus. Nullam rhoncus vel nibh in feugiat. Nulla ut dignissim metus. Vestibulum et turpis ut massa fringilla lobortis id ut orci. Sed pellentesque nibh et congue vehicula.",
  },
};

export const NoImage: Story = {
  args: {
    subtitle: "Subtitle",
    title: "Title",
    text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent sed felis sit amet massa porttitor dictum. Nullam pellentesque id nunc et dapibus. Nullam rhoncus vel nibh in feugiat. Nulla ut dignissim metus. Vestibulum et turpis ut massa fringilla lobortis id ut orci. Sed pellentesque nibh et congue vehicula.",
  },
};

export const OnlyText: Story = {
  args: {
    text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent sed felis sit amet massa porttitor dictum. Nullam pellentesque id nunc et dapibus. Nullam rhoncus vel nibh in feugiat. Nulla ut dignissim metus. Vestibulum et turpis ut massa fringilla lobortis id ut orci. Sed pellentesque nibh et congue vehicula.",
  },
};
