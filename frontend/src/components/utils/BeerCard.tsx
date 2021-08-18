import React, {FC} from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Tooltip from '@material-ui/core/Tooltip';
import {useRoomContext} from "../../hooks/useContextHook";
import {addBeerToRoom} from "../../api/room";

const useStyles = makeStyles(theme => ({
  root: {
    maxWidth: 345,
    minWidth: 200,
    [theme.breakpoints.down('sm')]: {
      maxWidth: 225,
    },
    [theme.breakpoints.up('md')]: {
      maxWidth: 225,
    },
  },
  main: {},
  media: {},
}));

interface MediaCardProps {
  beerId: number,
  name: string,
  description?: string,
  image?: string,
  brewery?: string,
}

const BeerCard: FC<MediaCardProps> = (
  {
    beerId,
    name,
    description,
    image,
    brewery
  }
) => {
  const classes = useStyles();
  const {beers, sendMessage, code, isHost} = useRoomContext();

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
        <CardActionArea className={classes.main}>
          <CardMedia
            component="img"
            alt=""
            height="200"
            image={image}
            className={classes.media}
          />
          <CardContent>
            <Typography gutterBottom variant="h5" component="h2">
              {name}
            </Typography>
            <Typography variant="body2" color="textSecondary" component="p">
              {brewery && `Browar ${brewery}`}
            </Typography>
          </CardContent>
        </CardActionArea>
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
}

export default BeerCard;
