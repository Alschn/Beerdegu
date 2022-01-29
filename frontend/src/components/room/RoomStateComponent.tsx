import Waiting from "./Waiting";
import SearchAPI from "./SearchAPI";
import BeerFormStepper from "./BeerFormStepper";
import ResultsStepper from "./ResultsStepper";
import {FC} from "react";
import {roomStateType} from "../../context/roomContext";

const RoomStateComponent: FC<{ state: roomStateType }> = ({state}) => {
  switch (state) {
    case "WAITING":
      return <Waiting/>;
    case "STARTING":
      return <SearchAPI/>;
    case "IN_PROGRESS":
      return <BeerFormStepper/>;
    case "FINISHED":
      return <ResultsStepper/>;
    default:
      return <></>;
  }
};

export default RoomStateComponent;
