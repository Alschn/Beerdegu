import {expect} from 'vitest';
import {render, screen} from "./utils";
import Browser from "../pages/Browser";

it('should add 2 numbers', () => {
  expect(1 + 1).toEqual(2);
});

it('should render a component', () => {
  render(<Browser/>);
  expect(screen.getByText('Not implemented yet')).toBeDefined();
});
