import {FC} from 'react';
import {Box, Button, Card, CardActions, CardContent, Tooltip, Typography} from '@mui/material';
import {useRoomContext} from "../../hooks/useContextHook";
import {addBeerToRoom} from "../../api/room";


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
      <Card sx={(theme) => ({
        maxWidth: 345, minWidth: 200,
        [theme.breakpoints.down('sm')]: {
          maxWidth: 225,
        },
        [theme.breakpoints.up('md')]: {
          maxWidth: 225,
        },
        margin: 2,
      })}>
        <Tooltip title={description ?? ''}>
          <CardContent>
            <Box display="flex" justifyContent="center">
              <img src={image} alt="" height={100}/>
            </Box>

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
      <Card sx={{display: 'flex', margin: '16px 8px', alignItems: 'center'}}>
        <img src={image} alt="" height={150}/>

        <Box display="flex" justifyContent="center" flexDirection="column">
          <CardContent sx={{flex: "1 0 auto"}}>
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
        </Box>
      </Card>
    );
  }
};

export default BeerCard;
