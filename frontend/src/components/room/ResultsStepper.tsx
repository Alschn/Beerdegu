import React, {FC, useState} from 'react';
import {useTheme} from '@material-ui/core/styles';
import MobileStepper from '@material-ui/core/MobileStepper';
import Button from '@material-ui/core/Button';
import KeyboardArrowLeft from '@material-ui/icons/KeyboardArrowLeft';
import KeyboardArrowRight from '@material-ui/icons/KeyboardArrowRight';
import UserRatingsTable from "./UserRatingsTable";
import BeerRatingsTable from "./BeerRatingsTable";
import {useRoomContext} from "../../hooks/useContextHook";

const ResultsStepper: FC = () => {
  const {results} = useRoomContext();
  const theme = useTheme();

  const [activeStep, setActiveStep] = useState<number>(0);

  const handleNext = () => setActiveStep((prevActiveStep) => prevActiveStep + 1);
  const handleBack = () => setActiveStep((prevActiveStep) => prevActiveStep - 1);

  return (
    <div className='results-stepper' style={{flexGrow: 1}}>
      <div className='results-stepper-header'
           style={{textAlign: 'center'}}>
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
            {theme.direction === 'rtl' ? <KeyboardArrowRight/> : <KeyboardArrowLeft/>}
            Twoje oceny
          </Button>
        }
        nextButton={
          <Button
            size="small" onClick={handleNext}
            disabled={activeStep === 1 || results.length === 0}
          >
            Wyniki
            {theme.direction === 'rtl' ? <KeyboardArrowLeft/> : <KeyboardArrowRight/>}
          </Button>
        }
      />

      {activeStep === 0 ? (
        <UserRatingsTable/>
      ) : (
        <BeerRatingsTable/>
      )}
    </div>
  );
}

export default ResultsStepper;
