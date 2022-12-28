import {Dialog} from "@mui/material";
import {Dispatch, FC} from "react";
import JoinRoom from "../../pages/JoinRoom";

interface JoinRoomDialogProps {
  roomName: string | null,
  isOpen: boolean,
  dispatch: Dispatch<any>
}

const JoinRoomDialog: FC<JoinRoomDialogProps> = ({isOpen, roomName, dispatch}) => {
  if (roomName == null) return null;

  const handleClose = () => dispatch({
    type: "CLOSE_JOIN_DIALOG",
    payload: false,
  });

  return (
    <Dialog
      open={isOpen}
      onClose={handleClose}
      style={{overflow: 'hidden'}}
    >
      <JoinRoom
        roomNameProp={roomName}
        isRoute={false}
      />
    </Dialog>
  );
};

export default JoinRoomDialog;
