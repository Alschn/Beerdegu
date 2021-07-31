import React, {FC} from "react";
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import {useRoomContext} from "../../hooks/useContextHook";
import {
  TableHeaderCell,
  TableHeaderIndexCell,
  TableHighlightedCell,
  TableIndexCell,
  TableRowCell
} from "../utils/TableCells";


const UserRatingsTable: FC = () => {
  const {userResults} = useRoomContext();

  return (
    <TableContainer component={Paper}>
      <Table aria-label="user-results-table">
        <TableHead>
          <TableRow>
            <TableHeaderIndexCell>Numer</TableHeaderIndexCell>
            <TableHeaderCell>Kolor</TableHeaderCell>
            <TableHeaderCell>Piana</TableHeaderCell>
            <TableHeaderCell>Zapach</TableHeaderCell>
            <TableHeaderCell>Smak</TableHeaderCell>
            <TableHeaderCell>Opinia</TableHeaderCell>
            <TableHeaderCell align="center">Ocena</TableHeaderCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {userResults.length > 0 && userResults.map(({color, foam, smell, taste, opinion, note}, idx) => (
            <TableRow>
              <TableIndexCell component="th" scope="row">{idx + 1}</TableIndexCell>
              <TableRowCell>{color}</TableRowCell>
              <TableRowCell>{foam}</TableRowCell>
              <TableRowCell>{smell}</TableRowCell>
              <TableRowCell>{taste}</TableRowCell>
              <TableRowCell>{opinion}</TableRowCell>
              <TableHighlightedCell align="right">{note}</TableHighlightedCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default UserRatingsTable
