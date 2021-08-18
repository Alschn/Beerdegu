import React, {FC, useCallback, useEffect, useState} from "react";
import {Grid, List} from "@material-ui/core";
import {getBeersByQuery} from "../../api/search";
import {BeerObject} from "../../utils/ws";
import BeerCard from "../utils/BeerCard";
import "./SearchAPI.scss";
import {useRoomContext} from "../../hooks/useContextHook";
import Tooltip from "@material-ui/core/Tooltip";
import ListItem from "@material-ui/core/ListItem";
import ListItemAvatar from "@material-ui/core/ListItemAvatar";
import Avatar from "@material-ui/core/Avatar";
import ListItemText from "@material-ui/core/ListItemText";
import ListItemSecondaryAction from "@material-ui/core/ListItemSecondaryAction";
import IconButton from "@material-ui/core/IconButton";
import DeleteIcon from '@material-ui/icons/Delete';
import SearchIcon from '@material-ui/icons/Search';
import {removeBeerFromRoom} from "../../api/room";


const SearchAPI: FC = () => {
  const [results, setResults] = useState<BeerObject[]>([]);
  const [query, setQuery] = useState<string>("");

  const {beers, sendMessage, roomState, code, isHost} = useRoomContext();

  const handleQueryChange = (e: React.BaseSyntheticEvent): void => setQuery(e.target.value);

  const handleSubmit = (): void => {
    getBeersByQuery(query).then(
      res => setResults(res.data)
    ).catch(err => console.log(err));
  };

  const removeBeer = (id: number) => {
    removeBeerFromRoom(code, id).then(() => {
      loadBeers();
    }).catch(err => console.log(err));
  };

  const loadBeers = useCallback(() => {
    sendMessage({
      command: 'load_beers',
    });
  }, [sendMessage]);

  useEffect(() => {
    loadBeers();
  }, [loadBeers]);

  const renderHostView = (): JSX.Element => {
    return (
      <>
        <Grid item xs={12} sm={6} md={8} lg={9}>
          <Grid item xs={12} className="search-api__inputs-header">
            <h2>Wyszukaj piwa:</h2>
          </Grid>

          <Grid item xs={12} className="search-api__inputs">
            <input value={query} onChange={handleQueryChange}/>
            <button onClick={handleSubmit}>
              <SearchIcon/>
            </button>
          </Grid>

          <Grid container className="search-api__results">
            {results.length > 0 && results.map((beer) => (
              <BeerCard
                beerId={beer.id}
                name={beer.name}
                description={beer.description}
                image={beer.image}
                brewery={beer.brewery.name}
              />
            ))}
          </Grid>
        </Grid>

        <Grid item xs={12} sm={6} md={4} lg={3}>
          <Grid item xs={12} className="beers-list">
            <h2>Piwa w pokoju:</h2>
            <List>
              {beers && beers.length > 0 && beers.map((beer) => (
                <Tooltip title={String(beer.description)}>
                  <ListItem className="beers-list-item">
                    <ListItemAvatar>
                      <Avatar>
                        <img src={beer.image} alt="" height={40}/>
                      </Avatar>
                    </ListItemAvatar>

                    <ListItemText className="beers-list-item-name">
                      {beer.name}
                    </ListItemText>

                    <ListItemSecondaryAction>
                      <IconButton edge="end" aria-label="delete" onClick={() => removeBeer(beer.id)}>
                        <DeleteIcon/>
                      </IconButton>
                    </ListItemSecondaryAction>
                  </ListItem>
                </Tooltip>
              ))}
            </List>
          </Grid>
        </Grid>
      </>
    );
  };

  const renderNormalUserView = (): JSX.Element => {
    return (
      <Grid item xs={12} className="beers-list-casual-wrapper">
        <List className="beers-list-casual">
          <h2>Piwa w pokoju:</h2>

          {beers && beers.length > 0 && beers.map((beer) => (
            <Tooltip title={String(beer.description)}>
              <ListItem className="beers-list-item">
                <ListItemAvatar>
                  <Avatar>
                    <img src={beer.image} alt="" height={40}/>
                  </Avatar>
                </ListItemAvatar>

                <ListItemText className="beers-list-item-name">
                  {beer.name}
                </ListItemText>
              </ListItem>
            </Tooltip>
          ))}
        </List>
      </Grid>
    );
  };

  return (
    <Grid container className="search-api">
      <Grid item xs={12} className="search-api__header">
        <h2>Stan: {roomState}</h2>
      </Grid>

      {isHost ? renderHostView() : renderNormalUserView()}
    </Grid>
  );
};

export default SearchAPI;
