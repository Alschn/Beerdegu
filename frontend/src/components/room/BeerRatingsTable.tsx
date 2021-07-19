import React from "react";
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import {useRoomContext} from "../../hooks/useContextHook";


export default function BeerRatingsTable() {
  const {results} = useRoomContext();

  return (
    <TableContainer component={Paper}>
      <Table aria-label="results-table">
        <TableHead>
          <TableRow>
            <TableCell>Numer</TableCell>
            <TableCell>Nazwa</TableCell>
            <TableCell>Browar</TableCell>
            <TableCell>Styl</TableCell>
            <TableCell align="right">Średnia Ocena</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {results.length > 0 && results.map(({beer, average_rating}, idx) => (
            <TableRow>
              <TableCell component="th" scope="row">{idx + 1}</TableCell>
              <TableCell>{beer.name}</TableCell>
              <TableCell>{beer.brewery}</TableCell>
              <TableCell>{beer.style}</TableCell>
              <TableCell align="right">{average_rating}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
