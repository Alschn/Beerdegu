import {Dialog} from "@mui/material";
import {Dispatch, FC} from "react";
import CreateRoom from "../../pages/CreateRoom";

interface CreateRoomDialogProps {
  isOpen: boolean,
  dispatch: Dispatch<any>
}

const CreateRoomDialog: FC<CreateRoomDialogProps> = ({isOpen, dispatch}) => {
  const handleClose = () => dispatch({
    type: "CLOSE_CREATE_DIALOG",
    payload: false,
  });

  return (
    <Dialog
      open={isOpen}
      onClose={handleClose}
    >
      <CreateRoom isRoute={false}/>
    </Dialog>
  );
};

export default CreateRoomDialog;
