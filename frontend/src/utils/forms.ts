import {FormEvent, KeyboardEvent} from "react";

export const onSubmit = (e: FormEvent, submitCallback: () => void) => {
  e.preventDefault();
  submitCallback();
};

export const submitWithEnter = (e: KeyboardEvent, submitCallback: () => void) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    submitCallback();
  }
};
