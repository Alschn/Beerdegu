import {BaseSyntheticEvent, FC, useCallback, useEffect, useMemo, useState} from "react";
import {
  Avatar,
  Grid,
  IconButton,
  List,
  ListItem,
  ListItemAvatar,
  ListItemSecondaryAction,
  ListItemText,
  Tooltip
} from "@mui/material";
import {getBeersByQuery} from "../../api/beers";
import BeerCard from "../utils/BeerCard";
import {useRoomContext} from "../../hooks/useContextHook";
import DeleteIcon from '@mui/icons-material/Delete';
import {removeBeerFromRoom} from "../../api/rooms";
import "./SearchAPI.scss";
import useDebounce from "../../hooks/useDebounce";
import {useInfiniteQuery} from "react-query";
import InfiniteScroll from "react-infinite-scroll-component";


const HostView: FC = () => {

  const {beers, sendMessage, code, isHost} = useRoomContext();


  const [query, setQuery] = useState<string>("");
  const debouncedQuery = useDebounce(query, 1_000);

  const {
    isFetching: isFetchingBeers,
    isSuccess: isSuccessBeers,
    data: beersData,
    hasNextPage: hasNextPageBeers,
    fetchNextPage: fetchNextPageBeers,
  } = useInfiniteQuery(
    ["beers", debouncedQuery],
    ({pageParam = 1, queryKey}) => getBeersByQuery(queryKey[1], pageParam), {
      enabled: isHost,
      refetchOnWindowFocus: false,
      getNextPageParam: (lastPage) => {
        if (lastPage.data.next !== null) {
          return lastPage.data.next.split('page=').pop();
        }
        return undefined;
      }
    }
  );

  const results = useMemo(() => {
    if (!beersData || !beersData.pages) return [];
    return beersData.pages.map(page => page.data.results).flat();
  }, [beersData]);

  const handleQueryChange = (e: BaseSyntheticEvent): void => setQuery(e.target.value);

  const loadBeers = useCallback(() => {
    sendMessage({command: 'load_beers'});
  }, [sendMessage]);

  const removeBeer = (id: number) => {
    removeBeerFromRoom(code, id).then(() => {
      loadBeers();
    }).catch(err => console.log(err));
  };

  return (
    <>
      <Grid item xs={12} sm={6} md={8} lg={9}>
        <Grid item xs={12} className="search-api__inputs-header">
          <h2>Wyszukaj piwa:</h2>
        </Grid>

        <Grid item xs={12} className="search-api__inputs">
          <input
            value={query}
            onChange={handleQueryChange}
            placeholder="Wpisz nazwę piwa, by wyszukać..."
          />
        </Grid>

        <InfiniteScroll
          next={fetchNextPageBeers}
          hasMore={Boolean(hasNextPageBeers)}
          loader={<></>}
          dataLength={beersData ? beersData.pages[0].data.count : 0}
          scrollableTarget={"root"}
        >
          <Grid container className="search-api__results">
            {results.map((beer) => (
              <BeerCard
                beerId={beer.id}
                name={beer.name}
                description={beer.description}
                image={beer.image}
                brewery={beer.brewery.name}
                casual={false}
                key={`beer-${beer.id}`}
              />
            ))}
          </Grid>
        </InfiniteScroll>
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

const ParticipantView: FC = () => {
  const {beers} = useRoomContext();

  return (
    <Grid item xs={12} className="beers-list-casual-wrapper">
      <List className="beers-list-casual">
        <h2>Piwa w pokoju:</h2>

        {beers && beers.length > 0 && beers.map((beer) => (
          <BeerCard
            beerId={beer.id}
            name={beer.name}
            description={beer.description}
            image={beer.image}
            brewery={beer.brewery.name}
            casual
          />
        ))}
      </List>
    </Grid>
  );
};


const SearchAPI: FC = () => {
  const {sendMessage, roomState, isHost} = useRoomContext();

  const loadBeers = useCallback(() => {
    sendMessage({
      command: 'load_beers',
    });
  }, [sendMessage]);

  useEffect(() => {
    // load beers in room on load
    loadBeers();
  }, [loadBeers]);

  return (
    <Grid container className="search-api">
      <Grid item xs={12} className="search-api__header">
        <h2>Stan: {roomState}</h2>
      </Grid>

      {isHost ? <HostView/> : <ParticipantView/>}
    </Grid>
  );
};

export default SearchAPI;
