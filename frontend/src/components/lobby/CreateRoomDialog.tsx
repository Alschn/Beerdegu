import {Dialog} from "@material-ui/core";
import {Dispatch, FC} from "react";
import CreateRoom from "../pages/CreateRoom";

interface CreateRoomDialogProps {
  isOpen: boolean,
  dispatch: Dispatch<any>
}

const CreateRoomDialog: FC<CreateRoomDialogProps> = ({isOpen, dispatch}) => {
  return (
    <Dialog open={isOpen} onClose={() => dispatch({
      type: "CLOSE_CREATE_DIALOG",
      payload: false,
    })}>
      <CreateRoom isRoute={false}/>
    </Dialog>
  );
};

export default CreateRoomDialog;
