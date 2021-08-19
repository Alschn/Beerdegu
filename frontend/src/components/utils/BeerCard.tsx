import React, {FC} from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Tooltip from '@material-ui/core/Tooltip';
import {useRoomContext} from "../../hooks/useContextHook";
import {addBeerToRoom} from "../../api/room";

const useStyles = makeStyles(theme => ({
  // casual = false
  root: {
    maxWidth: 345,
    minWidth: 200,
    [theme.breakpoints.down('sm')]: {
      maxWidth: 225,
    },
    [theme.breakpoints.up('md')]: {
      maxWidth: 225,
    },
    margin: 8,
  },
  main: {
    display: 'flex',
    justifyContent: 'center',
  },
  media: {
    height: 100,
  },
  // casual = true
  rootCasual: {
    display: 'flex',
    margin: '16px 8px',
    alignItems: 'center',
  },
  details: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  content: {
    flex: '1 0 auto',
  },
  image: {
    height: 150,
  },
}));

interface MediaCardProps {
  beerId: number,
  name: string,
  description?: string,
  image?: string,
  brewery?: string,
  casual: boolean
}

const BeerCard: FC<MediaCardProps> = (
  {
    beerId,
    name,
    description,
    image,
    brewery,
    casual = false,
  }
) => {
  const classes = useStyles();
  const {beers, sendMessage, code, isHost} = useRoomContext();

  if (!casual) {
    const addBeer = (): void => {
      addBeerToRoom(code, beerId).then(() => {
        sendMessage({
          command: 'load_beers',
        });
      }).catch(err => console.log(err));
    };

    const isBeerInRoom = (): boolean => beers.some((beer) => beer.id === beerId);

    return (
      <Card className={classes.root}>
        <Tooltip title={description ?? ''}>
          <CardContent>
            <div className={classes.main}>
              <img src={image} alt="" className={classes.media}/>
            </div>

            <Typography gutterBottom variant="h6">
              {name}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              {brewery && `Browar ${brewery}`}
            </Typography>
          </CardContent>
        </Tooltip>
        <CardActions>
          {isHost && !isBeerInRoom() && (
            <Button
              size="small" color="primary" variant="contained"
              onClick={addBeer}
            >
              Dodaj
            </Button>
          )}
        </CardActions>
      </Card>
    );
  } else {
    return (
      <Card className={classes.rootCasual}>
        <img
          className={classes.image}
          src={image}
          alt=""
        />
        <div className={classes.details}>
          <CardContent className={classes.content}>
            <Typography component="h5" variant="h5">
              {name}
            </Typography>
            <Typography variant="subtitle1">
              {brewery && `Browar ${brewery}`}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              {description}
            </Typography>
          </CardContent>
        </div>
      </Card>
    );
  }
};

export default BeerCard;
