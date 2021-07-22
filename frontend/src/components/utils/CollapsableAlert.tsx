import {Collapse} from "@material-ui/core";
import {Alert} from "@material-ui/lab";
import React, {FC, useEffect, useState} from "react";

export interface AlertContentObject {
  message: string,
  severity?: 'error' | 'success',
}

interface CollapsableAlertProps {
  content: AlertContentObject,
}

const CollapsableAlert: FC<CollapsableAlertProps> = ({content}) => {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (content.message !== "") setOpen(true);
  }, [content])

  return (
    <Collapse in={open}>
      {
        content.message && (
          <Alert
            severity={content.severity}
            onClose={() => setOpen(false)}
            style={{margin: 10}}
          >
            {content.message}
          </Alert>
        )
      }
    </Collapse>
  );
};

export default CollapsableAlert;
