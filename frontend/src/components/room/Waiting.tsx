import {FC} from "react";
import {useRoomContext} from "../../hooks/useContextHook";


const Waiting: FC = () => {
  const {roomState} = useRoomContext();

  return (
    <div>
      <div style={{display: 'flex', justifyContent: 'center'}}>
        <h2>Stan: {roomState}</h2>
      </div>

      <div style={{display: 'flex', justifyContent: 'center'}}>
        <h3>⌛ Oczekiwanie na uczestników...</h3>
      </div>
    </div>
  );
};

export default Waiting;
