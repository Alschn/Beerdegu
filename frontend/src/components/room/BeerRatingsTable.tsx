import React from "react";
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


export default function BeerRatingsTable() {
  const {results} = useRoomContext();

  return (
    <TableContainer component={Paper}>
      <Table aria-label="results-table">
        <TableHead>
          <TableRow>
            <TableHeaderIndexCell>Numer</TableHeaderIndexCell>
            <TableHeaderCell>Nazwa</TableHeaderCell>
            <TableHeaderCell>Browar</TableHeaderCell>
            <TableHeaderCell>Styl</TableHeaderCell>
            <TableHeaderCell align="center">Średnia Ocena</TableHeaderCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {results.length > 0 && results.map(({beer, average_rating}, idx) => (
            <TableRow>
              <TableIndexCell component="th" scope="row">{idx + 1}</TableIndexCell>
              <TableRowCell>{beer.name}</TableRowCell>
              <TableRowCell>{beer.brewery}</TableRowCell>
              <TableRowCell>{beer.style}</TableRowCell>
              <TableHighlightedCell>{average_rating}</TableHighlightedCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
