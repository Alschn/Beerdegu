import {withStyles} from "@material-ui/core";
import TableCell from "@material-ui/core/TableCell";

export const TableRowCell = withStyles(theme => ({
  root: {
    backgroundColor: '#ffffff',
  }
}))(TableCell);

export const TableHeaderCell = withStyles(theme => ({
  root: {
    backgroundColor: '#00ae1a',
    fontSize: '18px',
    fontWeight: 700,
  }
}))(TableCell);

export const TableHeaderIndexCell = withStyles(theme => ({
  root: {
    fontSize: '18px',
    fontWeight: 700,
  }
}))(TableCell);

export const TableIndexCell = withStyles(theme => ({
  root: {
    backgroundColor: 'rgba(193, 0, 0, 0.95)',
    color: 'white',
    textAlign: 'center',
    fontSize: '16px',
    fontWeight: 700,
    width: 50,
    border: '1px solid rgba(0, 0, 0, 0.3)'
  }
}))(TableCell);

export const TableHighlightedCell = withStyles(theme => ({
  root: {
    backgroundColor: '#e5e5e5',
    fontSize: '16px',
    fontWeight: 700,
    textAlign: 'center',
    width: 130,
  }
}))(TableCell);
