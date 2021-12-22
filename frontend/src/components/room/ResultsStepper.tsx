import React, {FC, useRef, useState} from 'react';
import {Button, MobileStepper} from '@mui/material';
import KeyboardArrowLeft from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRight from '@mui/icons-material/KeyboardArrowRight';
import UserRatingsTable from "./UserRatingsTable";
import BeerRatingsTable from "./BeerRatingsTable";
import {useRoomContext} from "../../hooks/useContextHook";
import exportToPdf from "../../utils/exportToPDF";
import "./ResultsStepper.scss";

const ResultsStepper: FC = () => {
  const {results} = useRoomContext();

  const [activeStep, setActiveStep] = useState<number>(0);

  const handleNext = () => setActiveStep((prevActiveStep) => prevActiveStep + 1);
  const handleBack = () => setActiveStep((prevActiveStep) => prevActiveStep - 1);

  const tableRef = useRef(null);

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
          onClick={() => exportToPdf(tableRef)}
          variant="contained"
          color="primary"
        >
          Export to PDF
        </Button>
      </div>
    </div>
  );
};

export default ResultsStepper;
