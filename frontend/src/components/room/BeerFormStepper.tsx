import {FC, useState} from 'react';
import KeyboardArrowLeft from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRight from '@mui/icons-material/KeyboardArrowRight';
import BeerForm from "./Form";
import {Button, Grid, MobileStepper} from '@mui/material';
import {useRoomContext} from "../../hooks/useContextHook";
import "./BeerFormStepper.scss";


const BeerFormStepper: FC = () => {
  const {beers} = useRoomContext();

  const [activeStep, setActiveStep] = useState<number>(0);
  const maxSteps = beers.length;

  const handleNext = (): void => setActiveStep((prevActiveStep) => prevActiveStep + 1);

  const handleBack = (): void => setActiveStep((prevActiveStep) => prevActiveStep - 1);

  if (maxSteps === 0) return null;

  return (
    <div className="beer-form-stepper-root">
      <MobileStepper
        steps={maxSteps}
        position="static"
        variant="text"
        activeStep={activeStep}
        nextButton={
          <Button size="small" onClick={handleNext} disabled={activeStep === maxSteps - 1}>
            Następne
            <KeyboardArrowRight/>
          </Button>
        }
        backButton={
          <Button size="small" onClick={handleBack} disabled={activeStep === 0}>
            <KeyboardArrowLeft/>
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
          <p><strong>Zawartość alkoholu:</strong> {beers[activeStep].percentage}%</p>
          <p><strong>Ekstrakt [°BLG]:</strong> {beers[activeStep].extract}</p>
          <p><strong>Goryczka [IBU]:</strong> {beers[activeStep].IBU}</p>
          <p><strong>Hoprate [g/L]:</strong> {beers[activeStep].hop_rate}</p>
          <p><strong>Opis:</strong> {beers[activeStep].description}</p>
        </Grid>
      </Grid>

      <BeerForm
        beerID={beers[activeStep].id}
      />
    </div>
  );
};

export default BeerFormStepper;
