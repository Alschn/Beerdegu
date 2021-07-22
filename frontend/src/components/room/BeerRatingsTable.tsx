import React from "react";
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import {useRoomContext} from "../../hooks/useContextHook";
import {TableHeaderCell, TableHeaderIndexCell, TableHighlightedCell, TableIndexCell} from "../utils/TableCells";


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
              <TableCell>{beer.name}</TableCell>
              <TableCell>{beer.brewery}</TableCell>
              <TableCell>{beer.style}</TableCell>
              <TableHighlightedCell>{average_rating}</TableHighlightedCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
