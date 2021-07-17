import React, {FC, useState} from 'react';
import {createStyles, makeStyles, Theme, useTheme} from '@material-ui/core/styles';
import MobileStepper from '@material-ui/core/MobileStepper';
import Button from '@material-ui/core/Button';
import KeyboardArrowLeft from '@material-ui/icons/KeyboardArrowLeft';
import KeyboardArrowRight from '@material-ui/icons/KeyboardArrowRight';
import BeerForm from "./Form";
import {Grid} from '@material-ui/core';

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      flexGrow: 1,
    },
    header: {
      display: 'flex',
      alignItems: 'center',
      height: 50,
      paddingLeft: theme.spacing(4),
      backgroundColor: theme.palette.background.default,
    },
    img: {
      height: '30%',
      maxHeight: 300,
      overflow: 'hidden',
      display: 'block',
    },
  }),
);

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
  const classes = useStyles();
  const theme = useTheme();

  const [activeStep, setActiveStep] = useState<number>(0);
  const maxSteps = beers.length;

  const handleNext = () => setActiveStep((prevActiveStep) => prevActiveStep + 1);

  const handleBack = () => setActiveStep((prevActiveStep) => prevActiveStep - 1);

  if (maxSteps === 0) return null;

  return (
    <div className={classes.root}>
      <Grid container justifyContent="center">
        <img
          className={classes.img}
          src={beers[activeStep].image}
          alt={beers[activeStep].name}
        />
      </Grid>

      <BeerForm
        beerID={beers[activeStep].id}
      />

      <MobileStepper
        steps={maxSteps}
        position="static"
        variant="text"
        activeStep={activeStep}
        nextButton={
          <Button size="small" onClick={handleNext} disabled={activeStep === maxSteps - 1}>
            Next
            {theme.direction === 'rtl' ? <KeyboardArrowLeft/> : <KeyboardArrowRight/>}
          </Button>
        }
        backButton={
          <Button size="small" onClick={handleBack} disabled={activeStep === 0}>
            {theme.direction === 'rtl' ? <KeyboardArrowRight/> : <KeyboardArrowLeft/>}
            Back
          </Button>
        }
      />
    </div>
  );
}

export default BeerFormStepper;
