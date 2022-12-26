import {FC, useRef, useState} from 'react';
import {Button, MobileStepper} from '@mui/material';
import KeyboardArrowLeft from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRight from '@mui/icons-material/KeyboardArrowRight';
import UserRatingsTable from "./UserRatingsTable";
import BeerRatingsTable from "./BeerRatingsTable";
import {useRoomContext} from "../../hooks/useContextHook";
import {useMutation} from "react-query";
import {generateReport} from "../../api/rooms";
import "./ResultsStepper.scss";

const ResultsStepper: FC = () => {
  const {code, results} = useRoomContext();

  const [activeStep, setActiveStep] = useState<number>(0);

  const handleNext = () => setActiveStep((prevActiveStep) => prevActiveStep + 1);
  const handleBack = () => setActiveStep((prevActiveStep) => prevActiveStep - 1);

  const tableRef = useRef(null);

  const mutation = useMutation(
    () => generateReport(code), {
      onSuccess: (response) => {
        const contentDisposition = response.headers['content-disposition'];
        const filename = contentDisposition.split(';')[1].split('=')[1];
        const cleanedFilename = filename.replace(/"/g, '');

        // create file link in browser's memory
        const href = URL.createObjectURL(response.data);

        // create "a" HTLM element with href to file & click
        const link = document.createElement('a');
        link.href = href;
        link.setAttribute('download', cleanedFilename);
        document.body.appendChild(link);
        link.click();

        // clean up "a" element & remove ObjectURL
        document.body.removeChild(link);
        URL.revokeObjectURL(href);
      }
    }
  );

  return (
    <div className="results-stepper">
      <div className="results-stepper-header">
        <h1>Degustacja zakończyła się!</h1>
      </div>

      <MobileStepper
        steps={2}
        position="static"
        variant="text"
        activeStep={activeStep}
        backButton={
          <Button
            size="small" onClick={handleBack}
            disabled={activeStep === 0}
          >
            <KeyboardArrowLeft/>
            <strong>Twoje oceny</strong>
          </Button>
        }
        nextButton={
          <Button
            size="small" onClick={handleNext}
            disabled={activeStep === 1 || results.length === 0}
          >
            <strong>Wyniki</strong>
            <KeyboardArrowRight/>
          </Button>
        }
      />

      <div id="ratings-table-to-pdf" ref={tableRef}>
        {activeStep === 0 ? (
          <UserRatingsTable/>
        ) : (
          <BeerRatingsTable/>
        )}
      </div>

      <div className="results-pdf-button">
        <Button
          onClick={() => mutation.mutate()}
          variant="contained"
          color="primary"
        >
          Zapisz wyniki
        </Button>
      </div>
    </div>
  );
};

export default ResultsStepper;
