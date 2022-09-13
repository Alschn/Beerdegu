import {styled} from "@mui/material/styles";
import TableCell from "@mui/material/TableCell";

export const TableRowCell = styled(TableCell)(({theme}) => ({
  backgroundColor: '#ffffff',
}));

export const TableHeaderCell = styled(TableCell)(({theme}) => ({
  backgroundColor: '#00ae1a',
  fontSize: '18px',
  fontWeight: 700,
}));

export const TableHeaderIndexCell = styled(TableCell)(({theme}) => ({
  fontSize: '18px',
  fontWeight: 700,
}));

export const TableIndexCell = styled(TableCell)(({theme}) => ({
  backgroundColor: 'rgba(193, 0, 0, 0.95)',
  color: 'white',
  textAlign: 'center',
  fontSize: '16px',
  fontWeight: 700,
  width: 50,
  border: '1px solid rgba(0, 0, 0, 0.3)'
}));

export const TableHighlightedCell = styled(TableCell)(({theme}) => ({
  backgroundColor: '#e5e5e5',
  fontSize: '16px',
  fontWeight: 700,
  textAlign: 'center',
  width: 130,
}));
