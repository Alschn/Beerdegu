import {Grid, MenuItem, TextField} from "@material-ui/core";
import React, {FC, Fragment, useEffect, useReducer} from "react";
import "./Form.scss";
import useWebSocket from "react-use-websocket";
import {useRoomContext} from "../../hooks/useContextHook";
import {UserRatingsObject, WebsocketMessage} from "../../utils/ws";

type State = UserRatingsObject;

type Action =
  { type: 'INPUT_CHANGE', field: string, payload: string | number } |
  { type: 'FETCH_FORM_DATA', payload: State }

const formReducer = (state: State, action: Action): State => {
  switch (action.type) {
    case "INPUT_CHANGE":
      return {
        ...state,
        [action.field]: action.payload,
      };
    case "FETCH_FORM_DATA":
      return {
        ...action.payload
      }
    default:
      return state;
  }
};

interface BeerFormProps {
  beerID: number;
}

const initialState = {
  color: "",
  smell: "",
  foam: "",
  taste: "",
  opinion: "",
  note: 1,
};

const FORM_SAVE_INTERVAL_MS = 5_000;

const notes: number[] = Array.from({length: 10}, (_, i) => i + 1);

const BeerForm: FC<BeerFormProps> = ({beerID}) => {
  const {code} = useRoomContext();
  const [state, dispatch] = useReducer(formReducer, initialState);

  const {
    sendJsonMessage,
  } = useWebSocket(`ws://127.0.0.1:8000/ws/room/${code}/`, {
    shouldReconnect: () => true,
    share: true,
    onMessage: (event) => {
      const parsed: WebsocketMessage = JSON.parse(event.data);
      if (parsed.command === 'set_form_data') {
        dispatch({
          type: 'FETCH_FORM_DATA',
          payload: parsed.data
        });
      }
    }
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>): void => {
    dispatch({
      type: 'INPUT_CHANGE',
      field: e.target.name,
      payload: e.target.value,
    });
  };

  useEffect(() => {
    sendJsonMessage({
      command: 'get_form_data',
      data: beerID
    })
  }, [sendJsonMessage, beerID])

  useEffect(() => {
    // save form so that users do not lose fields they filled
    // in case they got disconnected
    const formSaveInterval = setInterval(() => {
      sendJsonMessage({
        command: 'user_form_save',
        data: {
          ...state,
          beer_id: beerID,
        },
      });
    }, FORM_SAVE_INTERVAL_MS);
    return () => clearInterval(formSaveInterval);
  }, [state, sendJsonMessage, beerID])

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
          InputLabelProps={{
            shrink: true,
          }}
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
