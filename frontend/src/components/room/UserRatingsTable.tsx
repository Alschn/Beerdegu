import React, {FC} from "react";
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import {useRoomContext} from "../../hooks/useContextHook";


const UserRatingsTable: FC = () => {
  const {userResults} = useRoomContext();

  return (
    <TableContainer component={Paper}>
      <Table aria-label="user-results-table">
        <TableHead>
          <TableRow>
            <TableCell>Numer</TableCell>
            <TableCell>Kolor</TableCell>
            <TableCell>Piana</TableCell>
            <TableCell>Zapach</TableCell>
            <TableCell>Smak</TableCell>
            <TableCell>Opinia</TableCell>
            <TableCell align="right">Ocena</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {userResults.length > 0 && userResults.map(({color, foam, smell, taste, opinion, note}, idx) => (
            <TableRow>
              <TableCell component="th" scope="row">{idx + 1}</TableCell>
              <TableCell>{color}</TableCell>
              <TableCell>{foam}</TableCell>
              <TableCell>{smell}</TableCell>
              <TableCell>{taste}</TableCell>
              <TableCell>{opinion}</TableCell>
              <TableCell align="right">{note}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default UserRatingsTable
