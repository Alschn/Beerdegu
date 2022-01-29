import {Paper, Table, TableBody, TableContainer, TableHead, TableRow} from '@mui/material';
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
