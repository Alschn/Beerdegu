import Waiting from "./Waiting";
import SearchAPI from "./SearchAPI";
import BeerFormStepper from "./BeerFormStepper";
import ResultsStepper from "./ResultsStepper";
import {FC} from "react";
import {RoomStateType} from "../../context/RoomContext";

const RoomStateComponent: FC<{ state: RoomStateType }> = ({state}) => {
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
      return null;
  }
};

export default RoomStateComponent;
