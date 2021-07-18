import React, {FC, useState} from 'react';
import {useTheme} from '@material-ui/core/styles';
import MobileStepper from '@material-ui/core/MobileStepper';
import Button from '@material-ui/core/Button';
import KeyboardArrowLeft from '@material-ui/icons/KeyboardArrowLeft';
import KeyboardArrowRight from '@material-ui/icons/KeyboardArrowRight';
import BeerForm from "./Form";
import {Grid} from '@material-ui/core';
import "./BeerFormStepper.scss";

interface BeerObject {
  id: number,
  name: string,
  percentage: number,
  volume_ml: number,
  image?: string,
  description?: string,
  brewery?: any,
  style?: any,
  hops: any[]
}

interface StepperProps {
  beers: BeerObject[]
}

const BeerFormStepper: FC<StepperProps> = ({beers}) => {
  const theme = useTheme();

  const [activeStep, setActiveStep] = useState<number>(0);
  const maxSteps = beers.length;

  const handleNext = () => setActiveStep((prevActiveStep) => prevActiveStep + 1);

  const handleBack = () => setActiveStep((prevActiveStep) => prevActiveStep - 1);

  if (maxSteps === 0) return null;

  return (
    <div className='beer-form-stepper-root'>
      <MobileStepper
        steps={maxSteps}
        position="static"
        variant="text"
        activeStep={activeStep}
        nextButton={
          <Button size="small" onClick={handleNext} disabled={activeStep === maxSteps - 1}>
            Następne
            {theme.direction === 'rtl' ? <KeyboardArrowLeft/> : <KeyboardArrowRight/>}
          </Button>
        }
        backButton={
          <Button size="small" onClick={handleBack} disabled={activeStep === 0}>
            {theme.direction === 'rtl' ? <KeyboardArrowRight/> : <KeyboardArrowLeft/>}
            Poprzednie
          </Button>
        }
      />

      <Grid container className="beer-info-wrapper">
        <Grid item xs={2} className="beer-info-image">
          <img
            src={beers[activeStep].image}
            alt={beers[activeStep].name}
          />
        </Grid>

        <Grid item xs={10} className="beer-info-details">
          <p><strong>Nazwa:</strong> {beers[activeStep].name}</p>
          <p><strong>Browar:</strong> {beers[activeStep].brewery}</p>
          <p><strong>Styl:</strong> {beers[activeStep].style}</p>
          <p><strong>Opis:</strong> {beers[activeStep].description}</p>
        </Grid>
      </Grid>

      <BeerForm
        beerID={beers[activeStep].id}
      />
    </div>
  );
}

export default BeerFormStepper;