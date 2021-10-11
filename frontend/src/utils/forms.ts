import React from "react";

export const onSubmit = (e: React.FormEvent, submitCallback: () => void) => {
  e.preventDefault();
  submitCallback();
};

export const submitWithEnter = (e: React.KeyboardEvent, submitCallback: () => void) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    submitCallback();
  }
};
