import {Grid, MenuItem, TextField} from "@material-ui/core";
import React, {FC, Fragment, useEffect, useReducer} from "react";
import "./Form.scss";

interface State {
  color: string,
  smell: string,
  foam: string,
  taste: string,
  opinion: string,
  note: number | null
}

type Action =
  { type: 'INPUT_CHANGE', field: string, payload: string | number }

const formReducer = (state: State, action: Action): State => {
  switch (action.type) {
    case "INPUT_CHANGE":
      return {
        ...state,
        [action.field]: action.payload,
      };
    default:
      return state;
  }
};

interface BeerFormProps {
  sendMessage: (data: { command: string, data: State, }) => void;
}

const initialState = {
  color: "",
  smell: "",
  foam: "",
  taste: "",
  opinion: "",
  note: null,
};

const FORM_SAVE_INTERVAL_MS = 30_000;

const notes: number[] = Array.from({length: 10}, (_, i) => i + 1);

const BeerForm: FC<BeerFormProps> = ({sendMessage}) => {
  const [state, dispatch] = useReducer(formReducer, initialState);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    dispatch({
      type: 'INPUT_CHANGE',
      field: e.target.name,
      payload: e.target.value,
    });
  };

  useEffect(() => {
    // save form so that users do not lose fields they filled
    // in case they got disconnected
    const formSaveInterval = setInterval(() => {
      sendMessage({
        command: 'user_form_save',
        data: state,
      });
    }, FORM_SAVE_INTERVAL_MS);
    return () => clearInterval(formSaveInterval);
  }, [state, sendMessage])

  return (
    <Fragment>
      <Grid item xs={12} className="form-textfield-wrapper">
        <TextField
          id="colorTextField"
          name="color"
          label="Kolor"
          variant="outlined"
          multiline
          rows={2}
          value={state.color}
          onChange={handleInputChange}
        />
      </Grid>

      <Grid item xs={12} className="form-textfield-wrapper">
        <TextField
          id="foamTextField"
          name="foam"
          label="Piana"
          variant="outlined"
          multiline
          rows={2}
          value={state.foam}
          onChange={handleInputChange}
        />
      </Grid>

      <Grid item xs={12} className="form-textfield-wrapper">
        <TextField
          id="smellTextField"
          name="smell"
          label="Zapach"
          variant="outlined"
          multiline
          rows={2}
          value={state.smell}
          onChange={handleInputChange}
        />
      </Grid>

      <Grid item xs={12} className="form-textfield-wrapper">
        <TextField
          id="tasteTextField"
          name="taste"
          label="Smak"
          variant="outlined"
          multiline
          rows={2}
          value={state.taste}
          onChange={handleInputChange}
        />
      </Grid>

      <Grid item xs={12} className="form-textfield-wrapper">
        <TextField
          id="opinionTextField"
          name="opinion"
          label="Opinia"
          variant="outlined"
          multiline
          rows={2}
          value={state.opinion}
          onChange={handleInputChange}
        />
      </Grid>

      <Grid item xs={12} className="form-textfield-wrapper">
        <TextField
          id="noteSelectField"
          select
          name="note"
          label="Ocena"
          variant="outlined"
          multiline
          value={state.note}
          onChange={handleInputChange}
        >
          {notes.map(int => (
            <MenuItem key={`note=${int}`} value={int}>
              {int}
            </MenuItem>
          ))}
        </TextField>
      </Grid>
    </Fragment>
  );
};

export default BeerForm;
