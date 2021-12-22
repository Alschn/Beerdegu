import {FC, MouseEvent, useEffect, useReducer, useState} from 'react';
import {
  Button,
  Container,
  Divider,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow
} from '@mui/material';
import {getRooms} from "../../api/lobby";
import CreateRoomDialog from "../lobby/CreateRoomDialog";
import JoinRoomDialog from "../lobby/JoinRoomDialog";
import "./Lobby.scss";


interface Column {
  id: 'name' | 'host' | 'slots' | 'state' | 'has_password';
  label: string;
  align?: 'right' | 'left',
  minWidth?: number;
}

const columns: Column[] = [
  {id: 'name', label: 'Name', minWidth: 100},
  {id: 'host', label: 'Host', minWidth: 100},
  {id: 'slots', label: 'Slots', minWidth: 40},
  {id: 'state', label: 'State', minWidth: 100},
  {id: 'has_password', label: 'Password', minWidth: 40},
];

interface User {
  id: number;
  username: string;
}

interface RoomData {
  beers: [],
  created_at: Date,
  has_password: boolean,
  host: null | User,
  id: number,
  name: string,
  slots: number,
  state: string,
  updated_at: Date,
  users: []
}

const getFormattedValue = (row: any, column: Column) => {
  const value = row[column.id];
  switch (column.id) {
    case "host":
      if (value != null) return value.username;
      break;
    case "slots":
      return `${row.users.length}/${value}`;
    default:
      return String(value);
  }
};

const REFRESH_DATA_INTERVAL_MS = 10_000;

type State = {
  isJoinDialogOpen: boolean,
  isCreateDialogOpen: boolean,
}

type Action =
  { type: 'OPEN_JOIN_DIALOG', payload: true } |
  { type: 'CLOSE_JOIN_DIALOG', payload: false } |
  { type: 'OPEN_CREATE_DIALOG', payload: true } |
  { type: 'CLOSE_CREATE_DIALOG', payload: false }

const initialState = {isJoinDialogOpen: false, isCreateDialogOpen: false};

const dialogReducer = (state: State = initialState, action: Action) => {
  switch (action.type) {
    case "OPEN_JOIN_DIALOG":
      return {...state, isJoinDialogOpen: action.payload};
    case "CLOSE_JOIN_DIALOG":
      return {...state, isJoinDialogOpen: action.payload};
    case "OPEN_CREATE_DIALOG":
      return {...state, isCreateDialogOpen: action.payload};
    case "CLOSE_CREATE_DIALOG":
      return {...state, isCreateDialogOpen: action.payload};
    default:
      return state;
  }
};

const Lobby: FC = () => {
  const [rooms, setRooms] = useState<RoomData[]>([]);

  const [selected, setSelected] = useState<string | null>(null);
  const [{isJoinDialogOpen, isCreateDialogOpen}, dispatch] = useReducer(dialogReducer, initialState);

  useEffect(() => {
    // get initial data
    getRooms().then((res) => {
      setRooms(res.data);
    }).catch(err => console.log(err));
  }, []);

  useEffect(() => {
    // refresh data every n seconds
    const interval = setInterval(() => {
      getRooms().then((res) => {
        setRooms(res.data);
      }).catch(err => console.log(err));
    }, REFRESH_DATA_INTERVAL_MS);

    return () => clearInterval(interval);
  }, []);


  const handleRowClick = (e: MouseEvent<HTMLTableRowElement>) => {
    const roomName = e.currentTarget.getAttribute('data-room-name');
    setSelected(roomName);
  };

  return (
    <Container className="lobby">
      <h1 className="lobby-title">Lobby</h1>

      <Paper className="lobby-container">
        <TableContainer className="lobby-table-container">
          <Table stickyHeader aria-label="sticky-table">
            <TableHead>
              <TableRow>
                {columns.map((column) => (
                  <TableCell
                    key={column.id}
                    align={column.align}
                    style={{minWidth: column.minWidth}}
                  >
                    <strong>{column.label}</strong>
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {rooms.length > 0 && rooms.map((row: any) => (
                <TableRow
                  hover role="checkbox" tabIndex={-1} key={row.name} data-room-name={row.name}
                  onClick={handleRowClick}
                  selected={selected === row.name}
                >
                  {columns.map((column) => {
                    return (
                      <TableCell key={column.id} align="left">
                        {getFormattedValue(row, column)}
                      </TableCell>
                    );
                  })}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        <Divider/>

        <div className="lobby-bar">
          <div className="grow-full"/>

          {selected != null && (
            <Button
              onClick={() => dispatch({type: 'OPEN_JOIN_DIALOG', payload: true})}
              variant="contained"
              color="primary"
            >
              Join Room
            </Button>
          )}

          <Button
            onClick={() => dispatch({type: 'OPEN_CREATE_DIALOG', payload: true})}
            variant="contained"
            color="error"
          >
            Create Room
          </Button>
        </div>
      </Paper>

      <JoinRoomDialog isOpen={isJoinDialogOpen} dispatch={dispatch} roomName={selected}/>
      <CreateRoomDialog isOpen={isCreateDialogOpen} dispatch={dispatch}/>
    </Container>
  );
};

export default Lobby;
