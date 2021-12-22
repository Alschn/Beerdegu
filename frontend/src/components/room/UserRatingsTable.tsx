import {FC} from "react";
import {Paper, Table, TableBody, TableContainer, TableHead, TableRow} from '@mui/material';
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
};

export default UserRatingsTable;
